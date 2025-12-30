#!/bin/bash
# Quick test script for Dreamy Vision API endpoints

echo "🧪 Testing Dreamy Vision API"
echo "============================"
echo ""

# Test 1: Health check
echo "1️⃣ Testing /health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ "$HEALTH" == '{"status":"healthy"}' ]; then
    echo "✅ Health check passed: $HEALTH"
else
    echo "❌ Health check failed: $HEALTH"
    echo "   Make sure server is running!"
    exit 1
fi
echo ""

# Test 2: Hint endpoint (without Ollama - will use fallback)
echo "2️⃣ Testing /hint endpoint..."
HINT_RESPONSE=$(curl -s -X POST http://localhost:8000/hint \
  -H "Content-Type: application/json" \
  -d '{"description": "dinosaur", "num_hints": 3}')

if echo "$HINT_RESPONSE" | grep -q "hints"; then
    echo "✅ Hint endpoint works!"
    echo "   Response: $HINT_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "   $HINT_RESPONSE"
else
    echo "⚠️  Hint endpoint returned: $HINT_RESPONSE"
fi
echo ""

# Test 3: Root endpoint
echo "3️⃣ Testing root endpoint..."
ROOT=$(curl -s http://localhost:8000/)
echo "   Response: $ROOT"
echo ""

echo "============================"
echo "✅ Basic API tests complete!"
echo ""
echo "📝 Note: To test /enhance endpoint, you need:"
echo "   - An image file (base64 encoded)"
echo "   - A user drawing (base64 encoded)"
echo "   - A description"
echo ""
echo "   See test_enhance.py for a full example"

