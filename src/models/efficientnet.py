"""EfficientNet models (B0/B3/B4) for 5-class DR classification."""

import timm
import torch.nn as nn

_SUPPORTED_VARIANTS = {"b0", "b3", "b4"}


def create_efficientnet(
    variant: str = "b3",
    num_classes: int = 5,
    pretrained: bool = True,
    dropout: float = 0.4,
    freeze_base: bool = False,
) -> nn.Module:
    """Build an EfficientNet variant with a custom 5-class head.

    Uses timm to load the backbone, replaces the classifier with
    Dropout → Linear(in_features, num_classes).

    Args:
        variant: One of "b0", "b3", "b4". Default: "b3".
        num_classes: Number of output logits. Default: 5.
        pretrained: Load ImageNet weights via timm. Default: True.
        dropout: Dropout probability before the linear layer. Default: 0.4.
        freeze_base: If True, freeze all params except classifier. Default: False.

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
    in_features: int = model.classifier.in_features

    if freeze_base:
        for param in model.parameters():
            param.requires_grad = False

    model.classifier = nn.Sequential(
        nn.Dropout(p=dropout),
        nn.Linear(in_features, num_classes),
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
