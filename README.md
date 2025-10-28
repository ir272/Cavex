# Dental Diagnosis AI

An AI-powered dental X-ray analysis application for detecting cavities and gum disease. Built with React, TypeScript, Vite, and FastAPI with TensorFlow/Keras for machine learning.

## Features

- **Image Upload**: Drag-and-drop or click to upload dental X-ray images
- **ML-Powered Analysis**: Uses a pre-trained MobileNetV2-based model for classification
- **Real-time Results**: Instant diagnosis with confidence scores
- **Visual Heatmaps**: Highlights problem areas on X-ray images
- **Detailed Breakdown**: Shows confidence scores for all three categories:
  - Healthy
  - Cavity Detection
  - Gum Disease Detection
- **Modern UI**: Responsive design with gradient backgrounds and smooth animations

## Technology Stack

### Frontend
- **React 19.1.1** - Latest React features with React Compiler
- **TypeScript 5.9.3** - Type-safe development
- **Vite 7.1.7** - Fast build tool and dev server
- **CSS3** - Custom styling with modern CSS features

### Backend
- **FastAPI** - High-performance Python web framework
- **TensorFlow 2.18** - Deep learning framework
- **MobileNetV2** - Efficient CNN architecture (pre-trained on ImageNet)
- **OpenCV** - Image preprocessing and enhancement
- **Pillow** - Image validation and processing

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **pip** (Python package manager)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd Gallery
```

#### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Set Up Frontend

```bash
# Navigate back to root directory
cd ..

# Install dependencies
npm install
```

### Running the Application

#### Terminal 1: Start Backend

```bash
cd backend
source venv/bin/activate  # If not already activated
python main.py
```

#### Terminal 2: Start Frontend

```bash
# From project root
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

## Important Disclaimers

⚠️ **Educational Purpose Only**: This application is for educational and demonstration purposes only.

⚠️ **Not for Medical Use**: Do NOT use this tool for actual medical diagnosis. Always consult with a qualified dental professional.

⚠️ **Model Limitations**: The demo model is not trained on real dental X-ray data and should not be relied upon for any diagnostic purposes.

## Development

### Build for Production

```bash
# Build frontend
npm run build

# Preview production build
npm run preview

# Backend is production-ready by default
```

### Linting

```bash
npm run lint
```

### Type Checking

```bash
npm run build  # TypeScript compilation happens before Vite build
```

## Configuration

### Backend Configuration
Edit `backend/app/config.py` to modify:
- Upload directory
- Model path
- Image size
- Confidence thresholds
- CORS origins

### Frontend Configuration
Edit `src/App.tsx` to change:
- API URL (currently `http://localhost:8000`)

## Troubleshooting

### Backend Issues

**ImportError: No module named 'tensorflow'**
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt`

**CORS errors**
- Check that the frontend URL is in `ALLOWED_ORIGINS` in `backend/app/config.py`

### Frontend Issues

**Cannot connect to backend**
- Ensure backend is running on port 8000
- Check API_URL in `src/App.tsx`

**TypeScript errors**
- Run `npm run build` to see detailed errors
- Check that all imports use `type` keyword for type-only imports

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
