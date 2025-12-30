"""
Dreamy Vision - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import base64
import io
from PIL import Image

from app.models.enhancer import ImageEnhancer
from app.models.llm_service import get_llm_service

app = FastAPI(title="Dreamy Vision API")

# CORS middleware for web demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize enhancer and LLM service (lazy loading)
enhancer = None
llm_service = None

def get_enhancer(llm_backend: str = "ollama"):
    global enhancer
    if enhancer is None:
        enhancer = ImageEnhancer(llm_backend=llm_backend)
    return enhancer

def get_llm():
    global llm_service
    if llm_service is None:
        llm_service = get_llm_service("ollama")
    return llm_service


class EnhanceRequest(BaseModel):
    original_image: str  # base64 encoded
    user_drawing: str    # base64 encoded
    description: str
    enhancement_strength: float = 0.3


class EnhanceResponse(BaseModel):
    enhanced_image: str  # base64 encoded
    processing_time: float


class HintRequest(BaseModel):
    description: str
    num_hints: int = 3


class HintResponse(BaseModel):
    hints: List[str]
    enhanced_prompt: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Dreamy Vision API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/hint", response_model=HintResponse)
async def generate_hints(request: HintRequest):
    """
    Generate AI hints/suggestions for what the user might see
    Returns multiple alternative interpretations
    """
    try:
        llm = get_llm()
        
        # Generate hints
        hints = llm.generate_hints(request.description, request.num_hints)
        
        # Also generate an enhanced prompt
        enhanced_prompt = llm.enhance_prompt(request.description)
        
        return HintResponse(
            hints=hints,
            enhanced_prompt=enhanced_prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hint generation failed: {str(e)}")


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
        
        # Get enhancer (with LLM backend)
        enhancer = get_enhancer(llm_backend="ollama")
        
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
        # Remove data URL prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')
        
        # Validate and limit size
        width, height = image.size
        max_dimension = 2048
        
        if width > max_dimension or height > max_dimension:
            # Resize maintaining aspect ratio
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        return image
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

