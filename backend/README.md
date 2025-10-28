# Backend - Dental Diagnosis API

FastAPI-based backend for dental X-ray analysis with TensorFlow/Keras ML models.

## Architecture

### Components

1. **FastAPI Application** (`main.py`)
   - RESTful API server
   - CORS middleware for frontend communication
   - Automatic OpenAPI documentation

2. **ML Model** (`app/models/dental_model.py`)
   - MobileNetV2-based CNN
   - Transfer learning from ImageNet
   - 3-class classification (healthy, cavity, gum_disease)

3. **Image Preprocessing** (`app/preprocessing.py`)
   - Image validation and resizing
   - CLAHE enhancement for X-rays
   - Heatmap generation

4. **API Routes** (`app/routes/diagnosis.py`)
   - `/api/health` - Health check
   - `/api/diagnose` - Image upload and analysis
   - `/api/image/{name}` - Retrieve processed images

5. **Configuration** (`app/config.py`)
   - Centralized settings
   - Path management
   - Model hyperparameters

## Setup

### Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Dependencies

- **FastAPI** - Web framework
- **uvicorn** - ASGI server
- **TensorFlow** - Deep learning
- **OpenCV** - Image processing
- **Pillow** - Image handling
- **NumPy** - Numerical operations
- **pydantic** - Data validation

## Running

### Development

```bash
python main.py
```

Server starts at: `http://localhost:8000`

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Model Training

### Preparing Dataset

To train on real dental X-ray data:

```python
# Example training script
import tensorflow as tf
from app.models.dental_model import DentalDiagnosisModel

# Load your dataset
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'path/to/train',
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'path/to/train',
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

# Train model
model = DentalDiagnosisModel()
history = model.train(train_ds, val_ds, epochs=20)
model.save_model()
```

### Dataset Structure

```
dataset/
├── train/
│   ├── healthy/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   ├── cavity/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── gum_disease/
│       ├── img1.jpg
│       └── img2.jpg
└── test/
    └── (same structure)
```

## Image Preprocessing Pipeline

### Input Requirements
- Format: JPEG, PNG, or BMP
- Size: 100x100 to 5000x5000 pixels
- Max file size: 10MB

### Processing Steps
1. **Validation**: Check format, size, dimensions
2. **Resize**: Scale to 224x224
3. **Normalization**: Pixel values to [0, 1]
4. **CLAHE**: Enhance contrast for X-rays
5. **Batch**: Add batch dimension for model input

## Configuration

### Environment Variables

You can override settings with environment variables:

```bash
export MODEL_PATH=/path/to/model.h5
export UPLOAD_DIR=/path/to/uploads
export MAX_FILE_SIZE=10485760
```

### Config File

Edit `app/config.py` to modify:

```python
IMAGE_SIZE = (224, 224)          # Model input size
CONFIDENCE_THRESHOLD = 0.5       # Minimum confidence
NUM_CLASSES = 3                  # Output classes
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad request (invalid file, size exceeded)
- `404` - Resource not found
- `500` - Server error (processing failed)

Error response format:
```json
{
  "detail": "Error message here"
}
```

## Performance Optimization

### For Production

1. **Use GPU**: Install `tensorflow-gpu` for faster inference
2. **Model Quantization**: Reduce model size
3. **Caching**: Cache preprocessed images
4. **Load Balancing**: Run multiple workers
5. **CDN**: Serve static images via CDN

### Model Optimization

```python
# Convert to TensorFlow Lite for mobile/edge deployment
converter = tf.lite.TFLiteConverter.from_keras_model(model.model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
```

## Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Upload image
curl -X POST http://localhost:8000/api/diagnose \
  -F "file=@sample.jpg"
```

### Unit Tests

Create `tests/test_api.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## Security Considerations

1. **File Validation**: Only accept image files
2. **Size Limits**: Enforce max file size
3. **Rate Limiting**: Add rate limiting in production
4. **HTTPS**: Use HTTPS in production
5. **API Keys**: Consider API key authentication
6. **CORS**: Configure allowed origins properly

## Monitoring

### Logging

Add logging to track requests:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In your endpoints
logger.info(f"Processing image: {image_id}")
```

### Metrics

Track:
- Request count
- Response times
- Error rates
- Model inference time
- Upload sizes

## Troubleshooting

### TensorFlow Installation Issues

**macOS M1/M2**:
```bash
pip install tensorflow-macos
pip install tensorflow-metal  # For GPU acceleration
```

**CUDA GPU Support**:
```bash
pip install tensorflow-gpu
# Ensure CUDA and cuDNN are installed
```

### Memory Issues

If running out of memory:
1. Reduce batch size
2. Use model quantization
3. Clear uploads directory regularly
4. Implement memory limits

### Import Errors

```bash
# If modules not found
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

## Development Tips

1. **Auto-reload**: Use `--reload` flag during development
   ```bash
   uvicorn main:app --reload
   ```

2. **Debug Mode**: Enable FastAPI debug mode
   ```python
   app = FastAPI(debug=True)
   ```

3. **Interactive Testing**: Use `/docs` endpoint for API testing

## License

MIT License
