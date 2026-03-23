"""
Per-patient binocular DR classification model.

Architecture:

    img_L → Backbone → feat_L ─┐
                                  ├→ PatientHead → logits
    img_R → Backbone → feat_R ─┘

A single shared backbone processes each eye independently; the PatientHead
fuses the two feature vectors via concatenation + absolute difference and
maps them to class logits through a small MLP.

Zero tensors (all-zeros input) are passed for missing eyes — the backbone
still produces a valid (all-zero-like) feature vector, so the forward pass
never raises.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class Backbone(nn.Module):
    """
    Shared feature extractor — CNN with the final classifier head removed.

    Supports ResNet-50 (``model.fc``) and EfficientNet (``model.classifier``)
    as created by :func:`~src.models.resnet.create_resnet50` and
    :func:`~src.models.efficientnet.create_efficientnet`.  The head is
    replaced by :class:`~torch.nn.Identity` so the model returns a flat
    feature vector of shape ``(B, feat_dim)``.

    Args:
        base_model: Full classification model (with head).
        model_type: One of ``"resnet50"``, ``"efficientnet_b0"``,
            ``"efficientnet_b3"``, ``"efficientnet_b4"``.
    """

    def __init__(self, base_model: nn.Module, model_type: str) -> None:
        super().__init__()
        self.model_type = model_type

        if "resnet" in model_type:
            # fc = nn.Sequential(Dropout, Linear(2048, num_classes))
            self._feat_dim: int = (
                base_model.fc[1].in_features
                if isinstance(base_model.fc, nn.Sequential)
                else base_model.fc.in_features
            )
            base_model.fc = nn.Identity()
        elif "efficientnet" in model_type:
            # classifier = nn.Sequential(Dropout, Linear(in_features, num_classes))
            self._feat_dim = (
                base_model.classifier[1].in_features
                if isinstance(base_model.classifier, nn.Sequential)
                else base_model.classifier.in_features
            )
            base_model.classifier = nn.Identity()
        else:
            raise ValueError(
                f"Unsupported model_type '{model_type}'. "
                "Expected 'resnet50' or 'efficientnet_b*'."
            )

        self.model = base_model

    @property
    def feat_dim(self) -> int:
        """Dimensionality of the feature vector produced by this backbone."""
        return self._feat_dim

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Extract features from an image batch.

        Args:
            x: Float32 tensor of shape ``(B, 3, H, W)``.

        Returns:
            Feature tensor of shape ``(B, feat_dim)``.
        """
        return self.model(x)


class PatientHead(nn.Module):
    """
    Binocular fusion head: concat + |diff| → MLP → logits.

    Input dimension: ``feat_dim * 3``  (left ‖ right ‖ |left − right|).

    Args:
        feat_dim: Feature dimension from the backbone.
        num_classes: Number of output classes (default 5, DR grades 0–4).
        dropout: Dropout rate inside the MLP (default 0.3).
    """

    def __init__(
        self,
        feat_dim: int,
        num_classes: int = 5,
        dropout: float = 0.3,
    ) -> None:
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(feat_dim * 3, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, feat_L: torch.Tensor, feat_R: torch.Tensor) -> torch.Tensor:
        """
        Fuse left and right eye features and produce class logits.

        Args:
            feat_L: Left-eye feature tensor of shape ``(B, feat_dim)``.
            feat_R: Right-eye feature tensor of shape ``(B, feat_dim)``.

        Returns:
            Logit tensor of shape ``(B, num_classes)``.
        """
        x = torch.cat([feat_L, feat_R, torch.abs(feat_L - feat_R)], dim=1)
        return self.mlp(x)


class DRPatientModel(nn.Module):
    """
    Full per-patient DR classification model with shared backbone.

    Both eyes are processed by the same :class:`Backbone` instance (shared
    weights).  The :class:`PatientHead` fuses the resulting feature pairs.

    Args:
        backbone: :class:`Backbone` instance used for both eyes.
        num_classes: Number of output classes (default 5).
        head_dropout: Dropout rate for the :class:`PatientHead` MLP.
    """

    def __init__(
        self,
        backbone: Backbone,
        num_classes: int = 5,
        head_dropout: float = 0.3,
    ) -> None:
        super().__init__()
        self.backbone = backbone
        self.head = PatientHead(backbone.feat_dim, num_classes, head_dropout)

    def forward(
        self,
        img_L: torch.Tensor,
        img_R: torch.Tensor,
    ) -> torch.Tensor:
        """
        Forward pass for a patient image pair.

        Args:
            img_L: Left-eye tensor of shape ``(B, 3, H, W)``.
                Use a zero tensor for a missing eye.
            img_R: Right-eye tensor of shape ``(B, 3, H, W)``.
                Use a zero tensor for a missing eye.

        Returns:
            Logit tensor of shape ``(B, num_classes)``.
        """
        feat_L = self.backbone(img_L)
        feat_R = self.backbone(img_R)
        return self.head(feat_L, feat_R)
