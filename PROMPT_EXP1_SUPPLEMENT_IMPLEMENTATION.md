# Implementation Prompt: Experiment 1 Supplement — Focal Loss + Mask-Aware Resize

**Status:** APPROVED FOR IMPLEMENTATION  
**Scope:** Two modifications to `dr-classifier` — applied sequentially as Stage A then Stage B  
**Governance:** Protocol revision to RESEARCH_ARCHITECTURE and INVARIANTS required after both stages complete  
**Re-run requirement:** Full re-run of ALL Exp1 configs (A–F), ALL folds after implementation

---

## Pre-Implementation Checklist

Before touching any code:

1. `cd` into the `dr-classifier` repo root
2. `git checkout -b exp1-supplement-focal-loss-mask` (new branch)
3. `conda activate dr-classifier`
4. Verify existing smoke test passes: `python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs A`
5. Back up current Exp1 results: `cp -r outputs/exp1 backup_exp1_pre_supplement_$(date +%Y%m%d)`

---

## STAGE A: Focal Loss (Replacing Weighted CrossEntropy)

This is the simpler, self-contained change. Do it first.

### A1. Modify `src/training/losses.py`

**What exists now:**  
- `compute_class_weights(labels, num_classes, method)` → returns `torch.Tensor` of shape `(num_classes,)` with inverse-frequency weights normalized so they sum to `num_classes`
- `create_weighted_loss(class_weights, device)` → returns `nn.CrossEntropyLoss(weight=class_weights)`

**What to do:**

Keep `compute_class_weights()` **exactly as-is** — do not modify it at all. Its output will be reused as the α weights for Focal Loss.

Add a new class `FocalLoss(nn.Module)` **above** `create_weighted_loss`. Implementation:

```python
class FocalLoss(nn.Module):
    """Focal Loss for multi-class classification (Lin et al., 2017).

    Reduces the relative loss for well-classified examples (p_t > 0.5),
    focusing training on hard, misclassified examples.

    FL(p_t) = -α_t · (1 - p_t)^γ · log(p_t)

    Args:
        alpha: Per-class balance weights of shape (num_classes,).
            Typically inverse-frequency weights from compute_class_weights().
            Registered as a buffer (moves with .to(device) automatically).
        gamma: Focusing parameter. γ=0 recovers standard CE.
            γ=2 is the standard value from the original paper.
    """

    def __init__(self, alpha: torch.Tensor, gamma: float = 2.0) -> None:
        super().__init__()
        self.register_buffer("alpha", alpha)
        self.gamma = gamma

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Compute focal loss.

        Args:
            logits: Raw model output of shape (batch_size, num_classes).
            targets: Ground truth class indices of shape (batch_size,).

        Returns:
            Scalar loss tensor (mean over batch).
        """
        ce_loss = F.cross_entropy(logits, targets, reduction="none")
        p_t = torch.exp(-ce_loss)
        alpha_t = self.alpha[targets]
        focal_weight = alpha_t * (1.0 - p_t) ** self.gamma
        return (focal_weight * ce_loss).mean()
```

Add import at the top of the file:
```python
import torch.nn.functional as F
```

Now **modify** `create_weighted_loss` — rename it to `create_loss` and add a `loss_type` parameter:

```python
def create_loss(
    class_weights: torch.Tensor | None = None,
    device: str = "cpu",
    loss_type: str = "focal",
    gamma: float = 2.0,
) -> nn.Module:
    """Build the training loss function.

    Args:
        class_weights: Tensor of shape (num_classes,) from compute_class_weights(),
                       or None for unweighted loss.
        device: Device string to move weights to (e.g. "cuda" or "cpu").
        loss_type: "focal" (default) for FocalLoss, "ce" for weighted CrossEntropyLoss.
        gamma: Focusing parameter for Focal Loss. Ignored when loss_type="ce".

    Returns:
        Configured loss module (FocalLoss or nn.CrossEntropyLoss).
    """
    if class_weights is not None:
        class_weights = class_weights.to(device)

    if loss_type == "focal":
        if class_weights is None:
            raise ValueError("FocalLoss requires class_weights (alpha). Pass class_weights.")
        return FocalLoss(alpha=class_weights, gamma=gamma)
    elif loss_type == "ce":
        return nn.CrossEntropyLoss(weight=class_weights)
    else:
        raise ValueError(f"Unknown loss_type '{loss_type}'. Use 'focal' or 'ce'.")
```

