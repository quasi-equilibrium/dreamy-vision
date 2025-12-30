#!/bin/bash
# Push all changes to GitHub

cd ~/Downloads/dreamy-vision-main

echo "📤 Pushing to GitHub..."
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run ./setup_git.sh first"
    exit 1
fi

# Add all files
echo "1. Adding files..."
git add .

# Check if there are changes
if git diff --cached --quiet; then
    echo "   ⚠️  No changes to commit"
    git status
    exit 0
fi

# Commit
echo "2. Committing changes..."
git commit -m "Add image cropping tool, size limits, improved inpainting with proper blending, and lazy imports for stability"

# Push
echo "3. Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "   View at: https://github.com/quasi-equilibrium/dreamy-vision"
else
    echo ""
    echo "❌ Push failed. You may need to:"
    echo "   - Pull first: git pull origin main --allow-unrelated-histories"
    echo "   - Or force push (if you're sure): git push -u origin main --force"
fi

