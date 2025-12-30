# Step-by-Step Setup Guide

Follow these steps **in order**. Don't skip ahead!

## ✅ STEP 1: Install Xcode Command Line Tools (REQUIRED FIRST!)

**This is the most important step. Do this first!**

Open Terminal and run:
```bash
xcode-select --install
```

**What will happen:**
- A popup window will appear
- Click "Install" 
- Wait 5-10 minutes for it to download and install
- You'll see "The software was installed" when done

**Verify it worked:**
```bash
xcode-select -p
```
Should show: `/Library/Developer/CommandLineTools`

**If you see an error:** The GUI dialog might not have appeared. Try:
1. Open System Settings → Software Update
2. Or download manually from: https://developer.apple.com/download/all/

---

## ✅ STEP 2: Verify Python Works

After Step 1 completes, test Python:

```bash
python3 --version
```

You should see something like: `Python 3.9.6` or `Python 3.11.x`

**If it still doesn't work:** Wait a few minutes after Step 1 completes, then try again.

---

## ✅ STEP 3: Navigate to Project

```bash
cd ~/Downloads/dreamy-vision-main/backend
```

Verify you're in the right place:
```bash
ls -la requirements.txt
```

Should show the file exists.

---

## ✅ STEP 4: Create Virtual Environment

```bash
python3 -m venv venv
```

Wait for it to finish (may take 30 seconds).

**Verify it worked:**
```bash
ls -la venv
```

Should show a `venv` directory.

---

## ✅ STEP 5: Activate Virtual Environment

```bash
source venv/bin/activate
```

**You should see `(venv)` at the start of your terminal prompt!**

Like this: `(venv) user@mac backend %`

**If you don't see (venv):** The activation didn't work. Try:
```bash
cd ~/Downloads/dreamy-vision-main/backend
source venv/bin/activate
```

---

## ✅ STEP 6: Upgrade pip

```bash
pip install --upgrade pip
```

Wait for it to finish.

---

## ✅ STEP 7: Install Packages (THIS TAKES A WHILE!)

**Important:** This downloads ~8GB. Be patient! (10-30 minutes)

```bash
pip install -r requirements.txt
```

**What's happening:**
- Downloading PyTorch (~2GB)
- Downloading Stable Diffusion models (~4-5GB)
- Downloading other dependencies

**You'll see lots of output.** This is normal. Let it run.

**Common issues:**
- If it stops/freezes: Wait 5 minutes, then press Ctrl+C and try again
- If you see "Connection timeout": Your internet is slow, wait longer
- If you see "Permission denied": Make sure `(venv)` is in your prompt

---

## ✅ STEP 8: Verify Installation

After Step 7 finishes, test it:

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
```

Should print a version number.

```bash
python -c "import fastapi; print('FastAPI installed')"
```

Should print "FastAPI installed".

---

## ✅ STEP 9: Test the Server

```bash
# Make sure (venv) is active!
source venv/bin/activate

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**If you see errors:** Let me know what the error says!

---

## 🆘 Troubleshooting

### "xcode-select: error"
→ You didn't complete Step 1. Go back and install Xcode Command Line Tools.

### "python3: command not found"
→ Step 1 didn't complete. Wait longer, then try again.

### "No module named 'venv'"
→ Step 1 didn't complete. Install Xcode Command Line Tools.

### "Permission denied"
→ Make sure you activated the virtual environment (Step 5). You should see `(venv)` in your prompt.

### Packages install very slowly
→ This is normal! ~8GB download takes time. Be patient.

### "Could not find a version that satisfies the requirement"
→ Your Python version might be too old. Check with `python3 --version`. Need 3.9+.

---

## 📝 Quick Checklist

- [ ] Step 1: Xcode Command Line Tools installed
- [ ] Step 2: `python3 --version` works
- [ ] Step 3: In `~/Downloads/dreamy-vision-main/backend` directory
- [ ] Step 4: `venv` directory exists
- [ ] Step 5: See `(venv)` in terminal prompt
- [ ] Step 6: pip upgraded
- [ ] Step 7: All packages installed (takes 10-30 min)
- [ ] Step 8: Can import torch and fastapi
- [ ] Step 9: Server runs without errors

---

**Ready? Start with Step 1!** 🚀

