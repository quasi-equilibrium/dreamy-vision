# Dreamy Vision - Complete Setup Guide

## Prerequisites

- Mac Studio M2 Max
- Python 3.9+ (check with `python3 --version`)
- Homebrew (for Ollama installation)

## Step 1: Clone and Navigate

```bash
cd ~/Downloads/dreamy-vision-main/backend
```

## Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 3: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

**Note:** This will download:
- PyTorch (~2GB)
- Stable Diffusion models (~4-5GB on first use)
- ControlNet models (~1.5GB on first use)

Total download: ~8GB (one-time)

## Step 4: Set Up LLM (Choose One)

### Option A: Ollama (Recommended)

```bash
# Install Ollama
brew install ollama

# Start Ollama (in a separate terminal)
ollama serve

# Pull a model (in another terminal)
ollama pull mistral    # Fast, efficient (~4GB)
# OR
ollama pull llama2     # Better quality (~4GB)
```

### Option B: OpenAI API

```bash
# Set your API key
export OPENAI_API_KEY="your-key-here"
```

### Option C: Skip LLM (Basic Mode)

The app will work without LLM, but prompts won't be enhanced.

## Step 5: Test LLM Setup (Optional)

```bash
# Test Ollama
python test_llm.py --backend ollama

# Test OpenAI
python test_llm.py --backend openai
```

## Step 6: Run the Backend

```bash
# Make sure you're in the backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 7: Test the API

Open a new terminal and test:

```bash
# Health check
curl http://localhost:8000/health

# Test hint endpoint (if LLM is set up)
curl -X POST http://localhost:8000/hint \
  -H "Content-Type: application/json" \
  -d '{"description": "dinosaur", "num_hints": 3}'
```

## Step 8: Run Frontend

In another terminal:

```bash
cd ~/Downloads/dreamy-vision-main/web-demo
python3 -m http.server 8080
```

Open `http://localhost:8080` in your browser.

## Troubleshooting

### "Models not found" error
- Models download automatically on first use
- Check internet connection
- Be patient, first run takes 5-10 minutes

### "Ollama connection failed"
- Make sure `ollama serve` is running
- Check: `curl http://localhost:11434/api/tags`

### Out of memory
- Close other applications
- Use smaller models (mistral instead of llama2:13b)
- Reduce image size in config.py

### MPS (Metal) errors
- PyTorch MPS support is experimental
- If issues occur, the code falls back to CPU (slower but works)

## Next Steps

1. Try the `/hint` endpoint with different descriptions
2. Test image enhancement with `/enhance`
3. Experiment with different LLM backends
4. Adjust `enhancement_strength` parameter (0.2-0.4)

## Performance Expectations (M2 Max)

- Model loading: ~30-60 seconds (first time)
- Image enhancement: ~2-5 seconds per image
- LLM hint generation: ~1-3 seconds (Ollama)
- Total pipeline: ~3-8 seconds end-to-end

Enjoy! 🎨✨

