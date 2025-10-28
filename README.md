# Dental Diagnosis AI

AI-powered dental X-ray analysis for detecting cavities and gum disease.

## Features
* Drag-and-drop X-ray image upload
* ML-powered analysis with confidence scores
* Visual heatmaps highlighting problem areas
* Detects: Healthy teeth, Cavities, Gum Disease
* Responsive modern UI

## Tech Stack

**Frontend:** React 19 • TypeScript • Vite

**Backend:** FastAPI • TensorFlow 2.18 • MobileNetV2 • OpenCV

## Getting Started

**Prerequisites:** Node.js 18+ • Python 3.9+ • pip

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Gallery

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ..
npm install
```

### Running the App

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

## Usage

1. **Upload X-ray**: Click the upload area or drag and drop a dental X-ray image
2. **Analyze**: Click the "Analyze X-ray" button
3. **View Results**: See the diagnosis with:
   - Overall prediction (Healthy, Cavity, or Gum Disease)
   - Confidence score
   - Detailed breakdown for all categories
   - Visual comparison with heatmap overlay

## API Endpoints

### Health Check
```http
GET /api/health
```

Returns the health status and model loading state.

### Diagnose Image
```http
POST /api/diagnose
```

Upload and analyze a dental X-ray image.

**Request**: `multipart/form-data` with `file` field

**Response**:
```json
{
  "success": true,
  "prediction": "healthy",
  "confidence": 0.87,
  "confidence_scores": {
    "healthy": 0.87,
    "cavity": 0.08,
    "gum_disease": 0.05
  },
  "image_id": "uuid",
  "message": "Diagnosis message",
  "heatmap_url": "/api/image/uuid_heatmap.png"
}
```

### Get Image
```http
GET /api/image/{image_name}
```

Retrieve processed images (original or heatmap).

## Model Information

### Architecture
- **Base Model**: MobileNetV2 (pre-trained on ImageNet)
- **Custom Layers**: Global Average Pooling + Dense layers
- **Output**: 3-class softmax (healthy, cavity, gum_disease)
- **Input Size**: 224x224 RGB images

### Preprocessing Pipeline
1. Resize to 224x224
2. RGB normalization
3. CLAHE (Contrast Limited Adaptive Histogram Equalization)
4. Batch dimension expansion

### Training (For Production)
The current model uses MobileNetV2 with ImageNet weights as a demo. For production:

1. Collect labeled dental X-ray dataset
2. Split into train/validation/test sets
3. Use the `train()` method in `DentalDiagnosisModel`
4. Fine-tune the model on your dataset
5. Save weights with `save_model()`

## Disclaimers

⚠️ **Not for Medical Use**: Do NOT use this tool for actual medical diagnosis. Always consult with a qualified dental professional.

⚠️ **Model Limitations**: The demo model is not trained on real dental X-ray data and should not be relied upon for any diagnostic purposes.

## Future Enhancements

- [ ] Train model on real dental X-ray dataset
- [ ] Add user authentication
- [ ] Store diagnosis history
- [ ] Generate PDF reports
- [ ] Support for multiple X-ray views
- [ ] Integration with DICOM format
- [ ] More detailed segmentation and annotation
- [ ] Multi-language support

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
