# Step-by-Step: Run the Server

Follow these steps **exactly** in order.

## Step 1: Open Terminal

Open the Terminal app on your Mac.

---

## Step 2: Navigate to Backend Directory

Type this command and press Enter:

```bash
cd ~/Downloads/dreamy-vision-main/backend
```

**Verify you're in the right place:**
You should see the path in your terminal prompt. Or type:
```bash
pwd
```
Should show: `/Users/hco/Downloads/dreamy-vision-main/backend`

---

## Step 3: Activate Virtual Environment

Type this command and press Enter:

```bash
source venv/bin/activate
```

**IMPORTANT:** After this command, you should see `(venv)` at the start of your terminal prompt!

**Before:** `hco@Dreamys-Mac-Studio backend %`

**After:** `(venv) hco@Dreamys-Mac-Studio backend %`

**If you don't see `(venv)`:**
- The activation didn't work
- Make sure you're in the `backend` directory
- Try: `cd ~/Downloads/dreamy-vision-main/backend` again, then `source venv/bin/activate`

---

## Step 4: Run the Server

Type this command and press Enter:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**What you should see:**
```
INFO:     Will watch for changes in these directories: ['/Users/hco/Downloads/dreamy-vision-main/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**If you see errors:**
- Let me know what the error says
- Common: "Module not found" means venv isn't activated
- Common: "Address already in use" means port 8000 is busy

---

## Step 5: Test the Server (New Terminal)

**Keep the server running!** Open a **NEW Terminal window** (don't close the first one).

In the new terminal, type:

```bash
curl http://localhost:8000/health
```

**You should see:**
```json
{"status":"healthy"}
```

**If it works:** ✅ Server is running!

**If you see "Connection refused":**
- Go back to the first terminal
- Make sure the server is still running
- Check for any error messages

---

## Step 6: Stop the Server (When Done)

When you want to stop the server:

1. Go back to the terminal where the server is running
2. Press `Ctrl + C` (hold Control, press C)
3. You'll see the server stop

---

## Quick Reference

**To start the server:**
```bash
cd ~/Downloads/dreamy-vision-main/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**To test it:**
```bash
curl http://localhost:8000/health
```

**To stop it:**
Press `Ctrl + C` in the server terminal

---

## Troubleshooting

### "Command not found: uvicorn"
→ Virtual environment not activated. Make sure you see `(venv)` in your prompt.

### "Module not found"
→ Virtual environment not activated. Run `source venv/bin/activate` again.

### "Address already in use"
→ Port 8000 is busy. Either:
- Stop whatever is using port 8000
- Or use a different port: `--port 8001`

### Server starts but curl fails
→ Check if firewall is blocking. Try: `curl http://127.0.0.1:8000/health`

---

Ready? Start with Step 1! 🚀

