"""Configuration settings for the dental diagnosis application."""

from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Upload settings
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
SAMPLE_DATA_DIR.mkdir(exist_ok=True)

# Model settings
MODEL_DIR = BASE_DIR / "app" / "models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "dental_model.h5"

# Image settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}
IMAGE_SIZE = (224, 224)  # Input size for the model

# Model settings
CONFIDENCE_THRESHOLD = 0.5
NUM_CLASSES = 3  # healthy, cavity, gum_disease

# Class labels
CLASS_LABELS = {
    0: "healthy",
    1: "cavity",
    2: "gum_disease"
}

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite default dev server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
