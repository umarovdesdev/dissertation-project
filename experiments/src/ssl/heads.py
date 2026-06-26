"""Projection / prediction / DINO MLP heads for SSL methods (brief §5.1).

These small MLPs attach to the pooled trunk features. They carry no backbone
weights and are **not** saved into the SSL checkpoint (only the trunk is —
brief §9.2).
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class MLPHead(nn.Module):
    """2-layer MLP head: ``Linear → BN → ReLU → Linear`` (optional final BN).

    The default shape (BN on the hidden layer only) matches the BYOL projector
    and predictor. Setting ``last_bn=True`` adds a final BatchNorm (used by some
    projector variants).

    Args:
        in_dim: Input feature dimension.
        hidden_dim: Hidden layer width.
        out_dim: Output dimension.
        use_bn: Apply BatchNorm after the hidden linear. Default ``True``.
        last_bn: Apply BatchNorm after the output linear. Default ``False``.
    """

    def __init__(
        self,
        in_dim: int,
        hidden_dim: int,
        out_dim: int,
        use_bn: bool = True,
        last_bn: bool = False,
    ) -> None:
        super().__init__()
        layers: list[nn.Module] = [nn.Linear(in_dim, hidden_dim, bias=not use_bn)]
        if use_bn:
            layers.append(nn.BatchNorm1d(hidden_dim))
        layers.append(nn.ReLU(inplace=True))
        layers.append(nn.Linear(hidden_dim, out_dim))
        if last_bn:
            layers.append(nn.BatchNorm1d(out_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply the MLP.

        Args:
            x: Input tensor of shape ``(N, in_dim)``.

        Returns:
            Output tensor of shape ``(N, out_dim)``.
        """
        return self.net(x)


class DINOHead(nn.Module):
    """DINO projection head: 3-layer MLP → L2-normalize → weight-normed linear.

    Mirrors the canonical DINO head (Caron et al. 2021): an MLP bottleneck
    followed by an L2-normalized, weight-normalized last layer whose
    magnitude (``weight_g``) is fixed to 1 and frozen.

    Args:
        in_dim: Input feature dimension.
        out_dim: Output dimension (DINO prototype count, e.g. 65536).
        hidden_dim: MLP hidden width. Default 2048.
        bottleneck_dim: Bottleneck width before the last layer. Default 256.
    """

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        hidden_dim: int = 2048,
        bottleneck_dim: int = 256,
    ) -> None:
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, bottleneck_dim),
        )
        last_layer = nn.Linear(bottleneck_dim, out_dim, bias=False)
        self.last_layer = nn.utils.weight_norm(last_layer)
        # Fix the weight magnitude to 1 (standard DINO).
        self.last_layer.weight_g.data.fill_(1.0)
        self.last_layer.weight_g.requires_grad = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Project features to prototype logits.

        Args:
            x: Pooled features of shape ``(N, in_dim)``.

        Returns:
            Logits of shape ``(N, out_dim)``.
        """
        x = self.mlp(x)
        x = F.normalize(x, dim=-1, p=2)
        return self.last_layer(x)
