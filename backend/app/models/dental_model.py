"""Dental diagnosis ML model."""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
from typing import Dict, Tuple
from app.config import MODEL_PATH, IMAGE_SIZE, NUM_CLASSES, CLASS_LABELS


class DentalDiagnosisModel:
    """Dental diagnosis model for detecting cavities and gum disease."""

    def __init__(self, model_path: Path = MODEL_PATH):
        """
        Initialize the dental diagnosis model.

        Args:
            model_path: Path to saved model weights
        """
        self.model_path = model_path
        self.model = None
        self.load_or_create_model()

    def create_model(self) -> keras.Model:
        """
        Create a CNN-based model for dental diagnosis.

        Returns:
            Compiled Keras model
        """
        # Use MobileNetV2 as base model (efficient for deployment)
        base_model = keras.applications.MobileNetV2(
            input_shape=(*IMAGE_SIZE, 3),
            include_top=False,
            weights='imagenet'
        )

        # Freeze base model layers
        base_model.trainable = False

        # Build model
        inputs = keras.Input(shape=(*IMAGE_SIZE, 3))

        # Preprocessing
        x = keras.applications.mobilenet_v2.preprocess_input(inputs * 255.0)

        # Base model
        x = base_model(x, training=False)

        # Custom top layers
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

        model = keras.Model(inputs, outputs)

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def load_or_create_model(self):
        """Load existing model or create a new one."""
        if self.model_path.exists():
            try:
                print(f"Loading model from {self.model_path}")
                self.model = keras.models.load_model(self.model_path)
                print("Model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Creating new model...")
                self.model = self.create_model()
                # Initialize with random predictions (simulate trained model)
                self._initialize_demo_weights()
        else:
            print("No saved model found. Creating new model...")
            self.model = self.create_model()
            # Initialize with random predictions (simulate trained model)
            self._initialize_demo_weights()

    def _initialize_demo_weights(self):
        """
        Initialize model for demo purposes.
        In production, this should be replaced with actual training.
        """
        print("Initializing demo model (not trained on real data)")
        # The model is already initialized with ImageNet weights
        # For demo, we'll use it as-is

    def predict(self, preprocessed_image: np.ndarray) -> Tuple[Dict[str, float], str, float]:
        """
        Make prediction on preprocessed image.

        Args:
            preprocessed_image: Preprocessed image array

        Returns:
            Tuple of (confidence_scores_dict, predicted_class, max_confidence)
        """
        # Get model predictions
        predictions = self.model.predict(preprocessed_image, verbose=0)

        # Convert to probabilities dict
        confidence_scores = {}
        for idx, label in CLASS_LABELS.items():
            confidence_scores[label] = float(predictions[0][idx])

        # Get predicted class
        predicted_idx = int(np.argmax(predictions[0]))
        predicted_class = CLASS_LABELS[predicted_idx]
        max_confidence = float(predictions[0][predicted_idx])

        return confidence_scores, predicted_class, max_confidence

    def save_model(self):
        """Save the model to disk."""
        if self.model:
            self.model.save(self.model_path)
            print(f"Model saved to {self.model_path}")

    def train(self, train_data, validation_data, epochs: int = 10):
        """
        Train the model (placeholder for actual training).

        Args:
            train_data: Training dataset
            validation_data: Validation dataset
            epochs: Number of training epochs
        """
        if not self.model:
            self.model = self.create_model()

        # Unfreeze some layers for fine-tuning
        base_model = self.model.layers[2]
        base_model.trainable = True

        # Freeze early layers
        for layer in base_model.layers[:100]:
            layer.trainable = False

        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        # Train
        history = self.model.fit(
            train_data,
            validation_data=validation_data,
            epochs=epochs,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=3,
                    restore_best_weights=True
                ),
                keras.callbacks.ReduceLROnPlateau(
                    monitor='val_loss',
                    factor=0.5,
                    patience=2,
                    min_lr=1e-7
                )
            ]
        )

        return history


# Global model instance
_model_instance = None


def get_model() -> DentalDiagnosisModel:
    """Get or create the global model instance."""
    global _model_instance
    if _model_instance is None:
        _model_instance = DentalDiagnosisModel()
    return _model_instance
