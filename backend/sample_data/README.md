# Sample Data

This directory is for storing sample dental X-ray images for testing and demonstration purposes.

## Adding Sample Data

### Where to Find Sample Dental X-rays

**Important**: Only use images that are:
- Publicly available
- Licensed for use
- Anonymized (no patient information)

### Recommended Sources

1. **Public Datasets**:
   - Kaggle: Search for "dental x-ray dataset"
   - Academic papers with public datasets
   - Medical imaging repositories

2. **Test Images**:
   - Create synthetic test images
   - Use stock medical imagery (with proper licenses)

### File Organization

```
sample_data/
├── healthy/
│   ├── healthy_1.jpg
│   ├── healthy_2.jpg
│   └── ...
├── cavity/
│   ├── cavity_1.jpg
│   ├── cavity_2.jpg
│   └── ...
└── gum_disease/
    ├── gum_disease_1.jpg
    ├── gum_disease_2.jpg
    └── ...
```

## Image Requirements

- **Format**: JPEG, PNG, or BMP
- **Size**: Recommended 500x500 to 2000x2000 pixels
- **Quality**: High resolution for better analysis
- **Content**: Clear dental X-ray images
- **Privacy**: No patient identifying information

## Using Sample Data

### For Testing

```python
from pathlib import Path
from app.preprocessing import preprocess_image
from app.models.dental_model import get_model

# Load sample image
sample_path = Path("sample_data/healthy/healthy_1.jpg")

# Preprocess
preprocessed = preprocess_image(str(sample_path))

# Predict
model = get_model()
scores, prediction, confidence = model.predict(preprocessed)
print(f"Prediction: {prediction} ({confidence:.2%})")
```

### For Training

```python
import tensorflow as tf

# Load dataset from sample_data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'sample_data',
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)
```

## Disclaimer

The sample data in this directory is for **educational and testing purposes only**.

- Do NOT use for actual medical diagnosis
- Ensure proper licensing for any images you add
- Respect patient privacy and medical ethics
- Follow all applicable regulations (HIPAA, GDPR, etc.)

## Contributing Sample Data

If you have access to appropriate dental X-ray datasets:

1. Ensure you have permission to share
2. Anonymize all patient information
3. Organize by category (healthy, cavity, gum_disease)
4. Include source attribution if required by license
5. Document any preprocessing done to the images

## Legal Notice

Users of this application are responsible for ensuring they have appropriate rights to use any images they upload or add to this directory. The authors of this software assume no liability for improper use of medical imagery.
