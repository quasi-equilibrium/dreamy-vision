#!/usr/bin/env python3
"""
Comprehensive installation verification script
Checks if everything is set up correctly
"""

import sys
import os

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_check(name, status, details=""):
    """Print a check result"""
    if status:
        print(f"{GREEN}✅{RESET} {name}")
        if details:
            print(f"   {details}")
    else:
        print(f"{RED}❌{RESET} {name}")
        if details:
            print(f"   {details}")

def print_warning(name, details=""):
    """Print a warning"""
    print(f"{YELLOW}⚠️{RESET} {name}")
    if details:
        print(f"   {details}")

def print_info(name, details=""):
    """Print info"""
    print(f"{BLUE}ℹ️{RESET} {name}")
    if details:
        print(f"   {details}")

print("=" * 60)
print("Dreamy Vision - Installation Verification")
print("=" * 60)
print()

# Check 1: Python version
print("1. Python Environment")
print("-" * 60)
try:
    python_version = sys.version_info
    version_str = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
    if python_version.major == 3 and python_version.minor >= 9:
        print_check("Python version", True, f"Python {version_str}")
    else:
        print_check("Python version", False, f"Python {version_str} (need 3.9+)")
except:
    print_check("Python version", False, "Could not determine version")

# Check 2: Virtual environment
print()
print("2. Virtual Environment")
print("-" * 60)
venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
if venv_active:
    print_check("Virtual environment active", True, f"Using: {sys.prefix}")
else:
    print_warning("Virtual environment", "Not activated. Run: source venv/bin/activate")

# Check 3: Required packages
print()
print("3. Python Packages")
print("-" * 60)

packages = {
    "fastapi": "FastAPI",
    "uvicorn": "Uvicorn",
    "torch": "PyTorch",
    "diffusers": "Diffusers",
    "transformers": "Transformers",
    "pillow": "Pillow",
    "opencv-python": "OpenCV",
    "numpy": "NumPy",
    "controlnet_aux": "ControlNet Aux",
    "requests": "Requests",
}

installed = {}
missing = []

for package, name in packages.items():
    try:
        if package == "opencv-python":
            import cv2
            version = cv2.__version__
        elif package == "controlnet_aux":
            import controlnet_aux
            version = getattr(controlnet_aux, '__version__', 'installed')
        else:
            mod = __import__(package.replace("-", "_"))
            version = getattr(mod, '__version__', 'installed')
        installed[package] = version
        print_check(name, True, f"v{version}")
    except ImportError:
        missing.append(name)
        print_check(name, False, "Not installed")

if missing:
    print()
    print_warning("Missing packages", f"Install with: pip install -r requirements.txt")

# Check 4: Stable Diffusion Models
print()
print("4. Stable Diffusion Models")
print("-" * 60)

cache_dir = os.path.expanduser("~/.cache/huggingface/hub/")
if os.path.exists(cache_dir):
    import subprocess
    try:
        result = subprocess.run(
            ["du", "-sh", cache_dir],
            capture_output=True,
            text=True,
            timeout=5
        )
        size = result.stdout.split()[0]
        
        # Check for model directories
        sd_dir = os.path.join(cache_dir, "models--runwayml--stable-diffusion-v1-5")
        cn_dir = os.path.join(cache_dir, "models--lllyasviel--sd-controlnet-canny")
        
        sd_exists = os.path.exists(sd_dir)
        cn_exists = os.path.exists(cn_dir)
        
        if sd_exists and cn_exists:
            print_check("Models downloaded", True, f"Total size: {size}")
            print_info("Stable Diffusion 1.5", "Found")
            print_info("ControlNet Canny", "Found")
        else:
            print_warning("Models", f"Cache exists ({size}) but models may not be complete")
            if not sd_exists:
                print_warning("", "Stable Diffusion model not found")
            if not cn_exists:
                print_warning("", "ControlNet model not found")
    except:
        print_warning("Models", "Could not check cache size")
else:
    print_check("Models downloaded", False, "Cache directory not found")

# Check 5: Application files
print()
print("5. Application Files")
print("-" * 60)

required_files = [
    ("app/main.py", "Main application"),
    ("app/models/enhancer.py", "Image enhancer"),
    ("app/models/llm_service.py", "LLM service"),
    ("app/config.py", "Configuration"),
    ("app/utils/image_processing.py", "Image processing utils"),
]

all_present = True
for file_path, name in required_files:
    full_path = os.path.join(os.path.dirname(__file__), file_path)
    if os.path.exists(full_path):
        print_check(name, True)
    else:
        print_check(name, False, f"Missing: {file_path}")
        all_present = False

# Check 6: Server connectivity
print()
print("6. Server Status")
print("-" * 60)

try:
    import requests
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        print_check("Server running", True, "http://localhost:8000")
    else:
        print_warning("Server", f"Responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print_warning("Server", "Not running. Start with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
except Exception as e:
    print_warning("Server", f"Could not check: {e}")

# Check 7: Device (MPS/CUDA/CPU)
print()
print("7. Hardware Acceleration")
print("-" * 60)

try:
    import torch
    if torch.backends.mps.is_available():
        print_check("MPS (Metal) available", True, "Will use GPU acceleration on M2 Max")
    elif torch.cuda.is_available():
        print_check("CUDA available", True, "Will use GPU acceleration")
    else:
        print_warning("GPU acceleration", "Not available, will use CPU (slower)")
except:
    print_warning("PyTorch", "Could not check device support")

# Summary
print()
print("=" * 60)
print("Summary")
print("=" * 60)

if all_present and not missing and venv_active:
    print(f"{GREEN}✅ Installation looks good!{RESET}")
    print()
    print("Next steps:")
    print("  1. Make sure server is running")
    print("  2. Test endpoints: ./test_endpoints.sh")
    print("  3. Try the web frontend: cd ../web-demo && python3 -m http.server 8080")
else:
    print(f"{YELLOW}⚠️  Some issues found above{RESET}")
    print()
    if not venv_active:
        print("  → Activate virtual environment: source venv/bin/activate")
    if missing:
        print("  → Install missing packages: pip install -r requirements.txt")
    if not all_present:
        print("  → Some application files are missing")

print()

