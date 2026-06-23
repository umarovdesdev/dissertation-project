"""U-Net with a timm encoder + 2-channel heatmap head + DSNT decoding.

Architecture (brief §5):
  * encoder: a ``timm`` backbone with ``features_only=True`` (ResNet-18 default,
    EfficientNet-B0 option), ImageNet-pretrained;
  * decoder: a light U-Net that upsamples and fuses skip features to a single
    stride, producing a ``heatmap_size`` x ``heatmap_size`` feature map;
  * head: a 1x1 conv to ``out_channels`` (OD, fovea) heatmap logits;
  * decode: spatial softmax -> DSNT soft-argmax -> normalized coordinates,
    plus per-channel second moments for uncertainty.

Both landmarks are predicted jointly from a shared encoder so the fixed
OD<->fovea geometry acts as an implicit prior.

This module imports torch/timm; it is only usable in the ``dr-classifier``
environment.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

try:
    import timm
    _HAS_TIMM = True
except Exception:  # pragma: no cover
    timm = None  # type: ignore
    _HAS_TIMM = False

from .dsnt import dsnt, dsnt_second_moments, spatial_softmax


class _ConvBlock(nn.Module):
    """Two 3x3 conv + BN + ReLU layers."""

    def __init__(self, in_ch: int, out_ch: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class HeatmapUNet(nn.Module):
    """U-Net (timm encoder) producing OD + fovea heatmaps and DSNT coords."""

    def __init__(
        self,
        backbone: str = "resnet18",
        pretrained: bool = True,
        out_channels: int = 2,
        decoder_channels: tuple[int, ...] = (256, 128, 64, 32, 16),
        heatmap_size: int = 128,
    ) -> None:
        """Build the network.

        Args:
            backbone: timm encoder name (``"resnet18"`` or ``"efficientnet_b0"``).
            pretrained: Load ImageNet-pretrained encoder weights.
            out_channels: Number of landmark heatmaps (2: OD, fovea).
            decoder_channels: Channel widths for successive decoder stages.
            heatmap_size: Square output heatmap side; output is bilinearly
                resized to this if the decoder stride differs.
        """
        super().__init__()
        if not _HAS_TIMM:
            raise ImportError("timm is required to build HeatmapUNet")
        self.heatmap_size = heatmap_size
        self.encoder = timm.create_model(
            backbone, features_only=True, pretrained=pretrained, in_chans=3,
        )
        enc_chs = self.encoder.feature_info.channels()  # low->high stride

        # Decoder: walk from the deepest feature up, fusing skips.
        rev = list(reversed(enc_chs))  # deepest first
        dec_chs = list(decoder_channels)
        self.up_blocks = nn.ModuleList()
        in_ch = rev[0]
        for i in range(1, len(rev)):
            out_ch = dec_chs[min(i - 1, len(dec_chs) - 1)]
            self.up_blocks.append(_ConvBlock(in_ch + rev[i], out_ch))
            in_ch = out_ch
        # Optional extra refinement block at the shallowest decoder stride.
        self.final_conv = _ConvBlock(in_ch, dec_chs[-1])
        self.head = nn.Conv2d(dec_chs[-1], out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        """Run the network.

        Args:
            x: Input images ``(B, 3, S, S)`` in ``[0, 1]``.

        Returns:
            Dict with:
              * ``heatmap_logits`` ``(B, C, Hh, Hw)``,
              * ``heatmap`` softmax-normalized ``(B, C, Hh, Hw)``,
              * ``coords`` ``(B, C, 2)`` normalized ``[-1, 1]`` (x, y),
              * ``var`` ``(B, C, 2)`` second moments (heatmap-pixel^2).
        """
        feats = self.encoder(x)            # list low->high stride
        rev = list(reversed(feats))        # deepest first
        h = rev[0]
        for i, block in enumerate(self.up_blocks, start=1):
            skip = rev[i]
            h = F.interpolate(h, size=skip.shape[-2:], mode="bilinear",
                              align_corners=False)
            h = block(torch.cat([h, skip], dim=1))
        h = self.final_conv(h)
        if h.shape[-1] != self.heatmap_size:
            h = F.interpolate(h, size=(self.heatmap_size, self.heatmap_size),
                              mode="bilinear", align_corners=False)
        logits = self.head(h)
        prob = spatial_softmax(logits)
        coords = dsnt(prob)
        var = dsnt_second_moments(prob)
        return {
            "heatmap_logits": logits,
            "heatmap": prob,
            "coords": coords,
            "var": var,
        }


def build_model(model_cfg: dict, heatmap_size: int) -> HeatmapUNet:
    """Construct a :class:`HeatmapUNet` from a config dict.

    Args:
        model_cfg: The ``model`` section of the config.
        heatmap_size: Decoder output side (from ``data.heatmap_size``).

    Returns:
        An initialized :class:`HeatmapUNet`.
    """
    return HeatmapUNet(
        backbone=model_cfg.get("backbone", "resnet18"),
        pretrained=model_cfg.get("pretrained", True),
        out_channels=model_cfg.get("out_channels", 2),
        decoder_channels=tuple(model_cfg.get(
            "decoder_channels", (256, 128, 64, 32, 16))),
        heatmap_size=heatmap_size,
    )
