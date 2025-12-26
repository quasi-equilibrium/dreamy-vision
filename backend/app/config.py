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
DEFAULT_DENOISING_STRENGTH = 0.3
MIN_DENOISING_STRENGTH = 0.2
MAX_DENOISING_STRENGTH = 0.4

# Device
DEVICE = "mps" if hasattr(__import__('torch').cuda, 'is_available') else "cpu"
# For M2 Max, use MPS (Metal Performance Shaders)
try:
    import torch
    if torch.backends.mps.is_available():
        DEVICE = "mps"
    elif torch.cuda.is_available():
        DEVICE = "cuda"
    else:
        DEVICE = "cpu"
except:
    DEVICE = "cpu"

# Generation settings
NUM_INFERENCE_STEPS = 20
GUIDANCE_SCALE = 7.5

