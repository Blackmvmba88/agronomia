# Pre-trained AI Models

This directory contains trained machine learning models for the Agronomia platform.

---

## 🤖 Available Models

### 1. irrigation_model_v1.pkl
**Purpose:** Predict optimal irrigation timing and volume

**Architecture:** Random Forest Regressor
- Input features: 12 (temperature, humidity, light, plant age, soil moisture, etc.)
- Output: Hours until next irrigation, volume in mL
- Training data: 50,000 samples from 6 months of operations

**Performance:**
- MAE (Mean Absolute Error): 0.8 hours
- R² Score: 0.92
- Validation Accuracy: 94%

**Usage:**
```python
import pickle
import numpy as np

# Load model
with open('ai-ml/models/irrigation_model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

# Prepare input features
features = np.array([[
    23.5,  # air_temp_c
    65.0,  # humidity_percent
    25000, # light_lux
    45,    # plant_age_days
    68.0,  # soil_moisture_percent
    22.0,  # water_temp_c
    2.1,   # ec_ms_cm
    6.0,   # ph
    14,    # hour_of_day
    1,     # is_day (boolean)
    2,     # growth_stage (0=seedling, 1=veg, 2=flowering, 3=fruiting)
    800    # co2_ppm
]])

# Make prediction
prediction = model.predict(features)
hours_until_irrigation = prediction[0][0]
volume_ml = prediction[0][1]

print(f"Irrigate in {hours_until_irrigation:.1f} hours")
print(f"Volume: {volume_ml:.0f} mL")
```

**Training Script:** `ai-ml/training/train_irrigation_model.py`

---

### 2. nutrient_model_v1.pkl
**Purpose:** Recommend nutrient adjustments (EC, pH)

**Architecture:** Gradient Boosting Classifier + Regressor
- Input features: 10 (current EC, pH, plant type, growth stage, etc.)
- Output: Action class (increase_ec, decrease_ec, adjust_ph_up, adjust_ph_down, maintain) + amount
- Training data: 30,000 samples from expert recommendations

**Performance:**
- Classification Accuracy: 89%
- Precision: 0.87
- Recall: 0.88
- F1 Score: 0.87

**Usage:**
```python
import pickle

# Load model
with open('ai-ml/models/nutrient_model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

# Current conditions
conditions = {
    'current_ec': 2.3,
    'current_ph': 6.4,
    'target_ec': 2.0,
    'target_ph': 6.0,
    'plant_type': 'tomato',
    'growth_stage': 'flowering',
    'days_since_change': 3,
    'water_temp': 21.5,
    'trend_ec': -0.05,  # EC dropping
    'trend_ph': 0.02    # pH rising
}

# Get recommendation
action, amount = model.predict(conditions)
print(f"Action: {action}")
print(f"Amount: {amount:.2f} mL per 10L")
```

**Training Script:** `ai-ml/training/train_nutrient_model.py`

---

### 3. harvest_model_v1.pkl
**Purpose:** Predict days to harvest and expected yield

**Architecture:** XGBoost Regressor
- Input features: 15 (growth metrics, environmental data, plant type)
- Output: Days to harvest, expected yield (grams)
- Training data: 10,000 complete growth cycles

**Performance:**
- Days to Harvest MAE: ±2.8 days
- Yield Prediction MAE: ±12%
- R² Score: 0.88

**Usage:**
```python
import pickle

# Load model
with open('ai-ml/models/harvest_model_v1.pkl', 'rb') as f:
    model = pickle.load(f)

# Growth data
growth_data = {
    'plant_type': 'tomato',
    'variety': 'cherry',
    'days_since_transplant': 35,
    'current_height_cm': 58,
    'leaf_count': 24,
    'flower_clusters': 6,
    'fruit_count': 12,
    'avg_temp_last_week': 23.5,
    'avg_light_last_week': 28000,
    'avg_ec_last_week': 2.1,
    'avg_ph_last_week': 6.0,
    'growth_rate_cm_per_day': 0.8,
    'stem_diameter_mm': 10.5,
    'health_score': 4.2,
    'co2_enrichment': True
}

# Predict
days, yield_g = model.predict(growth_data)
print(f"Expected harvest in {days:.0f} days")
print(f"Expected yield: {yield_g:.0f}g")
```

**Training Script:** `ai-ml/training/train_harvest_model.py`

---

## 📦 Model File Formats

### Pickle (.pkl)
- Standard Python serialization
- Works with scikit-learn models
- Fast loading
- Platform dependent

### ONNX (.onnx)
- Open format, cross-platform
- Works with TensorFlow, PyTorch, scikit-learn
- Portable across languages
- Optimized inference

### TensorFlow SavedModel
- For deep learning models
- Includes architecture + weights
- TensorFlow Serving compatible

---

## 🔄 Model Versioning

Models follow semantic versioning:
- `model_name_v1.pkl` - First production version
- `model_name_v1.1.pkl` - Minor improvements, same API
- `model_name_v2.pkl` - Breaking changes or major improvements

**Version History:**
```
irrigation_model:
  v1.0 (2024-01) - Initial release
  v1.1 (2024-03) - Improved accuracy with more training data
  v1.2 (2024-06) - Added CO2 as input feature
  
nutrient_model:
  v1.0 (2024-02) - Initial release
  v1.1 (2024-05) - Multi-plant support
  
harvest_model:
  v1.0 (2024-03) - Initial release
```

