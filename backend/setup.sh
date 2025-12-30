#!/bin/bash
# Dreamy Vision Setup Script for Fresh Mac
# This script helps set up the project step by step

set -e  # Exit on error

echo "🎨 Dreamy Vision Setup Script"
echo "============================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Xcode Command Line Tools
echo "📦 Step 1: Checking Xcode Command Line Tools..."
if command_exists xcode-select && xcode-select -p &>/dev/null; then
    echo -e "${GREEN}✓ Xcode Command Line Tools are installed${NC}"
else
    echo -e "${YELLOW}⚠ Xcode Command Line Tools not found${NC}"
    echo "   Please run: xcode-select --install"
    echo "   This will open a GUI dialog. Click 'Install' and wait."
    read -p "   Press Enter after you've installed Xcode Command Line Tools..."
    
    if ! xcode-select -p &>/dev/null; then
        echo -e "${RED}✗ Xcode Command Line Tools still not found. Please install them first.${NC}"
        exit 1
    fi
fi

# Step 2: Check/Install Homebrew
echo ""
echo "🍺 Step 2: Checking Homebrew..."
if command_exists brew; then
    echo -e "${GREEN}✓ Homebrew is installed${NC}"
    brew --version
else
    echo -e "${YELLOW}⚠ Homebrew not found. Installing...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    if command_exists brew; then
        echo -e "${GREEN}✓ Homebrew installed successfully${NC}"
    else
        echo -e "${RED}✗ Homebrew installation failed${NC}"
        exit 1
    fi
fi

# Step 3: Check Python
echo ""
echo "🐍 Step 3: Checking Python..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Python 3 not found. Installing via Homebrew...${NC}"
    brew install python@3.11
    if command_exists python3; then
        echo -e "${GREEN}✓ Python installed${NC}"
    else
        echo -e "${RED}✗ Python installation failed${NC}"
        exit 1
    fi
fi

# Step 4: Navigate to backend directory
echo ""
echo "📁 Step 4: Setting up project directory..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}✗ requirements.txt not found. Are you in the backend directory?${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found project directory: $(pwd)${NC}"

# Step 5: Create virtual environment
echo ""
echo "🔧 Step 5: Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "   Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    else
        echo -e "${GREEN}✓ Using existing virtual environment${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Step 6: Activate and upgrade pip
echo ""
echo "⬆️  Step 6: Upgrading pip..."
source venv/bin/activate
pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

# Step 7: Install dependencies
echo ""
echo "📦 Step 7: Installing dependencies..."
echo "   This will download ~8GB of models. This may take 10-30 minutes..."
echo "   Please be patient..."
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 8: Check Ollama (optional)
echo ""
echo "🦙 Step 8: Checking Ollama (optional)..."
if command_exists ollama; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    echo "   To use Ollama:"
    echo "   1. Run 'ollama serve' in one terminal"
    echo "   2. Run 'ollama pull mistral' in another terminal"
else
    echo -e "${YELLOW}⚠ Ollama not found${NC}"
    read -p "   Install Ollama now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        brew install ollama
        echo -e "${GREEN}✓ Ollama installed${NC}"
        echo "   Next steps:"
        echo "   1. Run 'ollama serve' in one terminal"
        echo "   2. Run 'ollama pull mistral' in another terminal"
    else
        echo "   You can install Ollama later with: brew install ollama"
    fi
fi

# Summary
echo ""
echo "============================"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. (Optional) Test LLM setup:"
echo "   python test_llm.py --backend ollama"
echo ""
echo "3. Run the server:"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "4. In another terminal, run the frontend:"
echo "   cd ../web-demo"
echo "   python3 -m http.server 8080"
echo ""
echo "5. Open http://localhost:8080 in your browser"
echo ""
echo "Happy coding! 🎨✨"

