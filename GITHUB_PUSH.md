# How to Push to GitHub

Since this was downloaded as a zip, we need to initialize git and push.

## Step 1: Initialize Git

```bash
cd ~/Downloads/dreamy-vision-main
git init
```

## Step 2: Add All Files

```bash
git add .
```

## Step 3: Create Initial Commit

```bash
git commit -m "Add image cropping, size limits, and improved inpainting"
```

## Step 4: Add Remote (Your GitHub Repo)

```bash
git remote add origin https://github.com/quasi-equilibrium/dreamy-vision.git
```

## Step 5: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

---

## What Was Added

- ✅ Image cropping tool (512x512)
- ✅ Size validation (max 2048x2048, 10MB)
- ✅ Improved inpainting with proper blending
- ✅ Better error handling
- ✅ Lazy imports to prevent crashes

---

## If You Get Errors

**"Repository not found":**
- Make sure the repo exists on GitHub
- Check the URL is correct

**"Permission denied":**
- You may need to authenticate
- Use: `gh auth login` (if GitHub CLI installed)
- Or use SSH: `git@github.com:quasi-equilibrium/dreamy-vision.git`

**"Already exists":**
- If repo has content, you might need to pull first:
```bash
git pull origin main --allow-unrelated-histories
```

