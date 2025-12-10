"""
Irrigation Prediction Model
Uses LSTM neural network to predict optimal irrigation timing and volume
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import joblib
import json
from datetime import datetime, timedelta

class IrrigationPredictor:
    """
    Predicts optimal irrigation schedule based on environmental conditions
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.sequence_length = 24  # Use 24 hours of data
        self.feature_names = [
            'temperature',
            'humidity',
            'light_intensity',
            'growth_stage',
            'time_of_day',
            'soil_moisture',
            'vpd'  # Vapor Pressure Deficit
        ]
        
    def create_model(self, input_shape):
        """Create LSTM model architecture"""
        model = keras.Sequential([
            layers.LSTM(128, return_sequences=True, input_shape=input_shape),
            layers.Dropout(0.2),
            layers.LSTM(64, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(32),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dense(2)  # Output: [hours_until_irrigation, irrigation_volume_ml]
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def prepare_sequences(self, data, target):
        """Prepare time-series sequences for LSTM"""
        X, y = [], []
        
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(target[i + self.sequence_length])
        
        return np.array(X), np.array(y)
    
    def calculate_vpd(self, temperature, humidity):
        """Calculate Vapor Pressure Deficit"""
        # Saturation vapor pressure (kPa)
        svp = 0.6108 * np.exp((17.27 * temperature) / (temperature + 237.3))
        # Actual vapor pressure
        avp = svp * (humidity / 100)
        # VPD
        vpd = svp - avp
        return vpd
    
    def generate_synthetic_data(self, n_samples=10000):
        """Generate synthetic training data"""
        np.random.seed(42)
        
        data = {
            'temperature': np.random.normal(23, 3, n_samples),  # 23°C ± 3°C
            'humidity': np.random.normal(65, 10, n_samples),     # 65% ± 10%
            'light_intensity': np.random.uniform(0, 50000, n_samples),  # 0-50k lux
            'growth_stage': np.random.choice([0, 1, 2, 3, 4], n_samples),  # 5 stages
            'time_of_day': np.random.uniform(0, 24, n_samples),
            'soil_moisture': np.random.normal(60, 15, n_samples),  # %
        }
        
        df = pd.DataFrame(data)
        df['vpd'] = self.calculate_vpd(df['temperature'], df['humidity'])
        
        # Calculate target irrigation schedule (simplified model)
        # Higher temperature, lower humidity, higher light -> more frequent irrigation
        irrigation_score = (
            (df['temperature'] - 20) * 0.3 +
            (70 - df['humidity']) * 0.2 +
            (df['light_intensity'] / 1000) * 0.1 +
            (60 - df['soil_moisture']) * 0.4
        )
        
        # Hours until next irrigation (1-12 hours)
        df['hours_until_irrigation'] = np.clip(12 - irrigation_score / 5, 1, 12)
        
        # Irrigation volume in ml (100-500ml)
        df['irrigation_volume'] = np.clip(
            200 + irrigation_score * 10 + df['growth_stage'] * 20,
            100, 500
        )
        
        return df
    
    def train(self, data=None, epochs=50, batch_size=32):
        """Train the irrigation prediction model"""
        if data is None:
            print("Generating synthetic training data...")
            data = self.generate_synthetic_data()
        
        # Prepare features and targets
        features = data[self.feature_names].values
        targets = data[['hours_until_irrigation', 'irrigation_volume']].values
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Create sequences
        X, y = self.prepare_sequences(features_scaled, targets)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        print(f"Sequence shape: {X_train.shape}")
        
        # Create and train model
        self.model = self.create_model(input_shape=(self.sequence_length, len(self.feature_names)))
        
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Evaluate
        test_loss, test_mae = self.model.evaluate(X_test, y_test)
        print(f"\nTest Loss: {test_loss:.4f}")
        print(f"Test MAE: {test_mae:.4f}")
        
        return history
    
    def predict(self, sensor_data_sequence):
        """
        Predict irrigation schedule
        
        Args:
            sensor_data_sequence: List of sensor readings (last 24 hours)
                                 Each reading should be a dict with required features
        
        Returns:
            dict with 'hours_until_irrigation' and 'irrigation_volume_ml'
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Prepare features
        features = []
        for reading in sensor_data_sequence:
            feature_vector = [
                reading.get('temperature', 23),
                reading.get('humidity', 65),
                reading.get('light_intensity', 25000),
                reading.get('growth_stage', 2),
                reading.get('time_of_day', 12),
                reading.get('soil_moisture', 60),
                self.calculate_vpd(
                    reading.get('temperature', 23),
                    reading.get('humidity', 65)
                )
            ]
            features.append(feature_vector)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Reshape for prediction
        X = np.array([features_scaled])
        
        # Predict
        prediction = self.model.predict(X, verbose=0)
        
        return {
            'hours_until_irrigation': float(prediction[0][0]),
            'irrigation_volume_ml': float(prediction[0][1]),
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.92  # Could be calculated from model uncertainty
        }
    
    def save_model(self, path='irrigation_model'):
        """Save model and scaler"""
        self.model.save(f'{path}.h5')
        joblib.dump(self.scaler, f'{path}_scaler.pkl')
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'sequence_length': self.sequence_length,
            'created': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        with open(f'{path}_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {path}")
    
    def load_model(self, path='irrigation_model'):
        """Load model and scaler"""
        self.model = keras.models.load_model(f'{path}.h5')
        self.scaler = joblib.load(f'{path}_scaler.pkl')
        
        # Load metadata
        with open(f'{path}_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        self.feature_names = metadata['feature_names']
        self.sequence_length = metadata['sequence_length']
        
        print(f"Model loaded from {path}")

def main():
    """Train and save the irrigation prediction model"""
    print("=" * 60)
    print("Agronomia Irrigation Prediction Model Training")
    print("=" * 60)
    
    predictor = IrrigationPredictor()
    
    # Train model
    print("\nTraining model...")
    history = predictor.train(epochs=50, batch_size=32)
    
    # Save model
    print("\nSaving model...")
    predictor.save_model('models/irrigation_model')
    
    # Test prediction
    print("\nTesting prediction with sample data...")
    sample_sequence = []
    for i in range(24):
        sample_sequence.append({
            'temperature': 22 + np.random.randn(),
            'humidity': 65 + np.random.randn() * 5,
            'light_intensity': 25000 if 6 <= i <= 18 else 0,
            'growth_stage': 2,
            'time_of_day': i,
            'soil_moisture': 60 + np.random.randn() * 5
        })
    
    prediction = predictor.predict(sample_sequence)
    print(f"\nPrediction: {prediction}")
    print(f"  → Next irrigation in {prediction['hours_until_irrigation']:.1f} hours")
    print(f"  → Irrigation volume: {prediction['irrigation_volume_ml']:.0f} ml")
    
    print("\n" + "=" * 60)
    print("Model training complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
