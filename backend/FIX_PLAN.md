# Fix Plan: Localized Enhancement

## 🎯 The Problem

**Current behavior:**
- Entire image is regenerated
- Sketch location is ignored
- Text description has no effect
- Original image connection is lost

**Desired behavior:**
- Only enhance the area where user drew
- Preserve rest of original image
- Follow sketch location precisely
- Respect text description in that area only

---

## 🔧 Root Causes

1. **No masking** - Processing entire image, not just drawn area
2. **Strength too high** (0.3) - Regenerating too much
3. **No location awareness** - Sketch position ignored
4. **Wrong approach** - Using img2img globally instead of localized inpainting

---

## ✅ Solution: Masked Inpainting

**Change from:**
- Global img2img (entire image)

**To:**
- Masked inpainting (only drawn area)

**How:**
1. Create mask from user's drawing (where they drew)
2. Use inpainting pipeline instead of img2img
3. Only process the masked area
4. Blend result back into original

---

## 🛠️ Implementation Steps

### Step 1: Create Mask from Drawing
- Detect where user actually drew (non-black pixels)
- Create binary mask (1 = drawn area, 0 = preserve)
- Expand mask slightly for smooth blending

### Step 2: Use Inpainting Pipeline
- Switch from `StableDiffusionControlNetImg2ImgPipeline`
- To `StableDiffusionControlNetInpaintPipeline`
- This only processes masked areas

### Step 3: Lower Strength
- Reduce from 0.3 to 0.15-0.20
- Less regeneration, more enhancement

### Step 4: Better Blending
- Blend enhanced area with original
- Preserve original colors outside mask
- Smooth edges

---

## 📝 Code Changes Needed

1. **Add mask creation function**
2. **Switch to inpainting pipeline**
3. **Update enhance() method**
4. **Add blending logic**

---

Let me implement this fix now!