Also keep a backward-compatible alias so nothing breaks silently:
```python
# Backward-compatible alias
create_weighted_loss = create_loss
```

### A2. Modify `configs/default.yaml`

Add two new keys under the `training:` section, **after** the existing `class_weights: inverse_frequency` line:

```yaml
training:
  # ... existing keys ...
  class_weights:      inverse_frequency
  loss_type:          focal           # "focal" or "ce"
  focal_gamma:        2.0             # focusing parameter (ignored if loss_type=ce)
```

### A3. Modify `src/training/trainer.py`

**Import change** (line 19): Update the import:
```python
from src.training.losses import compute_class_weights, create_loss
```

**Constructor change** (inside `__init__`, around lines 50-51): Add two new attributes after `self.use_class_weights`:
```python
self.use_class_weights: bool = tc.get("class_weights") == "inverse_frequency"
self.loss_type: str = tc.get("loss_type", "focal")
self.focal_gamma: float = tc.get("focal_gamma", 2.0)
```

**Loss creation change** (inside `train_fold`, lines 214-218): Replace:
```python
criterion = create_weighted_loss(weights, device=str(self.device))
```
with:
```python
criterion = create_loss(
    class_weights=weights,
    device=str(self.device),
    loss_type=self.loss_type,
    gamma=self.focal_gamma,
)
```

### A4. Modify `src/training/patient_trainer.py`

Apply the **identical** changes as A3:

1. **Import**: Change `create_weighted_loss` → `create_loss`
2. **Constructor**: Add `self.loss_type` and `self.focal_gamma` attributes (same pattern as trainer.py)
3. **Loss creation** (around line 320-323): Replace `create_weighted_loss(weights, ...)` with `create_loss(weights, ..., loss_type=self.loss_type, gamma=self.focal_gamma)`

### A5. Modify `configs/smoke_test_1pct.yaml`

Add the same two keys so smoke tests also exercise Focal Loss:
```yaml
training:
  # ... existing keys ...
  loss_type:     focal
  focal_gamma:   2.0
```

### A6. Smoke Test Stage A

Run and verify:
```bash
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs A
```

**Expected:** Training runs without errors. Loss values should be **smaller in magnitude** than with weighted CE (Focal Loss down-weights easy examples). No NaN, no crash. The loss at epoch 0 will likely be lower than it was with weighted CE because high-confidence samples contribute much less.

Then also test with EfficientNet:
```bash
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs C
```

**Expected:** Same — no crash, no NaN. Mixed precision is auto-disabled for EfficientNet.

**Checkpoint:** After A6 passes, commit:
```bash
git add -A && git commit -m "feat: replace weighted CE with Focal Loss (γ=2, α=inverse-freq)"
```

---

## STAGE B: Mask-Aware Isotropic Resize (Option 1 — Mask for ALL Configs)

This is the more invasive change. It modifies preprocessing (Stage 1), model input channels (3→4), and the normalization stage.

**Design decision: Option 1** — all configs (A–D, including baseline) get the 4-channel mask input. This keeps the preprocessing factor clean: the only difference between baseline and full V4 is the V4 stages (flat-field, CLAHE, etc.), NOT the mask channel. The mask channel is universal infrastructure.

### B1. Modify `src/preprocessing/crop_resize.py`

**What exists now:**  
- `detect_fov_bbox(image)` → returns bounding box or None  
- `crop_and_resize(image, target_size)` → returns `(target_size, target_size, 3)` uint8 array

**What to do:**

Keep `detect_fov_bbox()` **exactly as-is**.

Add a new function `detect_is_cropped(image)` that implements the three concordant checks from the proposal. Place it **after** `detect_fov_bbox` and **before** `crop_and_resize`:

