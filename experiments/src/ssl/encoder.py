"""SSL encoder construction — factory-matched 4-channel trunks.

The SSL encoder MUST be the *same* backbone the supervised classifier uses, so
the pretrained weights drop straight into ``create_resnet50(in_channels=4)`` /
``create_efficientnet("b3", in_channels=4)`` with no architectural change (brief
§7). This module reuses the existing model factory and merely strips the
classification head, exposing the global-average-pooled feature vector that the
SSL projector/predictor attach to.
"""

from __future__ import annotations

import torch.nn as nn

from src.models.factory import create_model

# Backbones whose trunk head lives at ``model.classifier`` (timm EfficientNet)
# vs ``model.fc`` (torchvision ResNet). Mirrors src/models/factory.py.
_EFFICIENTNET_BACKBONES = {"efficientnet_b0", "efficientnet_b3", "efficientnet_b4"}
_RESNET_BACKBONES = {"resnet50"}

SUPPORTED_BACKBONES = _RESNET_BACKBONES | _EFFICIENTNET_BACKBONES


def build_ssl_encoder(
    backbone_name: str,
    in_channels: int = 4,
    pretrained: bool = False,
) -> tuple[nn.Module, int]:
    """Build a head-stripped backbone trunk for SSL pretraining or probing.

    Constructs the backbone via the shared model factory (so the 4-channel
    ``conv1`` / ``conv_stem`` replacement logic and trunk are byte-identical to
    the supervised model), then replaces the classification head with
    :class:`~torch.nn.Identity`. The returned module's ``forward`` therefore
    yields the pooled feature vector (2048-d for ResNet-50, ``feat_dim``-d for
    EfficientNet-B3).

    The trunk's ``state_dict`` keys match the factory model's trunk keys exactly,
    **excluding** the head — this is what :func:`save_ssl_checkpoint` stores and
    :func:`load_ssl_backbone` strict-loads back into a fresh-headed Exp-1 model.

    Args:
        backbone_name: One of ``"resnet50"``, ``"efficientnet_b0"``,
            ``"efficientnet_b3"``, ``"efficientnet_b4"``.
        in_channels: Input channel count. Default ``4`` (RGB + FOV mask).
        pretrained: If ``True``, start from ImageNet weights (the §11
            continual-SSL fallback / probe ImageNet baseline). Default ``False``
            (from-scratch random init, the locked default — INV-SSL-6).

    Returns:
        Tuple ``(trunk, feature_dim)`` where ``trunk`` is an ``nn.Module``
        producing ``(N, feature_dim)`` pooled features.

    Raises:
        ValueError: If ``backbone_name`` is not a supported CNN backbone.
    """
    if backbone_name not in SUPPORTED_BACKBONES:
        raise ValueError(
            f"Unsupported SSL backbone '{backbone_name}'. "
            f"Supported: {sorted(SUPPORTED_BACKBONES)}."
        )

    # dropout is irrelevant once the head is stripped; num_classes only sizes the
    # head we discard. Build with the requested pretrained / in_channels.
    model = create_model(
        backbone_name,
        {
            "pretrained": pretrained,
            "num_classes": 5,
            "dropout": 0.0,
            "in_channels": in_channels,
        },
    )

    if backbone_name in _RESNET_BACKBONES:
        # factory sets model.fc = Sequential(Dropout, Linear(2048, num_classes))
        feature_dim = int(model.fc[1].in_features)
        model.fc = nn.Identity()
    else:
        # factory sets model.classifier = Sequential(Dropout, Linear(feat_dim, n))
        feature_dim = int(model.classifier[1].in_features)
        model.classifier = nn.Identity()

    return model, feature_dim
