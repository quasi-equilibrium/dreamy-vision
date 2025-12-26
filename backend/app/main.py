"""
Dreamy Vision - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
import io
from PIL import Image

from app.models.enhancer import ImageEnhancer

app = FastAPI(title="Dreamy Vision API")

# CORS middleware for web demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize enhancer (lazy loading)
enhancer = None

def get_enhancer():
    global enhancer
    if enhancer is None:
        enhancer = ImageEnhancer()
    return enhancer


class EnhanceRequest(BaseModel):
    original_image: str  # base64 encoded
    user_drawing: str    # base64 encoded
    description: str
    enhancement_strength: float = 0.3


class EnhanceResponse(BaseModel):
    enhanced_image: str  # base64 encoded
    processing_time: float


@app.get("/")
async def root():
    return {"message": "Dreamy Vision API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/enhance", response_model=EnhanceResponse)
async def enhance_image(request: EnhanceRequest):
    """
    Enhance pattern image using user's drawing as guidance
    """
    try:
        import time
        start_time = time.time()
        
        # Decode images
        original_img = decode_base64_image(request.original_image)
        drawing_img = decode_base64_image(request.user_drawing)
        
        # Get enhancer
        enhancer = get_enhancer()
        
        # Enhance image
        enhanced_img = enhancer.enhance(
            original_image=original_img,
            user_drawing=drawing_img,
            description=request.description,
            enhancement_strength=request.enhancement_strength
        )
        
        # Encode result
        enhanced_base64 = encode_image_to_base64(enhanced_img)
        
        processing_time = time.time() - start_time
        
        return EnhanceResponse(
            enhanced_image=enhanced_base64,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")


def decode_base64_image(base64_str: str) -> Image.Image:
    """Decode base64 string to PIL Image"""
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        return image.convert('RGB')
    except Exception as e:
        raise ValueError(f"Invalid image data: {str(e)}")


def encode_image_to_base64(image: Image.Image) -> str:
    """Encode PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    return base64.b64encode(image_data).decode('utf-8')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