```python
def detect_is_cropped(image: np.ndarray) -> bool:
    """Detect whether the fundus circle is cropped by the camera frame.

    Uses three concordant checks:
    1. Circle fit test — max inscribed circle extends beyond image bounds.
    2. Border touch test — foreground mask touches image edges.
    3. Arc coverage test — contour arc length < 90% of expected circumference.

    Final decision: is_cropped = (not fits) OR touches_border OR (coverage < 0.9).

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).

    Returns:
        True if the fundus circle appears cropped.
    """
    import cv2

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Threshold to separate fundus from background
    _, binary = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

    h, w = binary.shape

    # Check 1: Circle fit test via distance transform
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    _, max_r, _, max_loc = cv2.minMaxLoc(dist)
    cx, cy = max_loc
    margin = 2
    fits = (cx - max_r >= -margin and cx + max_r <= w + margin and
            cy - max_r >= -margin and cy + max_r <= h + margin)

    # Check 2: Border touch test
    touches_border = (
        binary[0, :].any() or           # top row
        binary[-1, :].any() or          # bottom row
        binary[:, 0].any() or           # left column
        binary[:, -1].any()             # right column
    )

    # Check 3: Arc coverage test
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    coverage = 1.0  # default: assume full circle
    if contours and max_r > 10:
        largest = max(contours, key=cv2.contourArea)
        arc_length = cv2.arcLength(largest, closed=False)
        expected_circumference = 2.0 * np.pi * max_r
        coverage = arc_length / expected_circumference if expected_circumference > 0 else 1.0

    return (not fits) or touches_border or (coverage < 0.9)
```

Add import at the top:
```python
import cv2
```
(Note: `cv2` is not currently imported in `crop_resize.py` — only `numpy` and `PIL` are used. Add it.)

Now **replace** the existing `crop_and_resize` function with a new version that returns both the image AND a binary mask:

```python
def crop_and_resize(
    image: np.ndarray,
    target_size: int = 512,
) -> tuple[np.ndarray, np.ndarray]:
    """Crop to the FOV region and resize to target_size × target_size.

    Uses isotropic scaling with centered padding to preserve the fundus
    circle geometry. Returns a binary mask indicating real pixel data
    (1.0) vs padding (0.0).

    FOV detection is attempted first; if it fails (non-landscape image or
    bounding box too small) a center-square crop is used as fallback.

    Args:
        image: RGB uint8 NumPy array of shape (H, W, 3).
        target_size: Output spatial resolution in pixels (square).

    Returns:
        Tuple of:
          - image: RGB uint8 NumPy array of shape (target_size, target_size, 3).
          - mask: float32 NumPy array of shape (target_size, target_size)
                  with 1.0 where real data exists and 0.0 for padding.
    """
    pil_img = Image.fromarray(image)
    w, h = pil_img.size  # PIL: (width, height)

    bbox = detect_fov_bbox(pil_img)

    if bbox is None:
        # Fallback: center-square crop
        left = max((w - h) // 2, 0)
        upper = 0
        right = min(w - (w - h) // 2, w)
        lower = h
        bbox = (left, upper, right, lower)

    cropped = pil_img.crop(bbox)
    crop_w, crop_h = cropped.size

    # Isotropic resize: scale to fit within target_size, then pad
    scale = target_size / max(crop_h, crop_w)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    resized_arr = np.array(resized, dtype=np.uint8)

    # Create canvas with zero padding
    canvas = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    y_off = (target_size - new_h) // 2
    x_off = (target_size - new_w) // 2
    canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized_arr

    # Binary mask: 1.0 where real data, 0.0 where padding
    mask = np.zeros((target_size, target_size), dtype=np.float32)
    mask[y_off : y_off + new_h, x_off : x_off + new_w] = 1.0

    return canvas, mask
```

**CRITICAL:** The return type has changed from `np.ndarray` to `tuple[np.ndarray, np.ndarray]`. Every caller of `crop_and_resize` must be updated.

### B2. Modify `src/preprocessing/pipeline_v4.py`

**What exists now:**  
- `__call__` takes `(image, eye_side)` → returns `torch.Tensor` of shape `(3, H, W)`
- Stage 1 call: `image = crop_and_resize(image, self.config.target_size)`

**What to do:**

In the `__call__` method, update Stage 1 to capture the mask:

```python
# Stage 1: FOV crop + resize (always) — returns (image, mask)
image, fov_mask = crop_and_resize(image, self.config.target_size)
```

Then, at the end of `__call__`, after ImageNet normalization produces the 3-channel tensor, append the mask as a 4th channel:

