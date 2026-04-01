# V3 exports (kept for backward compatibility — exp2–exp6 still use these)
from .pipeline import PreprocessingPipeline
from .fov import standardize_fov
from .green_channel import extract_green_channel
from .normalization import normalize_pixels
from .clahe import apply_clahe, apply_clahe_sweep
from .hsv_enhancement import enhance_hsv

# V4 exports
from .pipeline_v4 import PreprocessingPipelineV4
from .config import PreprocessingV4Config, PIPELINE_PRESETS
from .canonical_orientation import detect_eye_side, canonical_flip, canonical_orientation
from .crop_resize import crop_and_resize
from .flat_field import apply_flat_field
from .upgraded_clahe import apply_upgraded_clahe, maybe_apply_clahe, ClaheParams
from .imagenet_normalize import imagenet_normalize
from .od_fovea_detect import ODFoveaResult, detect_od_fovea, rotate_to_horizontal

__all__ = [
    # V3
    "PreprocessingPipeline",
    "standardize_fov",
    "extract_green_channel",
    "normalize_pixels",
    "apply_clahe",
    "apply_clahe_sweep",
    "enhance_hsv",
    # V4
    "PreprocessingPipelineV4",
    "PreprocessingV4Config",
    "PIPELINE_PRESETS",
    "detect_eye_side",
    "canonical_flip",
    "canonical_orientation",
    "ODFoveaResult",
    "detect_od_fovea",
    "rotate_to_horizontal",
    "crop_and_resize",
    "apply_flat_field",
    "apply_upgraded_clahe",
    "maybe_apply_clahe",
    "ClaheParams",
    "imagenet_normalize",
]
