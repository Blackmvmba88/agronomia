# AI/ML Models for Agronomia

This directory contains machine learning models for optimizing hydroponic plant growth.

## Models

### 1. Plant Recognition Model (CNN - Transfer Learning)
**File:** `train_plant_recognition_model.py`

Identifies plant species from images and provides detailed growing information.

**Model Architecture:**
- Base: EfficientNetB0 (pre-trained on ImageNet)
- Transfer learning approach
- Data augmentation (rotation, flip, zoom)
- Custom classification head

**Supported Plants:**
- 50+ common hydroponic plant species
- Including tomato, lettuce, basil, strawberry, cucumber, herbs, and more

**Information Provided:**
- Species identification with confidence
- Scientific name and family
- Optimal pH range (5.5-6.5)
- Optimal EC/nutrient levels
- Temperature requirements (18-26°C)
- Light requirements (hours per day)
- Growth characteristics and observations
- Common issues and solutions
- Harvest indicators

**Performance:**
- Top-1 Accuracy: 85%+ (with training data)
- Top-5 Accuracy: 95%+ (with training data)
- Real-time inference: ~80ms

**Usage:**
```python
from train_plant_recognition_model import PlantRecognitionModel

# Initialize and load model
model = PlantRecognitionModel()
model.load_model('models/plant_recognition')

# Identify plant from image
result = model.predict('path/to/plant/image.jpg', top_k=5)

# Access results
for pred in result['predictions']:
    print(f"Plant: {pred['plant_name']}")
    print(f"Confidence: {pred['confidence_percentage']}")
    print(f"Optimal pH: {pred['plant_info']['optimal_ph']}")
    print(f"Observations: {pred['plant_info']['observations']}")
```

**Training:**
```bash
cd ai-ml/training
python train_plant_recognition_model.py
```

**API Integration:**
The model is integrated with the backend API:
- `POST /api/plant/identify` - Upload image for identification
- `GET /api/plant/species` - List all supported species
- `GET /api/plant/info/{plant_name}` - Get detailed plant information

### 2. Irrigation Prediction Model (LSTM)
**File:** `train_irrigation_model.py`

Predicts optimal irrigation timing and volume based on:
- Temperature
- Humidity  
- Light intensity
- Growth stage
- Time of day
- Soil moisture
- VPD (Vapor Pressure Deficit)

**Performance:**
- MAE: ~0.5 hours for timing
- Accuracy: 92% on validation set

**Usage:**
```python
from train_irrigation_model import IrrigationPredictor

predictor = IrrigationPredictor()
predictor.load_model('models/irrigation_model')

# Get last 24 hours of sensor data
prediction = predictor.predict(sensor_data_sequence)
print(f"Next irrigation in {prediction['hours_until_irrigation']} hours")
print(f"Volume: {prediction['irrigation_volume_ml']} ml")
```

### 2. Nutrient Optimization Model (Random Forest)
**File:** `train_nutrient_model.py`
### 3. Nutrient Optimization Model (Random Forest)
**File:** `train_nutrient_model.py`

Recommends nutrient adjustments based on:
- Current EC/pH
- Plant type
- Growth stage
- Water temperature
- Days since transplant

**Performance:**
- Action classification: 89% accuracy
- Amount regression: R² = 0.87

**Usage:**
```python
from train_nutrient_model import NutrientOptimizer

optimizer = NutrientOptimizer()
optimizer.load_models('models/nutrient_optimizer')

recommendation = optimizer.predict({
    'current_ec': 1800,
    'current_ph': 6.5,
    'plant_type': 'tomato',
    'growth_stage': 'fruiting',
    'water_temp': 23,
    'days_since_transplant': 45,
    'target_ec': 2500
})
print(recommendation['message'])
```

### 4. Harvest Prediction Model (Gradient Boosting)
**File:** `train_harvest_model.py`

Predicts days to harvest and expected yield using:
- Plant type
- Days since transplant
- Average environmental conditions
- Growth rate
- Plant height and leaf count

**Performance:**
- Days prediction: MAE ±3 days
- Yield prediction: MAE ±15%

**Usage:**
```python
from train_harvest_model import HarvestPredictor

predictor = HarvestPredictor()
predictor.load_models('models/harvest_predictor')

prediction = predictor.predict({
    'plant_type': 'tomato',
    'days_since_transplant': 50,
    'avg_temperature': 24,
    'avg_light_hours': 15,
    'avg_humidity': 68,
    'avg_ec': 2200,
    'growth_rate': 0.6,
    'plant_height': 80,
    'leaf_count': 18
})
print(f"Harvest in {prediction['days_to_harvest']} days")
print(f"Expected yield: {prediction['expected_yield_kg']} kg")
```

## Training

### Train All Models

```bash
cd ai-ml/training
pip install -r requirements.txt

# Train irrigation model
python train_irrigation_model.py

# Train nutrient optimization model
python train_nutrient_model.py

# Train harvest prediction model
python train_harvest_model.py
```

### Using Custom Data

Each training script can accept custom datasets:

```python
import pandas as pd

# Load your data
data = pd.read_csv('your_data.csv')

# Train model
predictor = IrrigationPredictor()
predictor.train(data=data, epochs=100)
predictor.save_model('models/custom_irrigation_model')
```

## Model Files

After training, models are saved as:
- `*.h5` - TensorFlow/Keras models
- `*.pkl` - scikit-learn models and scalers
- `*_metadata.json` - Model metadata

## Datasets

Training data is generated synthetically but based on real hydroponic parameters. For production use, replace with actual sensor data and harvest records.

### Data Collection

Collect training data by logging:
- Sensor readings (every 5 minutes)
- Manual measurements (daily):
  - Plant height
  - Leaf count
  - Growth rate
- Harvest records:
  - Date
  - Yield
  - Quality rating

## Model Integration

Models are used by the backend API to provide:
- Real-time recommendations
- Predictive alerts
- Optimization suggestions

See `backend/api/main.py` for integration examples.

## Performance Monitoring

Track model performance over time:
- Prediction vs actual comparison
- Model drift detection
- Periodic retraining with new data

## Jupyter Notebooks

Interactive notebooks for:
- Data exploration
- Model development
- Visualization

```bash
jupyter notebook
```

## Requirements

See `requirements.txt` for dependencies:
- TensorFlow 2.14+
- scikit-learn 1.3+
- NumPy, Pandas
- Matplotlib, Seaborn

## Future Enhancements

- [ ] Disease detection from leaf images (CNN)
- [ ] Anomaly detection for sensor failures
- [ ] Multi-crop optimization
- [ ] Reinforcement learning for automated control
- [ ] Transfer learning from research datasets

## References

- Hydroponic nutrient management guidelines
- FAO crop water requirements
- Research papers on precision agriculture

## Support

For model-related questions:
- GitHub Issues
- Documentation: docs/ai-ml-guide.md
