# LLM Setup Guide for Dreamy Vision

Dreamy Vision supports multiple LLM backends for prompt enhancement and understanding user descriptions. Choose the one that best fits your needs.

## Option 1: Ollama (Recommended for Local Use) 🦙

Ollama runs LLMs locally on your Mac Studio M2 Max. It's free, private, and works offline.

### Installation

```bash
# Install Ollama
brew install ollama

# Start Ollama service
ollama serve

# In another terminal, pull a model (choose one):
ollama pull llama2        # Good balance (7B parameters)
ollama pull mistral       # Fast and efficient
ollama pull codellama     # Good for technical tasks
ollama pull llama2:13b    # Larger, more capable (requires more RAM)
```

### Usage

The app will automatically use Ollama if it's running on `http://localhost:11434`.

**Pros:**
- ✅ Free and private
- ✅ Works offline
- ✅ No API keys needed
- ✅ Fast on M2 Max

**Cons:**
- ⚠️ Requires ~4-8GB RAM per model
- ⚠️ First run downloads model (~4-7GB)

## Option 2: OpenAI API (Cloud-Based) ☁️

Use GPT-3.5 or GPT-4 for prompt enhancement.

### Setup

```bash
# Set your API key
export OPENAI_API_KEY="your-api-key-here"
```

Then update `backend/app/main.py` to use OpenAI:
```python
llm_service = get_llm_service("openai")
```

**Pros:**
- ✅ Very high quality responses
- ✅ No local resources needed
- ✅ Always up-to-date models

**Cons:**
- ⚠️ Requires API key and costs money
- ⚠️ Requires internet connection
- ⚠️ Data sent to OpenAI servers

## Option 3: Hugging Face Transformers (Advanced) 🤗

Run local Hugging Face models. More complex setup but fully customizable.

### Setup

```python
# In backend/app/main.py
llm_service = get_llm_service("huggingface")
```

**Pros:**
- ✅ Full control over model
- ✅ Can use any Hugging Face model
- ✅ Completely offline

**Cons:**
- ⚠️ Requires significant RAM (8GB+)
- ⚠️ Slow first-time model loading
- ⚠️ More complex configuration

## Testing Your LLM Setup

Create a test script:

```python
# test_llm.py
from app.models.llm_service import get_llm_service

llm = get_llm_service("ollama")  # or "openai"

# Test prompt enhancement
enhanced = llm.enhance_prompt("dinosaur in clouds")
print(f"Enhanced: {enhanced}")

# Test hint generation
hints = llm.generate_hints("dinosaur", num_hints=3)
print(f"Hints: {hints}")
```

Run it:
```bash
cd backend
python test_llm.py
```

## Switching LLM Backends

Edit `backend/app/main.py`:

```python
# Use Ollama (default)
llm_service = get_llm_service("ollama")

# Use OpenAI
llm_service = get_llm_service("openai")

# Use Hugging Face
llm_service = get_llm_service("huggingface")
```

## Recommended Setup for Mac Studio M2 Max

1. **Start with Ollama + Mistral**: Fast, efficient, good quality
   ```bash
   brew install ollama
   ollama pull mistral
   ```

2. **For better quality, use Llama2 13B** (if you have 32GB+ RAM):
   ```bash
   ollama pull llama2:13b
   ```

3. **For production/cloud, use OpenAI** (if budget allows)

## Troubleshooting

### Ollama not connecting?
- Check if Ollama is running: `curl http://localhost:11434/api/tags`
- Start it: `ollama serve`
- Check firewall settings

### Out of memory?
- Use smaller models (mistral instead of llama2:13b)
- Close other applications
- Consider using OpenAI API instead

### Slow responses?
- Use smaller/faster models (mistral, llama2:7b)
- Reduce `num_hints` parameter
- Consider OpenAI API for faster cloud processing

