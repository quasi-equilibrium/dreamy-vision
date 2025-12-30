"""
Dreamy Vision - Configuration
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"

# Model configuration
SD_MODEL_ID = "runwayml/stable-diffusion-v1-5"
CONTROLNET_MODEL_ID = "lllyasviel/sd-controlnet-canny"

# Image processing
MAX_IMAGE_SIZE = 512  # Max dimension, maintains aspect ratio
TARGET_SIZE = 512     # For SD 1.5

# Enhancement settings
DEFAULT_DENOISING_STRENGTH = 0.12  # Very subtle - enhance pattern, don't regenerate
MIN_DENOISING_STRENGTH = 0.10
MAX_DENOISING_STRENGTH = 0.18

# Device
# Note: MPS has limited support, so we use CPU for stability
# Set PYTORCH_ENABLE_MPS_FALLBACK=1 if you want to try MPS with CPU fallback
DEVICE = "cpu"  # Default to CPU for stability
try:
    import torch
    import os
    
    # Check if MPS fallback is enabled
    if os.getenv("PYTORCH_ENABLE_MPS_FALLBACK") == "1":
        try:
            if torch.backends.mps.is_available():
                DEVICE = "mps"
                print("Using MPS with CPU fallback (PYTORCH_ENABLE_MPS_FALLBACK=1)")
        except Exception:
            # MPS check failed, use CPU
            DEVICE = "cpu"
    elif torch.cuda.is_available():
        DEVICE = "cuda"
    # Otherwise use CPU (default)
except ImportError:
    # Torch not available, use CPU
    DEVICE = "cpu"
except Exception as e:
    # Any other error, use CPU for safety
    print(f"Warning: Could not determine device, using CPU: {e}")
    DEVICE = "cpu"

# Generation settings
NUM_INFERENCE_STEPS = 30  # More steps for better quality
GUIDANCE_SCALE = 8.5  # Higher to better follow text description

