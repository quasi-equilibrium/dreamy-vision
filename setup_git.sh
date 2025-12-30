#!/bin/bash
# Setup Git and push to GitHub

echo "🔧 Setting up Git repository..."
echo ""

cd ~/Downloads/dreamy-vision-main

# Initialize git
echo "1. Initializing git repository..."
git init

# Add remote
echo "2. Adding GitHub remote..."
git remote add origin https://github.com/quasi-equilibrium/dreamy-vision.git

# Check if remote was added
if git remote -v | grep -q "quasi-equilibrium"; then
    echo "   ✅ Remote added successfully"
else
    echo "   ⚠️  Remote might already exist or failed"
    git remote -v
fi

echo ""
echo "3. Checking current status..."
git status

echo ""
echo "✅ Git setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Add files: git add ."
echo "  3. Commit: git commit -m 'Add image cropping, size limits, and improved inpainting'"
echo "  4. Push: git push -u origin main"
echo ""
echo "Or run: ./push_to_github.sh"

