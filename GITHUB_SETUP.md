# GitHub Repository Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `dreamy-vision` (or your preferred name)
3. Description: "See the hidden figures in patterns - AI-powered pattern enhancement"
4. Choose **Public** or **Private**
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Git Locally

Open terminal and run:

```bash
cd /Users/hco/dreamy-vision

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Dreamy Vision web demo and FastAPI backend"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/dreamy-vision.git

# Or if you prefer SSH:
# git remote add origin git@github.com:YOUR_USERNAME/dreamy-vision.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages (Optional - for web demo)

1. Go to your repository on GitHub
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` → `/web-demo` folder
5. Save

Your web demo will be available at:
`https://YOUR_USERNAME.github.io/dreamy-vision/`

## Notes

- The `.gitignore` file is already created to exclude:
  - Python virtual environments
  - AI model files (too large)
  - IDE files
  - OS files

- Model files won't be uploaded (they're in .gitignore)
- Users will need to download models on first run

