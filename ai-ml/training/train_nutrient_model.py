"""
Nutrient Optimization Model
Uses Random Forest to recommend nutrient adjustments for optimal plant growth
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib
import json
from datetime import datetime

class NutrientOptimizer:
    """
    Recommends nutrient adjustments based on current conditions and plant requirements
    """
    
    def __init__(self):
        self.action_model = None  # Classifier for action type
        self.amount_model = None  # Regressor for adjustment amount
        self.scaler = StandardScaler()
        self.plant_encoder = LabelEncoder()
        self.stage_encoder = LabelEncoder()
        
        self.feature_names = [
            'current_ec',
            'current_ph',
            'plant_type',
            'growth_stage',
            'water_temp',
            'days_since_transplant',
            'target_ec'
        ]
        
        # Nutrient action types
        self.actions = [
            'maintain',      # No change needed
            'increase_ec',   # Add more nutrients
            'decrease_ec',   # Dilute solution
            'adjust_ph_up',  # Increase pH
            'adjust_ph_down' # Decrease pH
        ]
    
    def generate_synthetic_data(self, n_samples=5000):
        """Generate synthetic training data for nutrient optimization"""
        np.random.seed(42)
        
        plant_types = ['lettuce', 'tomato', 'cucumber', 'pepper', 'herbs']
        growth_stages = ['seedling', 'vegetative', 'flowering', 'fruiting']
        
        # Target EC ranges by plant and stage
        ec_targets = {
            'lettuce': {'seedling': 800, 'vegetative': 1200, 'flowering': 1400, 'fruiting': 1400},
            'tomato': {'seedling': 1000, 'vegetative': 1800, 'flowering': 2500, 'fruiting': 3000},
            'cucumber': {'seedling': 900, 'vegetative': 1600, 'flowering': 2200, 'fruiting': 2400},
            'pepper': {'seedling': 1000, 'vegetative': 1800, 'flowering': 2200, 'fruiting': 2500},
            'herbs': {'seedling': 600, 'vegetative': 1000, 'flowering': 1200, 'fruiting': 1200},
        }
        
        data = []
        for _ in range(n_samples):
            plant = np.random.choice(plant_types)
            stage = np.random.choice(growth_stages)
            target_ec = ec_targets[plant][stage]
            
            # Current EC with some variance
            current_ec = target_ec + np.random.normal(0, 300)
            
            record = {
                'current_ec': max(0, current_ec),
                'current_ph': np.random.normal(6.0, 0.5),
                'plant_type': plant,
                'growth_stage': stage,
                'water_temp': np.random.normal(22, 2),
                'days_since_transplant': np.random.randint(1, 90),
                'target_ec': target_ec
            }
            
            # Determine action based on current vs target
            ec_diff = current_ec - target_ec
            ph_diff = record['current_ph'] - 6.0
            
            # Action priority: pH first, then EC
            if abs(ph_diff) > 0.5:
                if ph_diff > 0:
                    action = 'adjust_ph_down'
                    amount = abs(ph_diff) * 10  # ml of pH down per 10L
                else:
                    action = 'adjust_ph_up'
                    amount = abs(ph_diff) * 10
            elif abs(ec_diff) > 200:
                if ec_diff > 0:
                    action = 'decrease_ec'
                    amount = abs(ec_diff) / 10  # ml of water per 10L
                else:
                    action = 'increase_ec'
                    amount = abs(ec_diff) / 50  # ml of nutrient per 10L
            else:
                action = 'maintain'
                amount = 0
            
            record['action'] = action
            record['amount'] = amount
            
            data.append(record)
        
        return pd.DataFrame(data)
    
    def train(self, data=None, test_size=0.2):
        """Train both action classifier and amount regressor"""
        if data is None:
            print("Generating synthetic training data...")
            data = self.generate_synthetic_data()
        
        print(f"Training with {len(data)} samples")
        
        # Encode categorical variables
        plant_types = data['plant_type'].unique()
        growth_stages = data['growth_stage'].unique()
        self.plant_encoder.fit(plant_types)
        self.stage_encoder.fit(growth_stages)
        
        # Prepare features
        X = data.copy()
        X['plant_type'] = self.plant_encoder.transform(X['plant_type'])
        X['growth_stage'] = self.stage_encoder.transform(X['growth_stage'])
        X = X[self.feature_names].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Prepare targets
        y_action = data['action'].values
        y_amount = data['amount'].values
        
        # Split data
        X_train, X_test, y_action_train, y_action_test, y_amount_train, y_amount_test = train_test_split(
            X_scaled, y_action, y_amount, test_size=test_size, random_state=42
        )
        
        # Train action classifier
        print("\nTraining action classifier...")
        self.action_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.action_model.fit(X_train, y_action_train)
        
        # Evaluate action classifier
        action_pred = self.action_model.predict(X_test)
        print("\nAction Classifier Performance:")
        print(classification_report(y_action_test, action_pred))
        
        # Cross-validation score
        cv_scores = cross_val_score(self.action_model, X_scaled, y_action, cv=5)
        print(f"Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        
        # Train amount regressor
        print("\nTraining amount regressor...")
        self.amount_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.amount_model.fit(X_train, y_amount_train)
        
        # Evaluate amount regressor
        amount_pred = self.amount_model.predict(X_test)
        mse = mean_squared_error(y_amount_test, amount_pred)
        r2 = r2_score(y_amount_test, amount_pred)
        print("\nAmount Regressor Performance:")
        print(f"MSE: {mse:.2f}")
        print(f"R² Score: {r2:.3f}")
        
        # Feature importance
        print("\nTop 5 Important Features:")
        feature_importance = self.action_model.feature_importances_
        for idx in np.argsort(feature_importance)[-5:][::-1]:
            print(f"  {self.feature_names[idx]}: {feature_importance[idx]:.3f}")
        
        return {
            'action_accuracy': cv_scores.mean(),
            'amount_r2': r2
        }
    
    def predict(self, sensor_data):
        """
        Predict nutrient adjustment recommendation
        
        Args:
            sensor_data: dict with current sensor readings and plant info
        
        Returns:
            dict with recommended action and amount
        """
        if self.action_model is None or self.amount_model is None:
            raise ValueError("Models not trained. Call train() first.")
        
        # Prepare features
        features = [
            sensor_data.get('current_ec', 1500),
            sensor_data.get('current_ph', 6.0),
            self.plant_encoder.transform([sensor_data.get('plant_type', 'lettuce')])[0],
            self.stage_encoder.transform([sensor_data.get('growth_stage', 'vegetative')])[0],
            sensor_data.get('water_temp', 22),
            sensor_data.get('days_since_transplant', 30),
            sensor_data.get('target_ec', 1500)
        ]
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict action
        action = self.action_model.predict(features_scaled)[0]
        action_proba = self.action_model.predict_proba(features_scaled)[0]
        confidence = max(action_proba)
        
        # Predict amount
        amount = self.amount_model.predict(features_scaled)[0]
        
        # Generate recommendation message
        messages = {
            'maintain': "Nutrient levels are optimal. No adjustment needed.",
            'increase_ec': f"Add {amount:.1f} ml of nutrient solution per 10L to increase EC.",
            'decrease_ec': f"Add {amount:.1f} ml of fresh water per 10L to decrease EC.",
            'adjust_ph_up': f"Add {amount:.1f} ml of pH Up solution per 10L to raise pH.",
            'adjust_ph_down': f"Add {amount:.1f} ml of pH Down solution per 10L to lower pH."
        }
        
        return {
            'action': action,
            'amount_ml_per_10L': float(amount),
            'confidence': float(confidence),
            'message': messages[action],
            'timestamp': datetime.now().isoformat()
        }
    
    def save_models(self, path='nutrient_optimizer'):
        """Save models and preprocessing objects"""
        joblib.dump(self.action_model, f'{path}_action_model.pkl')
        joblib.dump(self.amount_model, f'{path}_amount_model.pkl')
        joblib.dump(self.scaler, f'{path}_scaler.pkl')
        joblib.dump(self.plant_encoder, f'{path}_plant_encoder.pkl')
        joblib.dump(self.stage_encoder, f'{path}_stage_encoder.pkl')
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'actions': self.actions,
            'plant_types': self.plant_encoder.classes_.tolist(),
            'growth_stages': self.stage_encoder.classes_.tolist(),
            'created': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        with open(f'{path}_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Models saved to {path}")
    
    def load_models(self, path='nutrient_optimizer'):
        """Load models and preprocessing objects"""
        self.action_model = joblib.load(f'{path}_action_model.pkl')
        self.amount_model = joblib.load(f'{path}_amount_model.pkl')
        self.scaler = joblib.load(f'{path}_scaler.pkl')
        self.plant_encoder = joblib.load(f'{path}_plant_encoder.pkl')
        self.stage_encoder = joblib.load(f'{path}_stage_encoder.pkl')
        
        # Load metadata
        with open(f'{path}_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        self.feature_names = metadata['feature_names']
        self.actions = metadata['actions']
        
        print(f"Models loaded from {path}")

def main():
    """Train and save the nutrient optimization models"""
    print("=" * 60)
    print("Agronomia Nutrient Optimization Model Training")
    print("=" * 60)
    
    optimizer = NutrientOptimizer()
    
    # Train models
    print("\nTraining models...")
    results = optimizer.train()
    
    # Save models
    print("\nSaving models...")
    optimizer.save_models('models/nutrient_optimizer')
    
    # Test prediction
    print("\nTesting prediction with sample data...")
    sample_data = {
        'current_ec': 1800,
        'current_ph': 6.5,
        'plant_type': 'tomato',
        'growth_stage': 'fruiting',
        'water_temp': 23,
        'days_since_transplant': 45,
        'target_ec': 2500
    }
    
    prediction = optimizer.predict(sample_data)
    print(f"\nPrediction for tomato in fruiting stage:")
    print(f"  Current EC: {sample_data['current_ec']} μS/cm")
    print(f"  Target EC: {sample_data['target_ec']} μS/cm")
    print(f"  → Action: {prediction['action']}")
    print(f"  → Amount: {prediction['amount_ml_per_10L']:.1f} ml per 10L")
    print(f"  → Confidence: {prediction['confidence']:.1%}")
    print(f"  → {prediction['message']}")
    
    print("\n" + "=" * 60)
    print("Model training complete!")
    print(f"Action classifier accuracy: {results['action_accuracy']:.1%}")
    print(f"Amount regressor R² score: {results['amount_r2']:.3f}")
    print("=" * 60)

if __name__ == "__main__":
    main()
