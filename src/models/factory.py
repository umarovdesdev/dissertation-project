"""Model factory for DR classification experiments."""

import torch.nn as nn

from src.models.resnet import create_resnet50
from src.models.efficientnet import create_efficientnet
from src.models.patient_model import Backbone, DRPatientModel

_EFFICIENTNET_VARIANTS = {"efficientnet_b0", "efficientnet_b3", "efficientnet_b4"}


def create_model(model_name: str, config: dict) -> nn.Module:
    """Instantiate a model by name from a config dict.

    Args:
        model_name: One of "resnet50", "efficientnet_b0",
                    "efficientnet_b3", "efficientnet_b4".
        config: Dict with keys:
            - pretrained (bool): Load ImageNet weights.
            - num_classes (int): Number of output logits.
            - dropout (float): Dropout rate before final linear.
            - freeze_base (bool): Freeze backbone params.

    Returns:
        Configured nn.Module ready for training.

    Raises:
        ValueError: If model_name is not recognised.
    """
    pretrained: bool = config.get("pretrained", True)
    num_classes: int = config.get("num_classes", 5)
    dropout: float = config.get("dropout", 0.4)
    freeze_base: bool = config.get("freeze_base", False)

    if model_name == "resnet50":
        return create_resnet50(
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_base=freeze_base,
        )
    elif model_name in _EFFICIENTNET_VARIANTS:
        variant = model_name.split("_")[1]  # "b0", "b3", or "b4"
        return create_efficientnet(
            variant=variant,
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_base=freeze_base,
        )
    else:
        raise ValueError(
            f"Unknown model '{model_name}'. "
            f"Supported: resnet50, efficientnet_b0, efficientnet_b3, efficientnet_b4."
        )


def create_patient_model(
    model_name: str,
    config: dict,
) -> DRPatientModel:
    """
    Create a :class:`~src.models.patient_model.DRPatientModel` with a shared backbone.

    Builds a standard single-image classification model via :func:`create_model`,
    strips its classifier head into a :class:`~src.models.patient_model.Backbone`,
    and wraps it with a :class:`~src.models.patient_model.PatientHead` for
    binocular fusion.

    Args:
        model_name: One of ``"resnet50"``, ``"efficientnet_b0"``,
            ``"efficientnet_b3"``, ``"efficientnet_b4"``.
        config: Dict with keys ``pretrained`` (bool), ``num_classes`` (int),
            ``dropout`` (float).

    Returns:
        :class:`~src.models.patient_model.DRPatientModel` instance.
    """
    base = create_model(model_name, config)
    backbone = Backbone(base, model_name)
    return DRPatientModel(
        backbone,
        num_classes=config.get("num_classes", 5),
        head_dropout=config.get("dropout", 0.3),
    )
