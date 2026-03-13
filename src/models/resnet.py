"""ResNet-50 model for 5-class DR classification."""

import torch.nn as nn
import torchvision.models as tv_models


def create_resnet50(
    num_classes: int = 5,
    pretrained: bool = True,
    dropout: float = 0.4,
    freeze_base: bool = False,
) -> nn.Module:
    """Build ResNet-50 with a custom 5-class head.

    Replaces the default 1000-class fc layer with
    Dropout → Linear(2048, num_classes).

    Args:
        num_classes: Number of output logits. Default: 5 (DR grades 0–4).
        pretrained: Load IMAGENET1K_V2 weights. Default: True.
        dropout: Dropout probability before the linear layer. Default: 0.4.
        freeze_base: If True, freeze all parameters except fc. Default: False.

    Returns:
        ResNet-50 nn.Module ready for fine-tuning.
    """
    weights = tv_models.ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
    model = tv_models.resnet50(weights=weights)

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
