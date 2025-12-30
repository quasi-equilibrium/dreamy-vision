# How to Verify Inpainting is Working

## 🔍 Check Server Logs

When you make a request, check the server terminal output. You should see:

**✅ If inpainting is working:**
```
🎨 Using INPAINTING pipeline (localized enhancement)
```

**❌ If it's falling back:**
```
⚠️  Using IMG2IMG pipeline (global enhancement - entire image)
   Reason: Inpaint pipeline not loaded
```

---

## 🧪 Quick Test

1. **Make a request** through the web interface
2. **Check the server terminal** (where uvicorn is running)
3. **Look for the message** above

---

## 🔧 If It's Not Using Inpainting

**Possible reasons:**

1. **Inpaint pipeline failed to load**
   - Check for errors in server startup
   - May need to download additional models

2. **Server needs restart**
   - Stop server (Ctrl+C)
   - Restart: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

3. **Model loading error**
   - Check if you see "Models loaded successfully"
   - Check for any error messages

---

## 📊 What You Should See

**In server logs when processing:**
```
Loading models on device: cpu
Models loaded successfully
🎨 Using INPAINTING pipeline (localized enhancement)
```

**If you see:**
```
⚠️  Using IMG2IMG pipeline
```
Then inpainting isn't working and we need to fix it.

---

## 🎯 Expected Behavior

**With inpainting working:**
- Only the area where you drew is enhanced
- Rest of image stays the same
- Original colors/textures preserved outside mask

**Without inpainting (fallback):**
- Entire image is regenerated
- Original connection lost
- This is what you're experiencing

---

**Check your server logs and let me know what you see!**

