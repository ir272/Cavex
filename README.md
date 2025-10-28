# Cavex

AI-powered dental X-ray analysis for detecting cavities and gum disease.

<img width="1344" height="893" alt="image" src="https://github.com/user-attachments/assets/29411369-f1b7-4a50-ac46-47f0b8913793" />


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

## Model Information

Architecture: MobileNetV2 (ImageNet pre-trained) + custom dense layers
Output: 3-class classification (Healthy, Cavity, Gum Disease)
Preprocessing: Resize to 224x224 → RGB normalization → CLAHE enhancement

## Future Enhancements

- [ ] Train model on real dental X-ray dataset
- [ ] Add user authentication & diagnosis history

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
