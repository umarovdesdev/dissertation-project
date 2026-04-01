"""EfficientNet models (B0/B3/B4) for 5-class DR classification."""

import timm
import torch
import torch.nn as nn

_SUPPORTED_VARIANTS = {"b0", "b3", "b4"}


def create_efficientnet(
    variant: str = "b3",
    num_classes: int = 5,
    pretrained: bool = True,
    dropout: float = 0.4,
    freeze_base: bool = False,
    in_channels: int = 4,
) -> nn.Module:
    """Build an EfficientNet variant with a custom 5-class head and configurable input channels.

    Uses timm to load the backbone, replaces the classifier with
    Dropout → Linear(in_features, num_classes).

    When in_channels != 3, the first Conv2d layer (conv_stem) is replaced
    with a new layer that copies pretrained weights for the first 3 channels
    and initializes additional channels with the RGB mean.

    Args:
        variant: One of "b0", "b3", "b4". Default: "b3".
        num_classes: Number of output logits. Default: 5.
        pretrained: Load ImageNet weights via timm. Default: True.
        dropout: Dropout probability before the linear layer. Default: 0.4.
        freeze_base: If True, freeze all params except classifier. Default: False.
        in_channels: Number of input channels. Default: 4 (RGB + mask).

    Returns:
        EfficientNet nn.Module ready for fine-tuning.

    Raises:
        ValueError: If variant is not in the supported set.
    """
    if variant not in _SUPPORTED_VARIANTS:
        raise ValueError(
            f"Unsupported variant '{variant}'. Choose from {_SUPPORTED_VARIANTS}."
        )

    model = timm.create_model(f"efficientnet_{variant}", pretrained=pretrained)
    feat_dim: int = model.classifier.in_features

    # Adapt first conv for 4-channel input
    if in_channels != 3:
        old_conv = model.conv_stem  # Conv2d(3, C_out, ...)
        new_conv = nn.Conv2d(
            in_channels, old_conv.out_channels,
            kernel_size=old_conv.kernel_size,
            stride=old_conv.stride,
            padding=old_conv.padding,
            bias=old_conv.bias is not None,
        )
        if pretrained:
            with torch.no_grad():
                new_conv.weight[:, :3] = old_conv.weight
                for c in range(3, in_channels):
                    new_conv.weight[:, c] = old_conv.weight.mean(dim=1)
        model.conv_stem = new_conv

    if freeze_base:
        for param in model.parameters():
            param.requires_grad = False

    model.classifier = nn.Sequential(
        nn.Dropout(p=dropout),
        nn.Linear(feat_dim, num_classes),
    )
    # classifier is always trainable
    for param in model.classifier.parameters():
        param.requires_grad = True

    return model


def get_gradcam_target_layer(model: nn.Module, variant: str = "b4") -> nn.Module:
    """Return the Grad-CAM target layer for a timm EfficientNet model.

    Uses conv_head (the last convolutional layer before global pooling),
    which produces spatially-rich feature maps suitable for activation
    visualisation and IoU computation against IDRiD lesion masks (Exp 4).

    Args:
        model: A timm EfficientNet model (output of create_efficientnet).
        variant: Model variant string — currently unused but kept for
                 forward-compatibility if layer selection diverges per variant.

    Returns:
        The conv_head nn.Conv2d module.
    """
    return model.conv_head
