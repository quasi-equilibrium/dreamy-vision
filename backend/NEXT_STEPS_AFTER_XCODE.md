# What to Do After Xcode Command Line Tools Install

## ✅ Step 1: Verify Installation Complete

Once you see "The software was installed" popup, verify it worked:

```bash
xcode-select -p
```

Should show: `/Library/Developer/CommandLineTools`

Also test Python:
```bash
python3 --version
```

Should show: `Python 3.x.x` (any version 3.9+ is fine)

---

## ✅ Step 2: Navigate to Project

```bash
cd ~/Downloads/dreamy-vision-main/backend
```

---

## ✅ Step 3: Create Virtual Environment

```bash
python3 -m venv venv
```

Wait ~30 seconds. You should see no errors.

---

## ✅ Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

**IMPORTANT:** Your terminal prompt should now show `(venv)` at the start!

Like: `(venv) hco@Dreamys-Mac-Studio backend %`

If you don't see `(venv)`, the activation didn't work. Try again.

---

## ✅ Step 5: Upgrade pip

```bash
pip install --upgrade pip
```

---

## ✅ Step 6: Install All Packages

**This is the big one! Downloads ~8GB, takes 10-30 minutes.**

```bash
pip install -r requirements.txt
```

**What you'll see:**
- Lots of "Collecting..." messages
- "Downloading..." progress bars
- This is normal! Let it run.

**Don't worry if:**
- It seems slow (normal!)
- You see warnings (usually fine)
- It takes 20+ minutes (normal for first install)

**Only stop if:**
- You see a clear ERROR (not warning)
- It completely freezes for 10+ minutes

---

## ✅ Step 7: Verify Installation

After Step 6 finishes, test:

```bash
python -c "import torch; print('PyTorch OK')"
python -c "import fastapi; print('FastAPI OK')"
```

Both should print "OK" messages.

---

## ✅ Step 8: Run the Server!

```bash
# Make sure (venv) is in your prompt!
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Success!** 🎉

---

## Quick Helper Script

After Xcode installs, you can run:

```bash
cd ~/Downloads/dreamy-vision-main/backend
./check_setup.sh
```

This tells you exactly what step you're on!

