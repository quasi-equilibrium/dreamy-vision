#!/usr/bin/env python3
"""
Pre-download Stable Diffusion models
This will download ~5.5GB of models to avoid delay on first use
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(__file__))

from app.config import SD_MODEL_ID, CONTROLNET_MODEL_ID
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
import torch

print("=" * 60)
print("Downloading Stable Diffusion Models")
print("=" * 60)
print(f"Stable Diffusion: {SD_MODEL_ID}")
print(f"ControlNet: {CONTROLNET_MODEL_ID}")
print(f"Total size: ~5.5GB")
print("=" * 60)
print()

# Check device
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Device: {device}")
print()

# Download ControlNet first
print("Step 1/2: Downloading ControlNet model...")
print("This may take 5-10 minutes...")
try:
    controlnet = ControlNetModel.from_pretrained(
        CONTROLNET_MODEL_ID,
        torch_dtype=torch.float32 if device == "mps" else torch.float16
    )
    print("✅ ControlNet downloaded!")
except Exception as e:
    print(f"❌ Error downloading ControlNet: {e}")
    sys.exit(1)

print()

# Download Stable Diffusion
print("Step 2/2: Downloading Stable Diffusion model...")
print("This may take 10-20 minutes...")
try:
    pipeline = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
        SD_MODEL_ID,
        controlnet=controlnet,
        torch_dtype=torch.float32 if device == "mps" else torch.float16,
        safety_checker=None,
        requires_safety_checker=False
    )
    print("✅ Stable Diffusion downloaded!")
except Exception as e:
    print(f"❌ Error downloading Stable Diffusion: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ All models downloaded successfully!")
print("=" * 60)
print()
print("Models are stored in: ~/.cache/huggingface/hub/")
print("You can check the size with: du -sh ~/.cache/huggingface/hub/")
print()