Replace the final return block:
```python
# Stage 4: ImageNet normalize → tensor (always last)
rgb_tensor = imagenet_normalize(
    image,
    mean=self.config.normalize_mean,
    std=self.config.normalize_std,
)

# Append FOV mask as 4th channel
mask_tensor = torch.from_numpy(fov_mask).unsqueeze(0)  # (1, H, W)
return torch.cat([rgb_tensor, mask_tensor], dim=0)      # (4, H, W)
```

**Update the docstrings:**
- `__call__` return type: change `(3, target_size, target_size)` → `(4, target_size, target_size)` everywhere in the docstring
- Add note: "Channel 3 is a binary FOV mask (1.0 = real data, 0.0 = padding)."

Also update the `fov_mask` variable through the intermediate stages. The mask is generated at Stage 1 and must survive through Stages 2, 3, 5 without modification (those stages only operate on the RGB image). The `fov_mask` variable just needs to be in scope when the final `torch.cat` runs — no other stage touches it. Verify this is the case (it is, since it's assigned before the other stages and not overwritten).

### B3. Modify `src/preprocessing/imagenet_normalize.py`

No changes needed. `imagenet_normalize` operates on the 3-channel RGB image. The mask is appended AFTER normalization. The function signature and behavior stay identical.

### B4. Modify `src/models/resnet.py`

**What exists now:**  
- `create_resnet50()` → builds a `torchvision.models.resnet50` with a replaced `fc` layer
- The first conv layer is `model.conv1` which is `Conv2d(3, 64, kernel_size=7, stride=2, padding=3)`

**What to do:**

Add a step after loading the model to replace `conv1` with a 4-channel version:

```python
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
```

Add import at the top:
```python
import torch
```

### B5. Modify `src/models/efficientnet.py`

**What exists now:**  
- `create_efficientnet(variant, ...)` → builds a `timm` EfficientNet with replaced `classifier`
- The first conv is `model.conv_stem` which is `Conv2d(3, 40, kernel_size=3, stride=2, padding=1)` for B3

**What to do:**

```python
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
```

Add imports at the top:
```python
import torch
import torch.nn as nn
```
(`nn` is already imported; add `torch` if not present.)

### B6. Modify `src/models/factory.py`

**What exists now:**  
- `create_model(model_name, config)` passes `pretrained`, `num_classes`, `dropout`, `freeze_base` to the model constructors
- `create_patient_model(model_name, config)` wraps `create_model`

**What to do:**

Add `in_channels` passthrough:

```python
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
            - in_channels (int): Input channels. Default: 4.

    Returns:
        Configured nn.Module ready for training.

    Raises:
        ValueError: If model_name is not recognised.
    """
    pretrained: bool = config.get("pretrained", True)
    num_classes: int = config.get("num_classes", 5)
    dropout: float = config.get("dropout", 0.4)
    freeze_base: bool = config.get("freeze_base", False)
    in_channels: int = config.get("in_channels", 4)

    if model_name == "resnet50":
        return create_resnet50(
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_base=freeze_base,
            in_channels=in_channels,
        )
    elif model_name in _EFFICIENTNET_VARIANTS:
        variant = model_name.split("_")[1]
        return create_efficientnet(
            variant=variant,
            num_classes=num_classes,
            pretrained=pretrained,
            dropout=dropout,
            freeze_base=freeze_base,
            in_channels=in_channels,
        )
    else:
        raise ValueError(
            f"Unknown model '{model_name}'. "
            f"Supported: resnet50, efficientnet_b0, efficientnet_b3, efficientnet_b4."
        )
```

### B7. Modify `configs/default.yaml`

Add `in_channels: 4` to **every** model section:

```yaml
models:
  resnet50:
    pretrained:    true
    num_classes:   5
    dropout:       0.4
    in_channels:   4
  efficientnet_b0:
    pretrained:    true
    num_classes:   5
    dropout:       0.4
    in_channels:   4
  efficientnet_b3:
    pretrained:    true
    num_classes:   5
    dropout:       0.4
    in_channels:   4
  efficientnet_b4:
    pretrained:    true
    num_classes:   5
    dropout:       0.4
    in_channels:   4
```

Also add to `configs/smoke_test_1pct.yaml` the same `in_channels: 4` entries.

### B8. Modify `src/data/datasets.py` — `BaseFundusDataset.__getitem__`

**What exists now (line 82):**
```python
tensor = torch.from_numpy(np.ascontiguousarray(image.transpose(2, 0, 1)))
```

This assumes 3 channels. After Stage B, the V4 pipeline returns 4-channel tensors directly, so `BaseFundusDataset` only needs a guard for the legacy V3 path. Check: the `EyePACSDataset.__getitem__` (lines 133-173) already handles V4 separately — when `preprocessing` is a `PreprocessingPipelineV4`, it returns the tensor directly at line 155. The legacy path at line 169 (`image.transpose(2, 0, 1)`) is only hit for V3 pipeline. **No change needed here** — V3 experiments (Exp2–6) use 3-channel images and the V3 pipeline, which is unaffected.

However, **verify** that the `EyePACSPatientPairDataset` (used by configs E/F) also routes through the V4 pipeline correctly. Search for its `__getitem__` and confirm it returns `self.preprocessing(image, eye_side=...)` directly when using V4. If it does, no change needed.

### B9. Verify Other Callers of `crop_and_resize`

Search the entire codebase for any other call to `crop_and_resize`:

```bash
grep -rn "crop_and_resize" src/ scripts/ tests/
```

**Expected callers:**
1. `src/preprocessing/pipeline_v4.py` — **already updated in B2**
2. `src/preprocessing/pipeline.py` (V3 legacy) — **this MUST be checked**
3. Any scripts (e.g., `smoke_test_v4.py`, `test_preprocessing.py`)

For **`src/preprocessing/pipeline.py` (V3 legacy)**:  
If the V3 pipeline calls `crop_and_resize`, you need to update it to unpack the tuple:
```python
image, _mask = crop_and_resize(image, target_size)
```
The V3 pipeline discards the mask since V3 experiments use 3-channel input.

For **any scripts** that call `crop_and_resize` directly: update them to unpack:
```python
image, mask = crop_and_resize(image, target_size)
# or if mask is not needed:
image, _ = crop_and_resize(image, target_size)
```

### B10. Verify Experiments 2–6 Are Not Broken

Experiments 2–6 use the V3 pipeline (`src/preprocessing/pipeline.py`) or the V4 pipeline in specific ways. After B9, run:

```bash
python run_experiment.py exp2 --config configs/smoke_test_1pct.yaml --fold 0
```

If Exp2 smoke test crashes, it's because `pipeline.py` wasn't updated for the new `crop_and_resize` return type (see B9).

### B11. Smoke Test Stage B

Run the full Exp1 smoke test:
```bash
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs A
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs C
python run_experiment.py exp1 --config configs/smoke_test_1pct.yaml --configs D
```

**Expected:**
- Model's first conv layer should accept 4-channel input without shape mismatch errors
- Tensor shapes in the training loop should be `(batch, 4, 512, 512)`
- Loss values are reasonable (no NaN, no explosion)
- EfficientNet still works with mixed precision disabled

**Verification command** — add a temporary print in `trainer.py`'s `train_one_epoch` to confirm tensor shape:
```python
# TEMPORARY — remove after verification
if total == 0:
    print(f"  [DEBUG] Input shape: {images.shape}")  # should print torch.Size([16, 4, 512, 512])
```

**Checkpoint:** After B11 passes, commit:
```bash
git add -A && git commit -m "feat: isotropic resize with centered padding + 4-channel mask input (all configs)"
```

---

## STAGE C: Governance Documentation Update

### C1. Update `CLAUDE.md`

In the "V4 Preprocessing Pipeline" section, update Stage 1 description:
```
Stage 1: FOV crop + isotropic resize + padding + mask generation — always
  - Isotropic scaling preserves fundus circle geometry
  - Centered padding fills unused canvas with zeros
  - Binary FOV mask (4th channel) marks real data (1.0) vs padding (0.0)
```

In the "Hardware Constraints" section, add:
```
- input_channels: 4 (RGB + FOV mask)
- loss_function: Focal Loss (γ=2, α=inverse-frequency class weights)
```

Update the "Commands" note if needed.

### C2. Update `docs/RESEARCH_ARCHITECTURE.md`

Add a "Protocol Revision" subsection documenting:
1. Loss function changed from weighted CrossEntropyLoss to Focal Loss (γ=2, α=inverse-frequency)
2. Image input changed from 3-channel RGB to 4-channel RGB+Mask
3. Resize strategy changed from direct resize to isotropic resize with centered padding
4. First conv layer of both architectures modified (channel 4 initialized with RGB weight mean)
5. All configs (A–F) use both changes — factorial design integrity preserved
6. Full re-run of all configs and all folds required

### C3. Update `docs/INVARIANTS.md`

Add or update the relevant invariants:
- Loss function invariant: "All Exp1 configs use FocalLoss(γ=2, α=inverse-frequency). No config uses plain CrossEntropyLoss."
- Input invariant: "All Exp1 configs receive 4-channel input (RGB + FOV mask). Channel 4 is a binary mask indicating real pixel data (1.0) vs padding (0.0)."

---

## STAGE D: Full Re-Run

### D1. Clear Previous Results

```bash
# Already backed up in pre-implementation checklist
rm -rf outputs/exp1/
```

### D2. Run All Configs

```bash
# Config A — baseline + ResNet-50
python run_experiment.py exp1 --config configs/default.yaml --configs A

# Config B — full V4 + ResNet-50
python run_experiment.py exp1 --config configs/default.yaml --configs B

# Config C — baseline + EfficientNet-B3
python run_experiment.py exp1 --config configs/default.yaml --configs C

# Config D — full V4 + EfficientNet-B3
python run_experiment.py exp1 --config configs/default.yaml --configs D
```

Each runs 3 folds × up to 20 epochs. Estimated time per config: ~2–4 hours on RTX 3060 (depends on early stopping).

### D3. Verify Results

After all 4 configs complete:
1. Check `outputs/exp1/summary.json` — does it contain all 4 configs?
2. Check dominance tests — B vs A and D vs C
3. Compare with pre-supplement results (in `backup_exp1_pre_supplement_*`)

---

## Summary of Files Modified

| File | Stage | Change |
|------|-------|--------|
| `src/training/losses.py` | A | Add `FocalLoss` class, rename `create_weighted_loss` → `create_loss` |
| `src/training/trainer.py` | A | Import `create_loss`, add `loss_type`/`focal_gamma` config, use new factory |
| `src/training/patient_trainer.py` | A | Same as trainer.py |
| `configs/default.yaml` | A+B | Add `loss_type`, `focal_gamma`, `in_channels` |
| `configs/smoke_test_1pct.yaml` | A+B | Same config additions |
| `src/preprocessing/crop_resize.py` | B | Add `detect_is_cropped`, rewrite `crop_and_resize` → isotropic + mask |
| `src/preprocessing/pipeline_v4.py` | B | Unpack mask from Stage 1, append as 4th channel after normalization |
| `src/preprocessing/pipeline.py` | B | Unpack mask from Stage 1, discard it (V3 stays 3-channel) |
| `src/models/resnet.py` | B | Add `in_channels` param, replace `conv1` for 4-channel input |
| `src/models/efficientnet.py` | B | Add `in_channels` param, replace `conv_stem` for 4-channel input |
| `src/models/factory.py` | B | Pass `in_channels` through to model constructors |
| `CLAUDE.md` | C | Update pipeline description and hardware constraints |
| `docs/RESEARCH_ARCHITECTURE.md` | C | Add protocol revision subsection |
| `docs/INVARIANTS.md` | C | Add loss function and input channel invariants |
| Any scripts calling `crop_and_resize` | B | Unpack `(image, mask)` tuple |

---

## Rollback Plan

If Stage B causes intractable issues (VRAM overflow from 4 channels, accuracy collapse, etc.):

1. Revert Stage B commits: `git revert HEAD~N` (where N = number of Stage B commits)
2. Keep Stage A (Focal Loss) — it's independent
3. Set `in_channels: 3` in configs
4. The `create_loss` function still works with `loss_type="focal"`
5. Re-run with Focal Loss only

If Focal Loss itself causes issues:
1. Set `loss_type: ce` in `configs/default.yaml`
2. Everything falls back to weighted CrossEntropyLoss
3. No code revert needed — the `create_loss` factory handles both
