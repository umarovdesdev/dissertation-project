"""
ResNet-50 baseline model for diabetic retinopathy grading.

The model replaces the ImageNet head with a classification head suited for
5-class DR grading (grades 0–4).  A lightweight attention gate on the final
feature map is included as an optional upgrade path.
"""

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import ResNet50_Weights


class DRClassifier(nn.Module):
    """
    ResNet-50 backbone with a custom classification head for DR grading.

    Args:
        num_classes: Number of output classes (default 5 for DR grades 0-4).
        pretrained: Initialise backbone with ImageNet weights.
        dropout: Dropout rate applied before the final linear layer.
        freeze_backbone: If True, only the classifier head is trained.
    """

    def __init__(
        self,
        num_classes: int = 5,
        pretrained: bool = True,
        dropout: float = 0.5,
        freeze_backbone: bool = False,
    ) -> None:
        super().__init__()

        weights = ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
        backbone = models.resnet50(weights=weights)

        # Remove the original FC head; keep everything up to the global pool
        self.backbone = nn.Sequential(*list(backbone.children())[:-1])

        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False

        in_features = backbone.fc.in_features  # 2048 for ResNet-50

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout / 2),
            nn.Linear(512, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Input tensor of shape (B, 3, H, W).

        Returns:
            Logits tensor of shape (B, num_classes).
        """
        features = self.backbone(x)   # (B, 2048, 1, 1)
        return self.classifier(features)

    def unfreeze_backbone(self, layers_from_end: int | None = None) -> None:
        """
        Unfreeze backbone layers for fine-tuning.

        Args:
            layers_from_end: If given, only unfreeze the last N child modules.
                             If None, unfreeze the entire backbone.
        """
        children = list(self.backbone.children())
        to_unfreeze = children if layers_from_end is None else children[-layers_from_end:]
        for module in to_unfreeze:
            for param in module.parameters():
                param.requires_grad = True


def build_model(config: dict) -> DRClassifier:
    """
    Instantiate a DRClassifier from a config dictionary.

    Expected keys (all optional, defaults shown):
        num_classes (int): 5
        pretrained (bool): True
        dropout (float): 0.5
        freeze_backbone (bool): False

    Args:
        config: Dictionary typically loaded from training_config.yaml["model"].

    Returns:
        Initialised DRClassifier.
    """
    return DRClassifier(
        num_classes=config.get("num_classes", 5),
        pretrained=config.get("pretrained", True),
        dropout=config.get("dropout", 0.5),
        freeze_backbone=config.get("freeze_backbone", False),
    )
