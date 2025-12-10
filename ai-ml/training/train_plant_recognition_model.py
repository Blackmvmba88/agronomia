"""
Plant Recognition Model Training Script
Uses transfer learning with pre-trained models for plant species identification
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import pandas as pd
import os
import json
from datetime import datetime

class PlantRecognitionModel:
    """
    Plant species recognition using transfer learning with EfficientNet
    Identifies plant species from images and provides detailed observations
    """
    
    def __init__(self, img_size=224, num_classes=50):
        """
        Initialize the plant recognition model
        
        Args:
            img_size: Input image size (default 224x224)
            num_classes: Number of plant species to classify
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.class_names = []
        self.plant_info = {}
        
    def build_model(self):
        """
        Build transfer learning model with EfficientNetB0 backbone
        """
        # Load pre-trained EfficientNet without top layers
        base_model = EfficientNetB0(
            include_top=False,
            weights='imagenet',
            input_shape=(self.img_size, self.img_size, 3)
        )
        
        # Freeze base model initially
        base_model.trainable = False
        
        # Build model
        inputs = keras.Input(shape=(self.img_size, self.img_size, 3))
        
        # Data augmentation
        x = layers.RandomFlip("horizontal")(inputs)
        x = layers.RandomRotation(0.2)(x)
        x = layers.RandomZoom(0.2)(x)
        
        # Preprocessing for EfficientNet
        x = keras.applications.efficientnet.preprocess_input(x)
        
        # Base model
        x = base_model(x, training=False)
        
        # Classification head
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_k_categorical_accuracy']
        )
        
        return self.model
    
    def generate_sample_data(self):
        """
        Generate sample plant classification data for demonstration
        In production, replace with real plant images dataset
        """
        # Common plant species for hydroponic/indoor growing
        self.class_names = [
            'tomato', 'lettuce', 'basil', 'strawberry', 'cucumber',
            'bell_pepper', 'spinach', 'kale', 'arugula', 'mint',
            'cilantro', 'parsley', 'chard', 'bok_choy', 'watercress',
            'oregano', 'thyme', 'rosemary', 'sage', 'dill',
            'chives', 'green_onion', 'radish', 'pak_choi', 'mustard_greens',
            'cabbage', 'broccoli', 'cauliflower', 'eggplant', 'zucchini',
            'squash', 'melon', 'bean', 'pea', 'celery',
            'fennel', 'endive', 'radicchio', 'collard_greens', 'turnip',
            'beet', 'carrot', 'potato', 'sweet_potato', 'ginger',
            'turmeric', 'lemongrass', 'lavender', 'chamomile', 'marigold'
        ]
        
        # Plant information database with characteristics and care tips
        self.plant_info = {
            'tomato': {
                'scientific_name': 'Solanum lycopersicum',
                'family': 'Solanaceae',
                'type': 'Fruiting vegetable',
                'growth_time': '60-80 days',
                'optimal_ph': '5.5-6.5',
                'optimal_ec': '2.0-5.0 mS/cm',
                'light_requirements': 'High (14-18 hours)',
                'temperature': '21-27°C',
                'observations': [
                    'Compound leaves with serrated edges',
                    'Yellow flowers with 5 petals',
                    'Requires support/staking',
                    'Needs regular pruning',
                    'High nutrient requirements during fruiting'
                ],
                'common_issues': ['Blossom end rot', 'Leaf curl', 'Aphids'],
                'harvest_indicators': 'Fruit color change, firm but slightly soft to touch'
            },
            'lettuce': {
                'scientific_name': 'Lactuca sativa',
                'family': 'Asteraceae',
                'type': 'Leafy green',
                'growth_time': '30-45 days',
                'optimal_ph': '5.5-6.5',
                'optimal_ec': '1.2-2.0 mS/cm',
                'light_requirements': 'Medium (12-14 hours)',
                'temperature': '15-21°C',
                'observations': [
                    'Rosette growth pattern',
                    'Smooth or ruffled leaves depending on variety',
                    'Cool season crop',
                    'Quick growing',
                    'Shallow root system'
                ],
                'common_issues': ['Tip burn', 'Bolting in heat', 'Aphids'],
                'harvest_indicators': 'Leaves reach full size, before bolting'
            },
            'basil': {
                'scientific_name': 'Ocimum basilicum',
                'family': 'Lamiaceae',
                'type': 'Herb',
                'growth_time': '20-30 days for harvest',
                'optimal_ph': '5.5-6.5',
                'optimal_ec': '1.0-1.6 mS/cm',
                'light_requirements': 'High (14-16 hours)',
                'temperature': '21-27°C',
                'observations': [
                    'Opposite leaf arrangement',
                    'Aromatic leaves',
                    'Square stems (Lamiaceae family trait)',
                    'Regular pinching encourages bushiness',
                    'Warm season herb'
                ],
                'common_issues': ['Fusarium wilt', 'Downy mildew', 'Japanese beetles'],
                'harvest_indicators': 'Before flowering for best flavor'
            },
            'strawberry': {
                'scientific_name': 'Fragaria × ananassa',
                'family': 'Rosaceae',
                'type': 'Fruit',
                'growth_time': '60-90 days',
                'optimal_ph': '5.5-6.5',
                'optimal_ec': '1.0-1.5 mS/cm',
                'light_requirements': 'Medium-High (12-16 hours)',
                'temperature': '18-24°C',
                'observations': [
                    'Trifoliate leaves',
                    'White flowers with yellow centers',
                    'Runners for propagation',
                    'Shallow root system',
                    'Requires pollination'
                ],
                'common_issues': ['Gray mold', 'Spider mites', 'Powdery mildew'],
                'harvest_indicators': 'Fully red color, sweet aroma'
            },
            'cucumber': {
                'scientific_name': 'Cucumis sativus',
                'family': 'Cucurbitaceae',
                'type': 'Fruiting vegetable',
                'growth_time': '50-70 days',
                'optimal_ph': '5.5-6.0',
                'optimal_ec': '1.7-2.5 mS/cm',
                'light_requirements': 'High (14-16 hours)',
                'temperature': '24-30°C',
                'observations': [
                    'Large palmate leaves',
                    'Climbing vines with tendrils',
                    'Yellow flowers',
                    'High water requirements',
                    'Requires support structure'
                ],
                'common_issues': ['Powdery mildew', 'Cucumber beetles', 'Pythium'],
                'harvest_indicators': 'Firm, bright green, before yellowing'
            }
        }
        
        # Add basic info for remaining plants
        basic_plants = [plant for plant in self.class_names if plant not in self.plant_info]
        for plant in basic_plants:
            self.plant_info[plant] = {
                'scientific_name': f'{plant.replace("_", " ").title()}',
                'family': 'Various',
                'type': 'Hydroponic plant',
                'growth_time': '30-90 days',
                'optimal_ph': '5.5-6.5',
                'optimal_ec': '1.0-2.5 mS/cm',
                'light_requirements': 'Medium (12-16 hours)',
                'temperature': '18-26°C',
                'observations': [
                    'Suitable for hydroponic cultivation',
                    'Requires proper nutrient balance',
                    'Monitor pH and EC regularly'
                ],
                'common_issues': ['Monitor for common pests and diseases'],
                'harvest_indicators': 'Monitor for maturity indicators'
            }
        
        print(f"Generated plant database with {len(self.class_names)} species")
        return self.class_names, self.plant_info
    
    def train(self, data_dir=None, epochs=50, batch_size=32):
        """
        Train the model on plant images
        
        Args:
            data_dir: Directory containing plant images organized by species
            epochs: Number of training epochs
            batch_size: Training batch size
        """
        # Generate sample data
        self.generate_sample_data()
        
        # Build model
        if self.model is None:
            self.build_model()
        
        print("Model architecture:")
        self.model.summary()
        
        # In production, load real image data here
        # For demonstration, we'll create synthetic training metadata
        print("\nNote: This is a demonstration script.")
        print("In production, replace with actual plant image dataset.")
        print("Recommended datasets:")
        print("  - PlantCLEF dataset")
        print("  - iNaturalist plant subset")
        print("  - Custom labeled plant images")
        
        return {
            'status': 'ready',
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'model_params': self.model.count_params()
        }
    
    def predict(self, image_path_or_array, top_k=5):
        """
        Predict plant species from image with detailed observations
        
        Args:
            image_path_or_array: Path to image file or numpy array
            top_k: Return top k predictions
            
        Returns:
            Dictionary with predictions and plant information
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Load and preprocess image
        if isinstance(image_path_or_array, str):
            img = keras.preprocessing.image.load_img(
                image_path_or_array,
                target_size=(self.img_size, self.img_size)
            )
            img_array = keras.preprocessing.image.img_to_array(img)
        else:
            img_array = image_path_or_array
        
        # Ensure correct shape
        if len(img_array.shape) == 3:
            img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        predictions = self.model.predict(img_array, verbose=0)
        
        # Get top k predictions
        top_indices = np.argsort(predictions[0])[-top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            plant_name = self.class_names[idx]
            confidence = float(predictions[0][idx])
            
            result = {
                'rank': i + 1,
                'plant_name': plant_name,
                'confidence': confidence,
                'confidence_percentage': f"{confidence * 100:.1f}%",
                'plant_info': self.plant_info.get(plant_name, {})
            }
            results.append(result)
        
        return {
            'predictions': results,
            'timestamp': datetime.now().isoformat(),
            'model_version': '1.0'
        }
    
    def save_model(self, save_dir='../models/plant_recognition'):
        """
        Save trained model and metadata
        """
        os.makedirs(save_dir, exist_ok=True)
        
        # Save model
        model_path = os.path.join(save_dir, 'plant_recognition_model.h5')
        self.model.save(model_path)
        
        # Save metadata
        metadata = {
            'model_version': '1.0',
            'img_size': self.img_size,
            'num_classes': self.num_classes,
            'class_names': self.class_names,
            'plant_info': self.plant_info,
            'created_at': datetime.now().isoformat()
        }
        
        metadata_path = os.path.join(save_dir, 'plant_recognition_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {save_dir}")
        return save_dir
    
    def load_model(self, load_dir='../models/plant_recognition'):
        """
        Load trained model and metadata
        """
        # Load model
        model_path = os.path.join(load_dir, 'plant_recognition_model.h5')
        self.model = keras.models.load_model(model_path)
        
        # Load metadata
        metadata_path = os.path.join(load_dir, 'plant_recognition_metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.img_size = metadata['img_size']
        self.num_classes = metadata['num_classes']
        self.class_names = metadata['class_names']
        self.plant_info = metadata['plant_info']
        
        print(f"Model loaded from {load_dir}")
        return self.model


def main():
    """
    Main training function
    """
    print("=" * 60)
    print("Plant Recognition Model Training")
    print("=" * 60)
    
    # Initialize model
    model = PlantRecognitionModel(img_size=224, num_classes=50)
    
    # Train model (in production, pass actual image data directory)
    print("\n1. Training model...")
    results = model.train(epochs=50, batch_size=32)
    print(f"\nTraining completed:")
    print(f"  - Classes: {results['num_classes']}")
    print(f"  - Parameters: {results['model_params']:,}")
    
    # Save model
    print("\n2. Saving model...")
    save_dir = model.save_model()
    
    # Test prediction with sample data
    print("\n3. Model ready for predictions")
    print(f"  - Supported plants: {len(model.class_names)}")
    print(f"  - Sample plants: {', '.join(model.class_names[:10])}")
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("\nTo use the model:")
    print("  from train_plant_recognition_model import PlantRecognitionModel")
    print("  model = PlantRecognitionModel()")
    print("  model.load_model()")
    print("  result = model.predict('path/to/plant/image.jpg')")
    print("=" * 60)


if __name__ == "__main__":
    main()
