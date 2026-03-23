"""V4 Pipeline Smoke Test — verifies end-to-end data flow."""

import pathlib
import sys

# Allow running from any directory (scripts/ or repo root)
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import torch

from src.preprocessing.config import PreprocessingV4Config, PIPELINE_PRESETS
from src.preprocessing.pipeline_v4 import PreprocessingPipelineV4
from src.preprocessing.canonical_flip import detect_eye_side, canonical_flip
from src.preprocessing.crop_resize import crop_and_resize
from src.preprocessing.flat_field import apply_flat_field
from src.preprocessing.upgraded_clahe import apply_upgraded_clahe, ClaheParams
from src.preprocessing.imagenet_normalize import imagenet_normalize
from src.data.augmentation_v4 import FundusAugmentationV4
from src.models.patient_model import DRPatientModel, Backbone
from src.models.factory import create_model, create_patient_model


def test_individual_stages() -> None:
    """Test each preprocessing stage individually."""
    print("Testing individual stages...")

    # Synthetic fundus image (landscape, like real fundus photos)
    img = np.random.randint(30, 220, (600, 800, 3), dtype=np.uint8)

    # Stage 0: Canonical flip
    flipped = canonical_flip(img, "left")
    assert flipped.shape == img.shape
    print("  Stage 0 (canonical flip): OK")

    # Stage 1: Crop + resize
    cropped = crop_and_resize(img, target_size=512)
    assert cropped.shape == (512, 512, 3)
    assert cropped.dtype == np.uint8
    print("  Stage 1 (crop+resize): OK")

    # Stage 2: Flat-field
    corrected = apply_flat_field(cropped, sigma=45.0)
    assert corrected.shape == (512, 512, 3)
    assert corrected.dtype == np.uint8
    print("  Stage 2 (flat-field): OK")

    # Stage 3: Upgraded CLAHE
    enhanced = apply_upgraded_clahe(corrected)
    assert enhanced.shape == (512, 512, 3)
    assert enhanced.dtype == np.uint8
    print("  Stage 3 (upgraded CLAHE): OK")

    # Stage 4: Normalize
    tensor = imagenet_normalize(enhanced)
    assert tensor.shape == (3, 512, 512)
    assert tensor.dtype == torch.float32
    print("  Stage 4 (normalize): OK")


def test_full_pipeline() -> None:
    """Test the full V4 pipeline."""
    print("\nTesting full pipeline...")

    img = np.random.randint(30, 220, (600, 800, 3), dtype=np.uint8)

    for preset in ["resnet", "efficientnet"]:
        config = PreprocessingV4Config.from_preset(preset)

        # Training mode
        pipe = PreprocessingPipelineV4.create_for_training(config)
        tensor = pipe(img, eye_side="left")
        assert tensor.shape == (3, 512, 512)

        # Inference mode
        pipe_inf = PreprocessingPipelineV4.create_for_inference(config)
        tensor_inf = pipe_inf(img, eye_side="right")
        assert tensor_inf.shape == (3, 512, 512)

        print(f"  Preset '{preset}': OK (train + inference)")

    # Baseline
    pipe_base = PreprocessingPipelineV4.create_baseline()
    tensor_base = pipe_base(img)
    assert tensor_base.shape == (3, 512, 512)
    print("  Baseline pipeline: OK")


def test_patient_model() -> None:
    """Test DRPatientModel forward pass."""
    print("\nTesting patient model...")

    for model_name in ["resnet50", "efficientnet_b3"]:
        config = {"pretrained": False, "num_classes": 5, "dropout": 0.4}
        model = create_patient_model(model_name, config)
        model.eval()

        B = 2
        img_L = torch.randn(B, 3, 224, 224)  # smaller for speed
        img_R = torch.randn(B, 3, 224, 224)

        with torch.no_grad():
            logits = model(img_L, img_R)
        assert logits.shape == (B, 5)

        # Test missing eye (zero tensor)
        img_R_zero = torch.zeros(B, 3, 224, 224)
        with torch.no_grad():
            logits2 = model(img_L, img_R_zero)
        assert logits2.shape == (B, 5)

        print(f"  {model_name}: OK")


def test_v3_backward_compat() -> None:
    """Verify V3 pipeline still works."""
    print("\nTesting V3 backward compatibility...")

    from src.preprocessing import PreprocessingPipeline

    p3 = PreprocessingPipeline.create_baseline()
    assert p3.is_absent()

    p3_full = PreprocessingPipeline.create_full()
    assert p3_full.is_active()

    from src.data.augmentation import FundusAugmentation
    aug = FundusAugmentation({"horizontal_flip": True})

    print("  V3 imports: OK")


if __name__ == "__main__":
    test_individual_stages()
    test_full_pipeline()
    test_patient_model()
    test_v3_backward_compat()
    print("\nAll V4 smoke tests passed!")
