"""ResNet-50 model for 5-class DR classification."""

import torch
import torch.nn as nn
import torchvision.models as tv_models


def create_resnet50(
    num_classes: int = 5,
    pretrained: bool = True,
    dropout: float = 0.4,
    freeze_base: bool = False,
    in_channels: int = 4,
) -> nn.Module:
    """Build ResNet-50 with a custom 5-class head and configurable input channels.

    Replaces the default 1000-class fc layer with
    Dropout → Linear(2048, num_classes).

    When in_channels != 3, the first Conv2d layer is replaced with a
    new layer that copies pretrained weights for the first 3 channels
    and initializes additional channels with the RGB mean.

    Args:
        num_classes: Number of output logits. Default: 5 (DR grades 0–4).
        pretrained: Load IMAGENET1K_V2 weights. Default: True.
        dropout: Dropout probability before the linear layer. Default: 0.4.
        freeze_base: If True, freeze all parameters except fc. Default: False.
        in_channels: Number of input channels. Default: 4 (RGB + mask).

    Returns:
        ResNet-50 nn.Module ready for fine-tuning.
    """
    weights = tv_models.ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
    model = tv_models.resnet50(weights=weights)

    # Adapt first conv for 4-channel input
    if in_channels != 3:
        old_conv = model.conv1  # Conv2d(3, 64, 7, stride=2, padding=3, bias=False)
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
                # Initialize extra channels with mean of RGB weights
                for c in range(3, in_channels):
                    new_conv.weight[:, c] = old_conv.weight.mean(dim=1)
        model.conv1 = new_conv

    if freeze_base:
        for param in model.parameters():
            param.requires_grad = False

    model.fc = nn.Sequential(
        nn.Dropout(p=dropout),
        nn.Linear(2048, num_classes),
    )
    # fc is always trainable regardless of freeze_base
    for param in model.fc.parameters():
        param.requires_grad = True

    return model
