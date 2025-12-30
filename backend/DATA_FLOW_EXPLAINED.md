# How User Input Flows Through the System

## 📥 User Inputs

1. **Text Description:** "What do you see here?" → User types: `"dinosaur"`
2. **User Drawing:** User draws on the image → Canvas drawing (PNG image)

---

## 🔄 Current Flow

### Step 1: User Submits (`/enhance` endpoint)

```python
# In app/main.py
request = {
    "original_image": base64_image,      # Original pattern photo
    "user_drawing": base64_drawing,       # User's sketch
    "description": "dinosaur",            # User's text
    "enhancement_strength": 0.3
}
```

### Step 2: Image Processing

**Original Image:**
- Resized to 512x512
- Kept as-is (this is what we enhance)

**User Drawing:**
- Converted to grayscale
- **Canny edge detection applied** (extracts edges)
- Becomes the "control image" for ControlNet
- **This is NOT sent to LLM** - it's visual guidance only

```python
# In app/utils/image_processing.py
def prepare_drawing_mask(drawing):
    gray = cv2.cvtColor(drawing, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)  # Edge detection
    return edges  # This becomes control_image
```

### Step 3: LLM Prompt Enhancement

**Only the TEXT description goes to LLM:**

```python
# In app/models/enhancer.py
description = "dinosaur"  # User's text

# LLM enhances the text prompt
enhanced_prompt = llm_service.enhance_prompt(description)
# Result: "minimal line art, dinosaur silhouette, clean edges..."
```

**The drawing is NOT sent to LLM** - it's only used as visual control.

### Step 4: Stable Diffusion Processing

**Three inputs go to Stable Diffusion:**

1. **Original Image** (512x512) - The pattern photo
2. **Control Image** (Canny edges from user drawing) - Visual guide
3. **Enhanced Prompt** (from LLM) - Text description

```python
result = pipeline(
    prompt=enhanced_prompt,           # Text: "minimal line art, dinosaur..."
    image=original_image,              # Original pattern photo
    control_image=control_image,        # Canny edges from user drawing
    strength=0.3,                      # How much to change
    ...
)
```

---

## 🎯 Key Points

### What LLM Sees:
✅ **Text description only** ("dinosaur")
❌ **NOT the drawing**
❌ **NOT the original image**

### What ControlNet Sees:
✅ **Canny edges from user drawing** (visual guide)
✅ **Original image** (what to enhance)
✅ **Text prompt** (what to create)

### What Stable Diffusion Sees:
✅ **All three:** Original + Control edges + Text prompt

---

## 🤔 Current Limitations

**The LLM doesn't see:**
- The user's drawing (only text description)
- The original image (no visual context)
- Where the drawing is placed

**This means:**
- LLM can't understand the visual relationship
- LLM can't see if drawing matches description
- LLM can't provide context-aware prompts

---

## 💡 Potential Improvements

### Option 1: Vision-Language Model (VLM)
**Give LLM visual context:**
- Send original image + drawing to a vision model
- Get better, context-aware prompts
- Examples: GPT-4 Vision, LLaVA, CLIP

### Option 2: Image-to-Text Analysis
**Analyze the drawing:**
- Use image captioning to describe the drawing
- Compare with user's text description
- Generate better prompts

### Option 3: Multi-Modal LLM
**Full context:**
- Send: original image + drawing + text description
- Get: enhanced prompt that understands all three

---

## 📊 Current vs. Improved Flow

### Current:
```
User Text → LLM → Enhanced Prompt
User Drawing → Canny Edges → ControlNet
Original Image → Stable Diffusion
```

### Improved (with Vision):
```
User Text + Drawing + Original Image → Vision LLM → Enhanced Prompt
User Drawing → Canny Edges → ControlNet  
Original Image → Stable Diffusion
```

---

## ❓ Questions for You

1. **Should LLM see the drawing?**
   - Currently: No (only text)
   - Could: Yes (with vision model)

2. **Should LLM see the original image?**
   - Currently: No
   - Could: Yes (to understand context)

3. **Is the text description enough?**
   - Currently: Yes (for basic prompts)
   - Could: No (need visual context)

4. **What's the main issue?**
   - LLM prompts not good enough?
   - ControlNet guidance not working?
   - Stable Diffusion generating too much?

---

**Let me know your thoughts and I'll explain more or suggest improvements!**

