"""Two-stage fine-tuning protocol for EfficientNet-B0.

Note: H-3 (Two-Stage Fine-Tuning hypothesis) was removed in V5.
These utilities remain available as training strategies but are not
tested as an independent hypothesis.
"""

import torch.nn as nn


def freeze_base_layers(model: nn.Module) -> None:
    """Freeze all model parameters except the classifier head.

    Stage 1 of the two-stage protocol: only the classifier is trained
    while the pretrained backbone is kept frozen.

    Args:
        model: A timm EfficientNet model whose classifier was replaced
               by create_efficientnet().
    """
    for param in model.parameters():
        param.requires_grad = False
    for param in model.classifier.parameters():
        param.requires_grad = True


def unfreeze_top_layers(model: nn.Module, num_blocks: int = 3) -> list[str]:
    """Unfreeze the top backbone layers for Stage 2 progressive fine-tuning.

    Unfreezes the last num_blocks EfficientNet blocks, conv_head, and bn2.
    The classifier remains trainable (already unfrozen from Stage 1).

    Args:
        model: A timm EfficientNet model (partially frozen from Stage 1).
        num_blocks: Number of tail blocks to unfreeze from model.blocks.
                    Default: 3 (blocks[-3:]).

    Returns:
        List of parameter names that were unfrozen by this call.
    """
    unfrozen_names: list[str] = []

    # Unfreeze last num_blocks from model.blocks
    total_blocks = len(model.blocks)
    for block_idx in range(max(0, total_blocks - num_blocks), total_blocks):
        for name, param in model.blocks[block_idx].named_parameters():
            param.requires_grad = True
            unfrozen_names.append(f"blocks.{block_idx}.{name}")

    # Unfreeze conv_head and bn2
    for name, param in model.conv_head.named_parameters():
        param.requires_grad = True
        unfrozen_names.append(f"conv_head.{name}")

    for name, param in model.bn2.named_parameters():
        param.requires_grad = True
        unfrozen_names.append(f"bn2.{name}")

    return unfrozen_names


def get_two_stage_param_groups(
    model: nn.Module,
    base_lr: float = 0.0001,
    classifier_lr: float = 0.001,
) -> list[dict]:
    """Build optimizer parameter groups for Stage 2 fine-tuning.

    Separates classifier parameters (higher lr) from unfrozen backbone
    parameters (lower lr) to prevent destroying pretrained features.

    Args:
        model: A timm EfficientNet model after unfreeze_top_layers() was called.
        base_lr: Learning rate for unfrozen backbone parameters. Default: 1e-4.
        classifier_lr: Learning rate for classifier head. Default: 1e-3.

    Returns:
        List of two optimizer param-group dicts, compatible with
        torch.optim.Adam([...]).
    """
    classifier_param_ids = {id(p) for p in model.classifier.parameters()}

    base_params = [
        p for p in model.parameters()
        if p.requires_grad and id(p) not in classifier_param_ids
    ]
    classifier_params = list(model.classifier.parameters())

    return [
        {"params": base_params,       "lr": base_lr},
        {"params": classifier_params, "lr": classifier_lr},
    ]
