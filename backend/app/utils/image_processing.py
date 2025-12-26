"""
Dreamy Vision - Image Processing Utilities
"""

from PIL import Image
import numpy as np
import cv2


def preprocess_image(image: Image.Image, max_size: int = 512, target_size: int = 512) -> Image.Image:
    """
    Preprocess image: resize to max dimension while maintaining aspect ratio,
    then pad/crop to target size if needed
    
    Args:
        image: PIL Image
        max_size: Maximum dimension (maintains aspect ratio)
        target_size: Target size for SD (square)
    
    Returns:
        Processed PIL Image
    """
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Get dimensions
    width, height = image.size
    
    # Resize to max dimension while maintaining aspect ratio
    if width > height:
        if width > max_size:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width, new_height = width, height
    else:
        if height > max_size:
            new_height = max_size
            new_width = int(width * (max_size / height))
        else:
            new_width, new_height = width, height
    
    # Resize
    image = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Pad to square if needed (for SD 1.5)
    if new_width != target_size or new_height != target_size:
        # Create square image with black padding
        square_image = Image.new('RGB', (target_size, target_size), (0, 0, 0))
        
        # Calculate position to center the image
        x_offset = (target_size - new_width) // 2
        y_offset = (target_size - new_height) // 2
        
        square_image.paste(image, (x_offset, y_offset))
        image = square_image
    
    return image


def prepare_drawing_mask(drawing: Image.Image, target_size: tuple) -> Image.Image:
    """
    Prepare user's drawing as a control mask for ControlNet
    
    Args:
        drawing: User's drawing (PIL Image)
        target_size: Target size (width, height)
    
    Returns:
        Processed mask image (Canny edges or line art)
    """
    # Resize drawing to match target size
    drawing = drawing.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    drawing_array = np.array(drawing)
    
    # Convert to grayscale if needed
    if len(drawing_array.shape) == 3:
        gray = cv2.cvtColor(drawing_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = drawing_array
    
    # Apply Canny edge detection to extract clean lines
    edges = cv2.Canny(gray, 50, 150)
    
    # Convert back to PIL Image
    mask_image = Image.fromarray(edges).convert('RGB')
    
    return mask_image

