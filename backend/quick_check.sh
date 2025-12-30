#!/bin/bash
# Quick installation check

echo "🔍 Dreamy Vision - Quick Installation Check"
echo "==========================================="
echo ""

# Check 1: Virtual environment
echo "1. Virtual Environment:"
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "   ✅ Activated: $VIRTUAL_ENV"
else
    echo "   ⚠️  Not activated"
    echo "      Run: source venv/bin/activate"
fi
echo ""

# Check 2: Python packages
echo "2. Python Packages:"
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null

python3 -c "import fastapi; print('   ✅ FastAPI')" 2>/dev/null || echo "   ❌ FastAPI missing"
python3 -c "import uvicorn; print('   ✅ Uvicorn')" 2>/dev/null || echo "   ❌ Uvicorn missing"
python3 -c "import torch; print('   ✅ PyTorch')" 2>/dev/null || echo "   ❌ PyTorch missing"
python3 -c "import diffusers; print('   ✅ Diffusers')" 2>/dev/null || echo "   ❌ Diffusers missing"
python3 -c "import transformers; print('   ✅ Transformers')" 2>/dev/null || echo "   ❌ Transformers missing"
python3 -c "import PIL; print('   ✅ Pillow')" 2>/dev/null || echo "   ❌ Pillow missing"
python3 -c "import cv2; print('   ✅ OpenCV')" 2>/dev/null || echo "   ❌ OpenCV missing"
echo ""

# Check 3: Application files
echo "3. Application Files:"
[ -f "app/main.py" ] && echo "   ✅ app/main.py" || echo "   ❌ app/main.py missing"
[ -f "app/models/enhancer.py" ] && echo "   ✅ app/models/enhancer.py" || echo "   ❌ enhancer.py missing"
[ -f "app/models/llm_service.py" ] && echo "   ✅ app/models/llm_service.py" || echo "   ❌ llm_service.py missing"
[ -f "app/config.py" ] && echo "   ✅ app/config.py" || echo "   ❌ config.py missing"
echo ""

# Check 4: Models
echo "4. Stable Diffusion Models:"
MODEL_SIZE=$(du -sh ~/.cache/huggingface/hub/ 2>/dev/null | cut -f1)
if [ -d ~/.cache/huggingface/hub/models--runwayml--stable-diffusion-v1-5 ] && \
   [ -d ~/.cache/huggingface/hub/models--lllyasviel--sd-controlnet-canny ]; then
    echo "   ✅ Models downloaded ($MODEL_SIZE)"
else
    echo "   ⚠️  Models not fully downloaded ($MODEL_SIZE)"
fi
echo ""

# Check 5: Server
echo "5. Server Status:"
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "   ✅ Server running on http://localhost:8000"
else
    echo "   ⚠️  Server not running"
    echo "      Start with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
fi
echo ""

echo "==========================================="
echo "✅ Check complete!"
echo ""

