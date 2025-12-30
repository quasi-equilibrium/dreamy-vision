#!/usr/bin/env python3
"""
Test script for the /enhance endpoint
Creates test images and tests the enhancement API
"""

import requests
import base64
import io
from PIL import Image, ImageDraw
import json
import sys

def create_test_image(size=(512, 512), pattern="clouds"):
    """Create a test pattern image"""
    img = Image.new('RGB', size, color='lightblue')
    draw = ImageDraw.Draw(img)
    
    if pattern == "clouds":
        # Draw some cloud-like shapes
        for i in range(5):
            x = 100 + i * 80
            y = 150 + (i % 2) * 50
            draw.ellipse([x, y, x+100, y+60], fill='white', outline='gray')
    elif pattern == "texture":
        # Draw a texture pattern
        for x in range(0, size[0], 20):
            for y in range(0, size[1], 20):
                if (x + y) % 40 == 0:
                    draw.rectangle([x, y, x+10, y+10], fill='gray')
    
    return img

def create_test_drawing(size=(512, 512), shape="dinosaur"):
    """Create a simple test drawing"""
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)
    
    if shape == "dinosaur":
        # Simple dinosaur silhouette
        # Body
        draw.ellipse([200, 200, 350, 350], fill='white', outline='white')
        # Head
        draw.ellipse([150, 150, 250, 250], fill='white', outline='white')
        # Tail
        draw.ellipse([350, 250, 450, 350], fill='white', outline='white')
        # Legs
        draw.rectangle([220, 350, 240, 450], fill='white')
        draw.rectangle([310, 350, 330, 450], fill='white')
    elif shape == "circle":
        draw.ellipse([150, 150, 350, 350], fill='white', outline='white')
    else:
        # Simple line
        draw.line([100, 200, 400, 300], fill='white', width=5)
    
    return img

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    return base64.b64encode(image_data).decode('utf-8')

def test_enhance_endpoint():
    """Test the /enhance endpoint"""
    
    print("=" * 60)
    print("Testing Image Enhancement Endpoint")
    print("=" * 60)
    print()
    
    # Check if server is running
    print("1. Checking server status...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("   ✅ Server is running")
        else:
            print(f"   ❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running!")
        print("   Start server with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Create test images
    print("2. Creating test images...")
    original_image = create_test_image(pattern="clouds")
    user_drawing = create_test_drawing(shape="dinosaur")
    
    print("   ✅ Created test pattern image (clouds)")
    print("   ✅ Created test drawing (dinosaur silhouette)")
    
    # Save test images for reference
    original_image.save("test_original.png")
    user_drawing.save("test_drawing.png")
    print("   💾 Saved test images: test_original.png, test_drawing.png")
    print()
    
    # Convert to base64
    print("3. Preparing request...")
    original_b64 = image_to_base64(original_image)
    drawing_b64 = image_to_base64(user_drawing)
    description = "dinosaur in clouds"
    
    print(f"   Description: '{description}'")
    print(f"   Original image size: {len(original_b64)} bytes (base64)")
    print(f"   Drawing size: {len(drawing_b64)} bytes (base64)")
    print()
    
    # Make request
    print("4. Sending enhancement request...")
    print("   This may take 30-60 seconds (first time loads models)...")
    print()
    
    payload = {
        "original_image": original_b64,
        "user_drawing": drawing_b64,
        "description": description,
        "enhancement_strength": 0.3
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/enhance",
            json=payload,
            timeout=120  # 2 minutes timeout for first request
        )
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Enhancement successful!")
            print(f"   Processing time: {result.get('processing_time', 0):.2f} seconds")
            print()
            
            # Decode and save result
            print("5. Saving result...")
            enhanced_b64 = result.get('enhanced_image', '')
            if enhanced_b64:
                enhanced_data = base64.b64decode(enhanced_b64)
                enhanced_image = Image.open(io.BytesIO(enhanced_data))
                enhanced_image.save("test_enhanced.png")
                print("   💾 Saved enhanced image: test_enhanced.png")
                print()
                
                print("=" * 60)
                print("✅ Test Complete!")
                print("=" * 60)
                print()
                print("Files created:")
                print("  - test_original.png  (input pattern)")
                print("  - test_drawing.png   (user's drawing)")
                print("  - test_enhanced.png  (AI-enhanced result)")
                print()
                return True
            else:
                print("   ⚠️  No enhanced image in response")
                return False
        else:
            print(f"   ❌ Request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⚠️  Request timed out (this can happen on first request)")
        print("   The models are loading. Try again in a minute.")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhance_endpoint()
    sys.exit(0 if success else 1)

