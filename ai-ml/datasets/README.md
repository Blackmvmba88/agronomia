# Sample Dataset for Agronomia

This directory contains sample datasets for training and testing the AI/ML models.

## Datasets

### 1. sensor_data.csv
Time-series sensor readings from hydroponic systems.

**Columns:**
- timestamp
- device_id
- ph
- water_temp (°C)
- air_temp (°C)
- humidity (%)
- ec (μS/cm)
- tds (ppm)
- lux
- plant_type
- growth_stage

### 2. growth_records.csv
Manual plant growth measurements.

**Columns:**
- date
- device_id
- plant_type
- days_since_transplant
- plant_height (cm)
- leaf_count
- stem_diameter (mm)
- notes

### 3. harvest_records.csv
Harvest data for yield analysis.

**Columns:**
- harvest_date
- device_id
- plant_type
- days_to_harvest
- yield_g
- quality_rating (1-5)
- brix_level (for tomatoes)
- notes

### 4. irrigation_logs.csv
Irrigation events and conditions.

**Columns:**
- timestamp
- device_id
- irrigation_volume_ml
- pre_moisture (%)
- post_moisture (%)
- temperature
- humidity
- light_level

### 5. nutrient_adjustments.csv
Nutrient solution adjustments.

**Columns:**
- timestamp
- device_id
- action (increase_ec, decrease_ec, adjust_ph_up, adjust_ph_down, maintain)
- amount_ml_per_10L
- before_ec
- after_ec
- before_ph
- after_ph
- plant_type
- growth_stage

## Data Collection

### Automated Collection
Sensor data is automatically collected via:
- ESP32 firmware → MQTT → Backend API → Database
- 5-second sensor readings
- 10-second publish intervals

### Manual Collection
Growth and harvest data should be recorded:
- **Daily:** Plant height, leaf count
- **Weekly:** Stem diameter, visual health assessment
- **At harvest:** Yield, quality, notes

## Data Format

All CSV files use:
- UTF-8 encoding
- Comma separator
- ISO 8601 datetime format
- Metric units

## Synthetic Data

For development and testing, synthetic data can be generated:

```python
from train_irrigation_model import IrrigationPredictor

predictor = IrrigationPredictor()
synthetic_data = predictor.generate_synthetic_data(n_samples=10000)
synthetic_data.to_csv('datasets/synthetic_sensor_data.csv', index=False)
```

## Data Privacy

- Remove personally identifiable information
- Anonymize location data if sharing
- Follow GDPR/privacy regulations

## Data Quality

Ensure data quality:
- Remove sensor errors (e.g., -127°C readings)
- Handle missing values
- Validate ranges (pH 0-14, EC 0-5000, etc.)
- Timestamp consistency

## Usage in Training

```python
import pandas as pd

# Load dataset
data = pd.read_csv('datasets/sensor_data.csv')

# Preprocess
data['timestamp'] = pd.to_datetime(data['timestamp'])
data = data.sort_values('timestamp')
data = data.dropna()

# Use in training
predictor.train(data=data)
```

## Contributing Data

To contribute datasets:
1. Ensure data is anonymized
2. Follow format guidelines
3. Include metadata (plant types, location climate, etc.)
4. Submit via pull request

## Sample Data Generation

Generate sample data for testing:

```bash
cd ai-ml/datasets
python generate_sample_data.py --samples 1000 --output sensor_data_sample.csv
```

## Data Visualization

Explore datasets with Jupyter notebooks:
```bash
jupyter notebook data_exploration.ipynb
```

## Citation

If using this data for research:
```
@dataset{agronomia2024,
  title={Agronomia Hydroponic Monitoring Dataset},
  author={Agronomia Project},
  year={2024},
  url={https://github.com/Blackmvmba88/agronomia}
}
```

## Support

For dataset questions:
- GitHub Issues
- Documentation: docs/data-guide.md
