#!/bin/bash
# Quick setup checker - tells you what step you're on

echo "🔍 Checking your setup..."
echo "========================="
echo ""

# Check Xcode Command Line Tools
echo -n "1. Xcode Command Line Tools: "
if xcode-select -p &>/dev/null; then
    echo "✅ INSTALLED"
    XCODE_OK=true
else
    echo "❌ NOT INSTALLED"
    echo "   → Run: xcode-select --install"
    XCODE_OK=false
fi

# Check Python
echo -n "2. Python 3: "
if /usr/bin/python3 --version &>/dev/null 2>&1; then
    PYTHON_VER=$(/usr/bin/python3 --version 2>&1 | head -1)
    echo "✅ FOUND - $PYTHON_VER"
    PYTHON_OK=true
else
    echo "❌ NOT WORKING"
    PYTHON_OK=false
fi

# Check if in right directory
echo -n "3. Project directory: "
if [ -f "requirements.txt" ]; then
    echo "✅ CORRECT ($(pwd))"
    DIR_OK=true
else
    echo "❌ WRONG DIRECTORY"
    echo "   → Run: cd ~/Downloads/dreamy-vision-main/backend"
    DIR_OK=false
fi

# Check virtual environment
echo -n "4. Virtual environment: "
if [ -d "venv" ]; then
    echo "✅ EXISTS"
    VENV_OK=true
else
    echo "❌ NOT CREATED"
    echo "   → Run: python3 -m venv venv"
    VENV_OK=false
fi

# Check if venv is activated
echo -n "5. Virtual environment activated: "
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ YES"
    ACTIVATED=true
else
    echo "❌ NO"
    echo "   → Run: source venv/bin/activate"
    ACTIVATED=false
fi

# Check packages
echo -n "6. Packages installed: "
if [ "$ACTIVATED" = true ] && python -c "import torch" &>/dev/null 2>&1; then
    echo "✅ YES"
    PACKAGES_OK=true
else
    echo "❌ NO"
    if [ "$ACTIVATED" = true ]; then
        echo "   → Run: pip install -r requirements.txt"
    else
        echo "   → First activate venv, then install packages"
    fi
    PACKAGES_OK=false
fi

echo ""
echo "========================="
echo ""

# Summary
if [ "$XCODE_OK" = false ]; then
    echo "🚨 START HERE: Install Xcode Command Line Tools"
    echo "   Run: xcode-select --install"
    echo "   Wait for GUI dialog, click Install, wait 5-10 minutes"
elif [ "$DIR_OK" = false ]; then
    echo "📍 Navigate to project: cd ~/Downloads/dreamy-vision-main/backend"
elif [ "$VENV_OK" = false ]; then
    echo "📦 Create virtual environment: python3 -m venv venv"
elif [ "$ACTIVATED" = false ]; then
    echo "🔌 Activate virtual environment: source venv/bin/activate"
elif [ "$PACKAGES_OK" = false ]; then
    echo "📥 Install packages: pip install -r requirements.txt"
    echo "   (This takes 10-30 minutes, downloads ~8GB)"
else
    echo "✅ Everything looks good! You can run:"
    echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
fi

echo ""