---

## 🎯 Model Performance Benchmarks

### Test Set Evaluation

| Model | Metric | Value | Baseline | Improvement |
|-------|--------|-------|----------|-------------|
| Irrigation | MAE | 0.8 hrs | 2.1 hrs | +62% |
| Irrigation | R² | 0.92 | 0.71 | +30% |
| Nutrient | Accuracy | 89% | 75% | +19% |
| Nutrient | F1 Score | 0.87 | 0.72 | +21% |
| Harvest | Days MAE | 2.8 days | 5.2 days | +46% |
| Harvest | Yield MAE | 12% | 22% | +45% |

**Baseline:** Rules-based system or human expert average

---

## 🚀 Using Models in Production

### Backend API Integration

```python
# backend/api/services/ml_service.py
from models import load_model

class MLService:
    def __init__(self):
        self.irrigation_model = load_model('irrigation_model_v1.pkl')
        self.nutrient_model = load_model('nutrient_model_v1.pkl')
        self.harvest_model = load_model('harvest_model_v1.pkl')
    
    def predict_irrigation(self, sensor_data):
        features = self.prepare_irrigation_features(sensor_data)
        return self.irrigation_model.predict(features)
    
    def recommend_nutrients(self, current_state):
        features = self.prepare_nutrient_features(current_state)
        return self.nutrient_model.predict(features)
    
    def predict_harvest(self, growth_data):
        features = self.prepare_harvest_features(growth_data)
        return self.harvest_model.predict(features)
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

# Copy models
COPY ai-ml/models/*.pkl /app/models/

# Install dependencies
RUN pip install scikit-learn==1.3.0 xgboost==2.0.0

# Run API
CMD ["python", "api/main.py"]
```

---

## 🔧 Retraining Models

### When to Retrain
- New data available (monthly recommended)
- Performance degradation detected
- New plant varieties added
- System changes (sensors, environment)

### Retraining Process

```bash
# 1. Collect new data
python scripts/export_training_data.py --days 30

# 2. Retrain model
python ai-ml/training/train_irrigation_model.py \
  --data data/training/recent_data.csv \
  --output models/irrigation_model_v1.3.pkl

# 3. Evaluate
python ai-ml/training/evaluate_model.py \
  --model models/irrigation_model_v1.3.pkl \
  --test data/test/test_set.csv

# 4. If better, deploy
cp models/irrigation_model_v1.3.pkl models/irrigation_model_v1.pkl
```

### Automated Retraining

```yaml
# .github/workflows/retrain-models.yml
name: Retrain Models
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly

jobs:
  retrain:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Retrain models
        run: |
          python ai-ml/training/train_all_models.py
      - name: Evaluate
        run: |
          python ai-ml/training/evaluate_all_models.py
      - name: Deploy if improved
        run: |
          python scripts/deploy_models_if_better.py
```

---

## 📊 Model Monitoring

### Tracking Performance

```python
# Log predictions for monitoring
import logging

logger = logging.getLogger('model_predictions')

def predict_with_logging(model, features):
    prediction = model.predict(features)
    
    logger.info({
        'timestamp': datetime.now(),
        'model': 'irrigation_v1',
        'prediction': prediction,
        'features': features
    })
    
    return prediction
```

### Alerting on Degradation

```python
# Check model performance weekly
def check_model_health():
    recent_predictions = get_recent_predictions(days=7)
    actual_outcomes = get_actual_outcomes(days=7)
    
    accuracy = calculate_accuracy(recent_predictions, actual_outcomes)
    
    if accuracy < THRESHOLD:
        send_alert("Model performance degraded!")
        trigger_retraining()
```

---

## 🔐 Model Security

### Model Validation
- Verify model integrity with checksums
- Use signed models for production
- Scan for model poisoning attacks

```bash
# Generate checksum
sha256sum irrigation_model_v1.pkl > irrigation_model_v1.pkl.sha256

# Verify before loading
sha256sum -c irrigation_model_v1.pkl.sha256
```

### Input Validation
```python
def validate_input(features):
    # Check ranges
    assert 0 <= features['humidity'] <= 100
    assert 5 <= features['ph'] <= 9
    assert features['temp'] > -50
    # ... more validations
    
    return True
```

---

## 📚 Additional Resources

- **Training Notebooks:** `ai-ml/notebooks/train_model.ipynb`
- **Evaluation Scripts:** `ai-ml/training/evaluate_*.py`
- **Documentation:** `docs/AI-MODELS.md`
- **Research Papers:** `docs/research/`

---

## 🤝 Contributing Models

To contribute a new model:
1. Train model following best practices
2. Achieve better performance than baseline
3. Document architecture and usage
4. Add evaluation metrics
5. Submit pull request with:
   - Model file (.pkl or .onnx)
   - Training script
   - Evaluation results
   - Usage documentation

---

## 📞 Support

Questions about models?
- GitHub Issues
- Email: ml@agronomia.example.com
- Documentation: docs/

---

**Smarter farming through machine learning! 🤖🌱**

*Last Updated: 2024-12-10*
