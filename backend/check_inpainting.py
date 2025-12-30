#!/usr/bin/env python3
"""
Check if inpainting is set up correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models.enhancer import ImageEnhancer

print("=" * 60)
print("Checking Inpainting Setup")
print("=" * 60)
print()

# Check if inpainting is enabled by default
enhancer = ImageEnhancer()

print("1. Inpainting enabled:", enhancer.use_inpainting)
print()

print("2. Pipelines loaded:")
if enhancer.pipeline:
    print(f"   ✅ Img2Img pipeline: {type(enhancer.pipeline).__name__}")
else:
    print("   ❌ Img2Img pipeline: Not loaded")

if enhancer.inpaint_pipeline:
    print(f"   ✅ Inpaint pipeline: {type(enhancer.inpaint_pipeline).__name__}")
else:
    print("   ❌ Inpaint pipeline: Not loaded")
    if enhancer.use_inpainting:
        print("   ⚠️  Inpainting is enabled but pipeline not loaded!")
        print("   This means it will fall back to img2img (global enhancement)")
print()

print("3. What will be used:")
if enhancer.use_inpainting and enhancer.inpaint_pipeline:
    print("   ✅ Inpainting (localized enhancement)")
else:
    print("   ⚠️  Img2Img (global enhancement - entire image)")
    print("   This is why you're seeing full image regeneration!")
print()

print("=" * 60)
if enhancer.use_inpainting and enhancer.inpaint_pipeline:
    print("✅ Setup looks correct!")
else:
    print("⚠️  Setup issue detected!")
    print()
    print("Possible causes:")
    print("  1. Inpaint pipeline failed to load")
    print("  2. Check server logs for errors")
    print("  3. May need to restart server")
print("=" * 60)

