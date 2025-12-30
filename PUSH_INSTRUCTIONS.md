# Push to GitHub - Simple Instructions

## Quick Method

Run these commands in your terminal:

```bash
cd ~/Downloads/dreamy-vision-main

# Setup git (first time only)
./setup_git.sh

# Push to GitHub
./push_to_github.sh
```

---

## Manual Method

If the scripts don't work, run these commands one by one:

```bash
cd ~/Downloads/dreamy-vision-main

# 1. Initialize git
git init

# 2. Add GitHub remote
git remote add origin https://github.com/quasi-equilibrium/dreamy-vision.git

# 3. Add all files
git add .

# 4. Commit
git commit -m "Add image cropping, size limits, improved inpainting, and lazy imports"

# 5. Push
git branch -M main
git push -u origin main
```

---

## If You Get Errors

### "Remote already exists"
```bash
git remote set-url origin https://github.com/quasi-equilibrium/dreamy-vision.git
```

### "Repository not found" or "Permission denied"
- Make sure you're logged into GitHub
- Check the repo URL is correct
- You might need to authenticate

### "Updates were rejected"
The repo might have content. Try:
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

## What's Being Pushed

✅ Image cropping tool (512x512)
✅ Size validation (max 2048x2048, 10MB)
✅ Improved inpainting with proper blending
✅ Lazy imports (prevents crashes)
✅ Better error handling
✅ All new backend improvements

---

**Run the scripts and let me know if you need help!**

