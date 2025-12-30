# Security Guide for Dreamy Vision Server

## 🔒 Current Security Status

### ⚠️ Current Setup (Development Mode)

Your server is currently running in **development mode** with:
- **Host:** `0.0.0.0:8000` - Accessible from your local network
- **CORS:** `allow_origins=["*"]` - Allows requests from any origin
- **No authentication** - Anyone who can reach it can use it
- **No rate limiting** - No protection against abuse

---

## 🎯 Is It Safe?

### ✅ Safe If:
- ✅ Running on your **local Mac only**
- ✅ Only **you** can access it (localhost)
- ✅ **Not exposed** to the internet
- ✅ Using for **development/testing**

### ⚠️ Risky If:
- ⚠️ Exposed to the **internet** (port forwarding, etc.)
- ⚠️ On a **shared network** (office, public WiFi)
- ⚠️ Other people can **access your network**
- ⚠️ Running **24/7** without monitoring

---

## 🛡️ Security Risks

### 1. **Network Exposure**
- `0.0.0.0` makes it accessible to your local network
- If someone is on your WiFi, they could access it
- If you have port forwarding, it's exposed to the internet

### 2. **No Authentication**
- Anyone who can reach the server can:
  - Use your AI models (costs compute resources)
  - Generate images (uses your GPU/RAM)
  - Potentially abuse the service

### 3. **Resource Abuse**
- No rate limiting means someone could:
  - Spam requests
  - Use all your GPU/RAM
  - Slow down your Mac

### 4. **CORS Wide Open**
- `allow_origins=["*"]` allows any website to call your API
- Could be used for malicious requests

---

## 🔐 How to Secure It

### Option 1: Localhost Only (Safest for Development)

**Change the host to localhost only:**

In `app/main.py` or when running:
```bash
# Instead of:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Use:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**This makes it:**
- ✅ Only accessible from your Mac
- ✅ Not accessible from network
- ✅ Safest option for development

---

### Option 2: Add Basic Authentication

Add a simple API key check:

```python
# In app/main.py
API_KEY = os.getenv("API_KEY", "your-secret-key-here")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path.startswith("/health"):
        return await call_next(request)
    
    api_key = request.headers.get("X-API-Key")
    if api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API key"}
        )
    return await call_next(request)
```

Then use it:
```bash
curl -H "X-API-Key: your-secret-key-here" http://localhost:8000/enhance
```

---

### Option 3: Restrict CORS

Change CORS to only allow your frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Only your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

### Option 4: Use Firewall

**macOS Firewall:**
1. System Settings → Network → Firewall
2. Enable Firewall
3. Block incoming connections (except what you need)

**Or use `ufw` (if installed):**
```bash
# Allow only localhost
sudo ufw allow from 127.0.0.1 to any port 8000
```

---

## 📋 Recommendations

### For Development (Current Use):
✅ **Use localhost only:**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

✅ **Keep it simple:**
- Only run when you need it
- Stop it when done (`Ctrl+C`)
- Don't expose to internet

### For Production (If You Deploy):
🔒 **Add authentication**
🔒 **Use HTTPS**
🔒 **Rate limiting**
🔒 **Proper CORS**
🔒 **Environment variables for secrets**

---

## 🚨 What NOT to Do

❌ **Don't expose to internet** without authentication
❌ **Don't use `0.0.0.0`** if you don't need network access
❌ **Don't run 24/7** without security measures
❌ **Don't share your API** publicly without protection

---

## ✅ Quick Security Checklist

- [ ] Using `127.0.0.1` instead of `0.0.0.0` (if local only)
- [ ] Firewall enabled on Mac
- [ ] Not exposing port to internet
- [ ] Only running when needed
- [ ] No sensitive data in code
- [ ] CORS restricted (if needed)

---

## 🎯 Summary

**Current Status:**
- ⚠️ Accessible on local network (if using `0.0.0.0`)
- ✅ Safe for local development
- ⚠️ Not safe for internet exposure

**Recommendation:**
- ✅ Use `127.0.0.1` for localhost-only access
- ✅ Only run when you need it
- ✅ Stop server when done
- ✅ Add authentication if exposing to network

**For now:** Your setup is **safe for local development** as long as:
- You're on a trusted network
- Not exposing to internet
- Only you can access it

