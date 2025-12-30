"""
Dreamy Vision - Image Processing Utilities
"""

from PIL import Image
import numpy as np
import cv2


def preprocess_image(image: Image.Image, max_size: int = 512, target_size: int = 512, force_square: bool = True) -> Image.Image:
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
    
    # If image is already target size, return as-is (user cropped it)
    if new_width == target_size and new_height == target_size:
        return image
    
    # Pad to square if needed (for SD 1.5)
    if force_square and (new_width != target_size or new_height != target_size):
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


def create_inpaint_mask(drawing: Image.Image, target_size: tuple, expand: int = 10) -> Image.Image:
    """
    Create a binary mask for inpainting from user's drawing
    Only the area where user drew will be enhanced
    
    Args:
        drawing: User's drawing (PIL Image)
        target_size: Target size (width, height)
        expand: Pixels to expand mask for smooth blending
    
    Returns:
        Binary mask (white = enhance, black = preserve)
    """
    # Resize drawing to match target size
    drawing = drawing.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    drawing_array = np.array(drawing)
    
    # Convert to grayscale
    if len(drawing_array.shape) == 3:
        gray = cv2.cvtColor(drawing_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = drawing_array
    
    # Create mask: anywhere user drew (non-black pixels)
    # Use lower threshold to catch lighter drawings
    # Invert: black background = 0, white drawing = 255
    _, mask = cv2.threshold(gray, 5, 255, cv2.THRESH_BINARY)
    
    # If mask is mostly black (user drew on black background), we need to check
    # If most pixels are black, the drawing might be white/colored on black
    # In that case, we want non-black pixels
    white_pixels = np.sum(mask > 0)
    if white_pixels < (mask.size * 0.01):  # Less than 1% white
        # Drawing might be on black background, invert threshold
        _, mask = cv2.threshold(255 - gray, 5, 255, cv2.THRESH_BINARY)
    
    # Expand mask slightly for smooth blending
    if expand > 0:
        kernel = np.ones((expand, expand), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        # Smooth edges
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Convert to PIL Image (white = enhance area, black = preserve)
    mask_image = Image.fromarray(mask).convert('L')
    
    return mask_image

