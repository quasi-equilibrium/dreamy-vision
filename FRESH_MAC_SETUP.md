# Fresh Mac Setup Guide for Dreamy Vision

Since this is a fresh Mac, we need to install some prerequisites first.

## Step 1: Install Xcode Command Line Tools

This is required for Python and many other tools.

**Option A: Automatic (Recommended)**
```bash
xcode-select --install
```
This will open a GUI dialog. Click "Install" and wait for it to complete (~5-10 minutes).

**Option B: Manual**
1. Open App Store
2. Search for "Xcode"
3. Install Xcode (large download, ~12GB)
4. Or download Command Line Tools from: https://developer.apple.com/download/all/

## Step 2: Install Homebrew

Homebrew is a package manager for macOS. Install it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the prompts. This may ask for your password.

After installation, you may need to add Homebrew to your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify installation:
```bash
brew --version
```

## Step 3: Verify Python

Check if Python 3 is available:
```bash
python3 --version
```

You should see something like: `Python 3.11.x` or `Python 3.12.x`

If not, install Python via Homebrew:
```bash
brew install python@3.11
```

## Step 4: Set Up Dreamy Vision Backend

Now proceed with the project setup:

```bash
# Navigate to backend
cd ~/Downloads/dreamy-vision-main/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (this will take a while, ~8GB download)
pip install -r requirements.txt
```

**Note:** The first `pip install` will download:
- PyTorch (~2GB)
- Stable Diffusion models (~4-5GB on first use)
- ControlNet models (~1.5GB on first use)

This may take 10-30 minutes depending on your internet speed.

## Step 5: Install Ollama (Optional but Recommended)

```bash
# Install Ollama
brew install ollama

# Start Ollama (keep this terminal open)
ollama serve
```

In a **new terminal window**:
```bash
# Pull a model (choose one)
ollama pull mistral    # Fast, efficient (~4GB download)
# OR
ollama pull llama2     # Better quality (~4GB download)
```

## Step 6: Test the Setup

```bash
# Make sure you're in the backend directory with venv activated
cd ~/Downloads/dreamy-vision-main/backend
source venv/bin/activate

# Test LLM (if Ollama is running)
python test_llm.py --backend ollama
```

## Step 7: Run the Server

```bash
# Make sure venv is activated
source venv/bin/activate

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Troubleshooting

### "xcode-select: error: No developer tools were found"
- Run: `xcode-select --install`
- Wait for GUI dialog and click "Install"

### "brew: command not found"
- Install Homebrew (Step 2 above)
- Make sure to add it to your PATH

### "python3: command not found"
- Install Python: `brew install python@3.11`
- Or use the system Python if available

### "Permission denied" errors
- Some commands may need `sudo` (use carefully)
- Check file permissions

### Slow downloads
- First-time setup downloads ~12GB total
- Be patient, especially for model downloads
- Check your internet connection

## Quick Checklist

- [ ] Xcode Command Line Tools installed
- [ ] Homebrew installed
- [ ] Python 3 verified
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Ollama installed (optional)
- [ ] Server running on port 8000

## Next Steps

Once everything is set up:
1. Test the API: `curl http://localhost:8000/health`
2. Try the hint endpoint
3. Run the frontend: `cd web-demo && python3 -m http.server 8080`
4. Open `http://localhost:8080` in your browser

Good luck! 🚀

