"""API routes for dental diagnosis."""

import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Optional

from app.config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from app.preprocessing import preprocess_image, validate_image, create_heatmap, enhance_xray
from app.models.dental_model import get_model


router = APIRouter(prefix="/api", tags=["diagnosis"])


class PredictionResponse(BaseModel):
    """Response model for prediction."""
    success: bool
    prediction: str
    confidence: float
    confidence_scores: Dict[str, float]
    image_id: str
    message: Optional[str] = None
    heatmap_url: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    model_config = {"protected_namespaces": ()}

    status: str
    message: str
    model_loaded: bool


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the API
    """
    try:
        model = get_model()
        model_loaded = model.model is not None
        return HealthResponse(
            status="healthy",
            message="Dental diagnosis API is running",
            model_loaded=model_loaded
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Error: {str(e)}",
            model_loaded=False
        )


@router.post("/diagnose", response_model=PredictionResponse)
async def diagnose_image(file: UploadFile = File(...)):
    """
    Diagnose dental X-ray image.

    Args:
        file: Uploaded image file

    Returns:
        Prediction results with confidence scores
    """
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower() if file.filename else ""
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error reading file: {str(e)}"
        )

    # Validate image
    is_valid, error_message = validate_image(file_content, MAX_FILE_SIZE)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)

    # Generate unique ID for this image
    image_id = str(uuid.uuid4())

    # Save uploaded file
    upload_path = UPLOAD_DIR / f"{image_id}{file_ext}"
    try:
        with open(upload_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )

    try:
        # Preprocess image
        preprocessed = preprocess_image(str(upload_path))

        # Get model and make prediction
        model = get_model()
        confidence_scores, predicted_class, max_confidence = model.predict(preprocessed)

        # Create heatmap
        heatmap_path = UPLOAD_DIR / f"{image_id}_heatmap.png"
        import numpy as np
        prediction_array = np.array([[confidence_scores[label] for label in sorted(confidence_scores.keys())]])
        create_heatmap(str(upload_path), prediction_array, str(heatmap_path))

        # Prepare response
        response = PredictionResponse(
            success=True,
            prediction=predicted_class,
            confidence=max_confidence,
            confidence_scores=confidence_scores,
            image_id=image_id,
            message=_get_diagnosis_message(predicted_class, max_confidence),
            heatmap_url=f"/api/image/{image_id}_heatmap.png"
        )

        return response

    except Exception as e:
        # Clean up uploaded file on error
        if upload_path.exists():
            upload_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@router.get("/image/{image_name}")
async def get_image(image_name: str):
    """
    Retrieve processed image.

    Args:
        image_name: Name of the image file

    Returns:
        Image file
    """
    image_path = UPLOAD_DIR / image_name

    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)


def _get_diagnosis_message(prediction: str, confidence: float) -> str:
    """
    Generate user-friendly diagnosis message.

    Args:
        prediction: Predicted class
        confidence: Confidence score

    Returns:
        Diagnosis message
    """
    if prediction == "healthy":
        if confidence > 0.8:
            return "The dental X-ray appears healthy with no signs of cavities or gum disease."
        else:
            return "The dental X-ray appears mostly healthy, but consider a professional examination."
    elif prediction == "cavity":
        if confidence > 0.8:
            return "Potential cavity detected. Please consult with a dentist for proper diagnosis and treatment."
        else:
            return "Possible cavity detected. Recommend professional dental examination for confirmation."
    elif prediction == "gum_disease":
        if confidence > 0.8:
            return "Signs of gum disease detected. Please schedule an appointment with your dentist."
        else:
            return "Possible gum disease indicators. Recommend professional dental consultation."
    else:
        return "Analysis complete. Please consult with a dental professional for proper diagnosis."
