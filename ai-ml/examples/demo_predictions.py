"""
Example usage of Agronomia AI/ML models
"""

import sys
sys.path.append('..')

from training.train_irrigation_model import IrrigationPredictor
from training.train_nutrient_model import NutrientOptimizer
from training.train_harvest_model import HarvestPredictor
import numpy as np

def demo_irrigation_prediction():
    """Demonstrate irrigation prediction"""
    print("\n" + "="*60)
    print("Irrigation Prediction Demo")
    print("="*60)
    
    predictor = IrrigationPredictor()
    
    # Generate sample sequence (24 hours of data)
    sample_sequence = []
    for hour in range(24):
        is_day = 6 <= hour <= 20
        sample_sequence.append({
            'temperature': 24 if is_day else 20,
            'humidity': 65 + np.random.randn() * 3,
            'light_intensity': 25000 if is_day else 0,
            'growth_stage': 2,  # Vegetative
            'time_of_day': hour,
            'soil_moisture': 60 + np.random.randn() * 5
        })
    
    print("\nConditions:")
    print(f"  Current temperature: {sample_sequence[-1]['temperature']}°C")
    print(f"  Current humidity: {sample_sequence[-1]['humidity']:.1f}%")
    print(f"  Soil moisture: {sample_sequence[-1]['soil_moisture']:.1f}%")
    
    # Note: Requires trained model
    print("\n⚠️  To run prediction, first train the model:")
    print("    cd ai-ml/training")
    print("    python train_irrigation_model.py")

def demo_nutrient_optimization():
    """Demonstrate nutrient optimization"""
    print("\n" + "="*60)
    print("Nutrient Optimization Demo")
    print("="*60)
    
    optimizer = NutrientOptimizer()
    
    # Sample conditions
    conditions = {
        'current_ec': 1800,
        'current_ph': 6.5,
        'plant_type': 'tomato',
        'growth_stage': 'fruiting',
        'water_temp': 23,
        'days_since_transplant': 45,
        'target_ec': 2500
    }
    
    print("\nCurrent Conditions:")
    print(f"  Plant: {conditions['plant_type']} ({conditions['growth_stage']})")
    print(f"  EC: {conditions['current_ec']} μS/cm (target: {conditions['target_ec']})")
    print(f"  pH: {conditions['current_ph']}")
    print(f"  Water temp: {conditions['water_temp']}°C")
    
    print("\n⚠️  To run prediction, first train the model:")
    print("    cd ai-ml/training")
    print("    python train_nutrient_model.py")

def demo_harvest_prediction():
    """Demonstrate harvest prediction"""
    print("\n" + "="*60)
    print("Harvest Prediction Demo")
    print("="*60)
    
    predictor = HarvestPredictor()
    
    # Sample plant data
    plant_data = {
        'plant_type': 'tomato',
        'days_since_transplant': 50,
        'avg_temperature': 24,
        'avg_light_hours': 15,
        'avg_humidity': 68,
        'avg_ec': 2200,
        'growth_rate': 0.6,
        'plant_height': 80,
        'leaf_count': 18
    }
    
    print("\nPlant Data:")
    print(f"  Type: {plant_data['plant_type']}")
    print(f"  Age: {plant_data['days_since_transplant']} days")
    print(f"  Height: {plant_data['plant_height']} cm")
    print(f"  Leaf count: {plant_data['leaf_count']}")
    print(f"  Growth rate: {plant_data['growth_rate']} cm/day")
    
    print("\n⚠️  To run prediction, first train the model:")
    print("    cd ai-ml/training")
    print("    python train_harvest_model.py")

def main():
    """Run all demos"""
    print("="*60)
    print("Agronomia AI/ML Models - Demo Examples")
    print("="*60)
    print("\nThis script demonstrates how to use the AI/ML models.")
    print("First, you need to train the models by running the training scripts.")
    
    demo_irrigation_prediction()
    demo_nutrient_optimization()
    demo_harvest_prediction()
    
    print("\n" + "="*60)
    print("Training Instructions")
    print("="*60)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Train models (takes 2-5 minutes):")
    print("   python train_irrigation_model.py")
    print("   python train_nutrient_model.py")
    print("   python train_harvest_model.py")
    print("\n3. Run this demo again to see predictions!")
    print("="*60)

if __name__ == "__main__":
    main()
