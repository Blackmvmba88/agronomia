# Demo Data for Agronomia

This directory contains pre-loaded sample datasets that demonstrate the Agronomia platform without requiring any physical hardware.

## 📊 Available Datasets

### 1. greenhouse_1_month.csv
**Description:** One month of continuous sensor data from a hydroponic greenhouse

**Records:** 8,640 (5-minute intervals for 30 days)

**Columns:**
- `timestamp` - Date and time of measurement
- `device_id` - Greenhouse device identifier
- `location` - Physical location in greenhouse
- `air_temp_c` - Air temperature (°C)
- `water_temp_c` - Water temperature (°C)
- `humidity_percent` - Relative humidity (%)
- `ph` - pH level of nutrient solution
- `ec_us_cm` - Electrical conductivity (μS/cm)
- `tds_ppm` - Total dissolved solids (ppm)
- `light_lux` - Light intensity (lux)
- `par_umol` - Photosynthetically active radiation (μmol/m²/s)
- `co2_ppm` - CO2 concentration (ppm)
- `water_level_cm` - Water level in reservoir (cm)
- `flow_rate_lpm` - Water flow rate (liters per minute)

**Use Cases:**
- Dashboard visualization without sensors
- Time-series analysis training
- Alert threshold testing
- Data pipeline validation

---

### 2. strawberry_batch_04.json
**Description:** Complete growth tracking data for a strawberry batch (variety: Albion)

**Duration:** 60 days from transplant to harvest

**Contents:**
- Batch metadata (variety, start date, system type)
- Weekly growth measurements (height, leaves, crown diameter)
- Flowering and fruiting progression
- Environmental conditions summary
- Nutrient schedule and adjustments
- Harvest data (6 harvests with quality metrics)
- Total yield and performance metrics
- Observations and recommendations

**Use Cases:**
- Growth prediction model training
- Harvest forecasting
- Nutrient optimization
- Batch comparison and analysis
- Report generation

---

### 3. ph_vs_ec_experiment.csv
**Description:** Controlled experiment comparing pH and EC effects on plant growth

**Design:** 3 pH levels × 3 EC levels × 4 replicates × 7 weeks = 252 records

**Treatments:**
- pH levels: 5.5, 6.0, 6.5
- EC levels: 1600, 2000, 2400 μS/cm
- Replicates: 4 per treatment
- Duration: 6 weeks + initial measurement

**Measurements:**
- Plant height (cm)
- Leaf count
- Stem diameter (mm)
- Chlorophyll content (SPAD)
- Cumulative yield (g)
- Root health score (1-5)

**Use Cases:**
- Statistical analysis (ANOVA)
- Optimization of growing conditions
- pH and EC recommendation models
- Treatment comparison visualizations
- Scientific report generation

---

## 🚀 Quick Start

### Load Data in Python
```python
import pandas as pd
import json

# Load greenhouse sensor data
greenhouse_data = pd.read_csv('data/greenhouse_1_month.csv')
greenhouse_data['timestamp'] = pd.to_datetime(greenhouse_data['timestamp'])

# Load strawberry batch data
with open('data/strawberry_batch_04.json', 'r') as f:
    strawberry_data = json.load(f)

# Load experiment data
experiment_data = pd.read_csv('data/ph_vs_ec_experiment.csv')
```

### Visualize in Dashboard
```bash
# Start the backend API
cd backend/api
python main.py

# Import demo data
curl -X POST http://localhost:8000/api/data/import \
  -F "file=@../../data/greenhouse_1_month.csv"

# Access dashboard
open http://localhost:3000
```

### Use in Jupyter Notebooks
```python
# Load and explore
import matplotlib.pyplot as plt
import seaborn as sns

# Plot temperature over time
plt.figure(figsize=(15, 5))
plt.plot(greenhouse_data['timestamp'], greenhouse_data['air_temp_c'])
plt.title('Air Temperature - 1 Month')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.show()

# Experiment analysis
sns.boxplot(data=experiment_data, x='ph_target', y='cumulative_yield_g', hue='ec_target_us_cm')
plt.title('Yield by pH and EC Treatment')
plt.show()
```

---

## 📈 Data Statistics

### Greenhouse Data (30 Days)
```
Temperature Range: 16-32°C (air), 18-26°C (water)
Humidity Range: 45-85%
pH Range: 5.2-7.2
EC Range: 1400-2600 μS/cm
Light Cycle: 14 hours (6 AM - 8 PM)
```

### Strawberry Batch
```
Total Yield: 7.2 kg (150g per plant)
Production Days: 60
Quality Rating: 4.5/5
Average Brix: 8.5
```

### pH/EC Experiment
```
Optimal Conditions: pH 6.0, EC 2000 μS/cm
Best Treatment Yield: ~350g per plant
Growth Period: 42 days
```

---

## 🔄 Regenerate Data

To create fresh demo data:

```bash
cd data
python generate_demo_data.py
```

This will regenerate all three datasets with new random variations while maintaining realistic patterns.

---

## 📊 Data Quality

All datasets feature:
- ✓ Realistic value ranges based on hydroponic best practices
- ✓ Natural variation and noise
- ✓ Day/night cycles
- ✓ Growth progression patterns
- ✓ No missing values
- ✓ Proper data types and formats

---

## 🎯 Educational Value

These datasets are perfect for:
- **Students:** Learn data science with real agricultural data
- **Researchers:** Test algorithms before deploying to real systems
- **Developers:** Build and test features without hardware
- **Presentations:** Demonstrate system capabilities
- **Tutorials:** Create reproducible examples

---

## 📝 Citation

If you use this data in research or publications:

```
@dataset{agronomia_demo_2024,
  title={Agronomia Demo Datasets - Hydroponic Monitoring Data},
  author={Agronomia Project Contributors},
  year={2024},
  url={https://github.com/Blackmvmba88/agronomia},
  note={Synthetic data for demonstration and education}
}
```

---

## 🤝 Contributing

To add more demo datasets:
1. Follow the format conventions above
2. Ensure data is realistic and scientifically accurate
3. Include comprehensive documentation
4. Add visualization examples
5. Submit a pull request

---

## 📞 Support

Questions about the demo data?
- Open an issue on GitHub
- Check the main documentation
- Join our community discussions

---

**Built with ❤️ for agricultural innovation and education**
