# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack dental diagnosis application combining:
- **Frontend**: React 19 + TypeScript + Vite (modern UI with strict typing)
- **Backend**: Python FastAPI + TensorFlow/Keras (ML-powered diagnosis)

The application uses AI to analyze dental X-ray images and detect cavities and gum disease.

## Development Commands

### Frontend Commands
- `npm run dev` - Start Vite development server at http://localhost:5173
- `npm run build` - Compile TypeScript (`tsc -b`) and build for production
- `npm run lint` - Run ESLint on the codebase
- `npm run preview` - Preview the production build locally

### Backend Commands
```bash
cd backend
source venv/bin/activate  # Activate virtual environment first
python main.py  # Start FastAPI server at http://localhost:8000
```

### Backend Setup (First Time)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Architecture

### Frontend Structure
```
src/
├── components/
│   ├── ImageUpload.tsx      - Drag-and-drop image upload
│   ├── DiagnosisResults.tsx - Results display with charts
│   └── *.css                - Component styles
├── types.ts                 - TypeScript type definitions
├── App.tsx                  - Main application component
├── main.tsx                 - React 19 entry point
└── *.css                    - Global styles
```

### Backend Structure
```
backend/
├── app/
│   ├── models/
│   │   └── dental_model.py  - TensorFlow/Keras ML model
│   ├── routes/
│   │   └── diagnosis.py     - API endpoints
│   ├── config.py            - Configuration settings
│   └── preprocessing.py     - Image processing utilities
├── main.py                  - FastAPI application entry
├── requirements.txt         - Python dependencies
├── uploads/                 - Uploaded images (gitignored)
└── sample_data/            - Sample dental X-rays
```

## Technology Stack

### Frontend
- **React 19.1.1** - Uses React Compiler, StrictMode, and createRoot API
- **TypeScript 5.9.3** - Strict mode with comprehensive linting
- **Vite 7.1.7** - Fast build tool and dev server with HMR
- **CSS3** - Custom styling with gradients and animations

### Backend
- **FastAPI** - High-performance async Python web framework
- **TensorFlow 2.18** - Deep learning framework
- **MobileNetV2** - Pre-trained CNN base model
- **OpenCV** - Image preprocessing and CLAHE enhancement
- **Pillow** - Image validation
- **Uvicorn** - ASGI server

## Key Development Practices

### TypeScript Strictness
- `verbatimModuleSyntax: true` - Must use `type` keyword for type-only imports
  ```typescript
  import type { DiagnosisResult } from './types';  // Correct
  import { DiagnosisResult } from './types';       // Error
  ```
- `erasableSyntaxOnly: true` - React 19 Compiler requirement
- All unused locals/parameters cause build errors
- TypeScript must compile before Vite build runs

### API Integration
- Frontend connects to backend at `http://localhost:8000`
- CORS configured for `http://localhost:5173` (Vite default)
- API endpoints:
  - `GET /api/health` - Health check
  - `POST /api/diagnose` - Upload and analyze X-ray
  - `GET /api/image/{name}` - Retrieve processed images

### ML Model
- Uses transfer learning from MobileNetV2 (ImageNet weights)
- Input: 224x224 RGB images
- Output: 3-class softmax (healthy, cavity, gum_disease)
- Preprocessing: resize → normalize → CLAHE → batch dimension
- Model auto-initializes on first request (downloads ImageNet weights)

## Running the Application

**Both servers must run simultaneously:**

1. **Terminal 1 - Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

2. **Terminal 2 - Frontend**:
   ```bash
   npm run dev
   ```

3. Open browser to `http://localhost:5173`

## Common Tasks

### Adding New API Endpoints
1. Define route in `backend/app/routes/diagnosis.py`
2. Add request/response models using Pydantic
3. Update frontend API calls in `src/App.tsx`
4. Handle CORS if needed in `backend/app/config.py`

### Modifying ML Model
1. Edit `backend/app/models/dental_model.py`
2. Update `IMAGE_SIZE` or `NUM_CLASSES` in `backend/app/config.py`
3. Retrain model using the `train()` method
4. Save with `model.save_model()`

### Adding Frontend Components
1. Create `.tsx` file in `src/components/`
2. Create matching `.css` file
3. Use `type` imports for all type-only imports
4. Export as default or named export
5. Import in `App.tsx`

## Configuration Files

### Backend Config (`backend/app/config.py`)
- Upload directory paths
- Model hyperparameters
- Image size and validation rules
- CORS allowed origins

### Frontend Config
- API URL: Defined in `src/App.tsx` as `API_URL` constant
- For production, change to actual backend URL

## Important Constraints

### TypeScript
- Type imports MUST use `import type` syntax
- No unused variables allowed
- Strict null checks enforced
- All React Hooks rules enforced

### Python
- FastAPI async/await patterns
- Pydantic models for validation
- Type hints required for all functions
- Virtual environment required for dependencies

### ML Model
- First run downloads ~14MB ImageNet weights
- Inference time: ~100-500ms per image
- GPU acceleration available with tensorflow-gpu
- Model not trained on real dental data (demo only)

## Troubleshooting

### Frontend
- **CORS errors**: Check `ALLOWED_ORIGINS` in backend config
- **Type errors**: Use `import type` for type-only imports
- **Build fails**: Run `npm run lint` to see ESLint errors

### Backend
- **Import errors**: Activate virtual environment
- **TensorFlow errors**: Ensure compatible Python version (3.9-3.11)
- **Port in use**: Backend defaults to port 8000, ensure it's free

## Important Disclaimers

This application is for **educational purposes only**:
- Not trained on real dental X-ray data
- Not for medical diagnosis
- Demo model uses generic ImageNet features
- Always consult dental professionals for real diagnosis
