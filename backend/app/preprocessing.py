"""Image preprocessing utilities for dental X-ray analysis."""

import io
import cv2
import numpy as np
from PIL import Image
from typing import Tuple
from app.config import IMAGE_SIZE


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess dental X-ray image for model inference.

    Args:
        image_path: Path to the image file

    Returns:
        Preprocessed image array ready for model input
    """
    # Read image
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize to model input size
    img = cv2.resize(img, IMAGE_SIZE, interpolation=cv2.INTER_AREA)

    # Normalize pixel values to [0, 1]
    img = img.astype(np.float32) / 255.0

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    # This enhances contrast in dental X-rays
    img_lab = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_lab[:, :, 0] = clahe.apply(img_lab[:, :, 0])
    img = cv2.cvtColor(img_lab, cv2.COLOR_LAB2RGB).astype(np.float32) / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    return img


def enhance_xray(image_path: str, output_path: str) -> str:
    """
    Enhance dental X-ray for better visualization.

    Args:
        image_path: Path to input image
        output_path: Path to save enhanced image

    Returns:
        Path to enhanced image
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(img)

    # Apply denoising
    enhanced = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)

    # Save enhanced image
    cv2.imwrite(output_path, enhanced)

    return output_path


def create_heatmap(image_path: str, prediction: np.ndarray, output_path: str) -> str:
    """
    Create a heatmap overlay showing areas of concern.

    Args:
        image_path: Path to original image
        prediction: Model prediction array
        output_path: Path to save heatmap

    Returns:
        Path to heatmap image
    """
    # Read original image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (512, 512))

    # Create a simple gradient heatmap based on confidence
    # In a real application, this would use GradCAM or similar technique
    confidence = float(np.max(prediction))
    predicted_class = int(np.argmax(prediction))

    # Only create heatmap for problematic predictions
    if predicted_class > 0 and confidence > 0.5:
        # Create red overlay
        heatmap = np.zeros_like(img)
        heatmap[:, :, 0] = 255  # Red channel

        # Apply gaussian blur for smooth gradient
        heatmap = cv2.GaussianBlur(heatmap, (0, 0), sigmaX=50, sigmaY=50)

        # Blend with original image
        alpha = confidence * 0.4
        overlay = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)
    else:
        overlay = img

    # Convert back to BGR for saving
    overlay = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, overlay)

    return output_path


def validate_image(file_content: bytes, max_size: int) -> Tuple[bool, str]:
    """
    Validate uploaded image file.

    Args:
        file_content: Image file content in bytes
        max_size: Maximum allowed file size in bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    if len(file_content) > max_size:
        return False, f"File size exceeds maximum allowed size of {max_size / (1024*1024)}MB"

    # Try to open as image
    try:
        img = Image.open(io.BytesIO(file_content))
        img.verify()

        # Check if image format is supported
        if img.format.lower() not in ['jpeg', 'jpg', 'png', 'bmp']:
            return False, f"Unsupported image format: {img.format}"

        # Check image dimensions (should be reasonable)
        width, height = img.size
        if width < 100 or height < 100:
            return False, "Image dimensions too small (minimum 100x100)"
        if width > 5000 or height > 5000:
            return False, "Image dimensions too large (maximum 5000x5000)"

        return True, ""

    except Exception as e:
        return False, f"Invalid image file: {str(e)}"
