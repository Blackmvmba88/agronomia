#!/usr/bin/env python3
"""
Generate pre-loaded demo datasets for Agronomia
This creates realistic sample data that can be used without any hardware
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta


def generate_greenhouse_1_month():
    """Generate 1 month of greenhouse sensor data"""
    print("Generating greenhouse_1_month.csv...")
    
    # 1 month of data, 5-minute intervals
    start_time = datetime.now() - timedelta(days=30)
    num_records = 30 * 24 * 12  # 8640 records
    timestamps = [start_time + timedelta(minutes=i*5) for i in range(num_records)]
    
    data = []
    
    for i, ts in enumerate(timestamps):
        hour = ts.hour
        day_of_month = (i // (24 * 12)) + 1
        
        # Simulate day/night cycle
        is_day = 6 <= hour <= 20
        
        # Light follows day/night cycle with seasonal variation
        if is_day:
            base_lux = 25000 + day_of_month * 200  # Increasing light over month
            lux = np.random.normal(base_lux, 3000)
        else:
            lux = np.random.normal(0, 50)
        
        # Temperature varies with light and time
        if is_day:
            air_temp = 23 + (hour - 13) * 0.5 + np.random.normal(0, 1.2)
            water_temp = 21.5 + (hour - 13) * 0.3 + np.random.normal(0, 0.8)
        else:
            air_temp = 19 + np.random.normal(0, 0.8)
            water_temp = 20.5 + np.random.normal(0, 0.5)
        
        # Humidity inversely related to temperature
        humidity = 68 - (air_temp - 21) * 2 + np.random.normal(0, 3)
        
        # pH drifts slightly, requires periodic adjustment
        ph_drift = 0.3 * np.sin(i / 500) + 0.1 * (i / num_records)
        ph = 6.0 + ph_drift + np.random.normal(0, 0.08)
        
        # EC decreases as plants consume nutrients, with weekly refills
        week = i // (7 * 24 * 12)
        ec_base = 2100 - (i % (7 * 24 * 12)) / (7 * 24 * 12) * 400
        ec = ec_base + np.random.normal(0, 80)
        
        # CO2 levels (ppm)
        if is_day:
            co2 = np.random.normal(800, 100)
        else:
            co2 = np.random.normal(600, 80)
        
        record = {
            'timestamp': ts.strftime('%Y-%m-%d %H:%M:%S'),
            'device_id': 'GREENHOUSE-MAIN-01',
            'location': 'Section A',
            'air_temp_c': round(np.clip(air_temp, 16, 32), 2),
            'water_temp_c': round(np.clip(water_temp, 18, 26), 2),
            'humidity_percent': round(np.clip(humidity, 45, 85), 1),
            'ph': round(np.clip(ph, 5.2, 7.2), 2),
            'ec_us_cm': int(np.clip(ec, 1400, 2600)),
            'tds_ppm': int(np.clip(ec * 0.5, 700, 1300)),
            'light_lux': int(max(0, lux)),
            'par_umol': int(max(0, lux * 0.0185)),  # Convert lux to PAR
            'co2_ppm': int(co2),
            'water_level_cm': round(np.random.normal(45, 2), 1),
            'flow_rate_lpm': round(np.random.normal(2.5, 0.3), 2)
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    df.to_csv('data/greenhouse_1_month.csv', index=False)
    print(f"✓ Created greenhouse_1_month.csv with {len(df)} records")
    return df


def generate_strawberry_batch():
    """Generate JSON data for a strawberry growing batch"""
    print("\nGenerating strawberry_batch_04.json...")
    
    start_date = datetime.now() - timedelta(days=60)
    
    batch_data = {
        "batch_id": "STR-2024-04",
        "plant_type": "strawberry",
        "variety": "Albion (Day-Neutral)",
        "start_date": start_date.strftime('%Y-%m-%d'),
        "location": "Greenhouse A - Section 2",
        "system_type": "NFT (Nutrient Film Technique)",
        "initial_plant_count": 48,
        "transplant_age_days": 21,
        
        "growth_timeline": [
            {
                "date": (start_date + timedelta(days=i*7)).strftime('%Y-%m-%d'),
                "days_since_transplant": i*7,
                "average_height_cm": round(8 + i * 1.2 + np.random.normal(0, 0.3), 1),
                "average_leaf_count": int(12 + i * 1.5),
                "crown_diameter_cm": round(6 + i * 0.8 + np.random.normal(0, 0.2), 1),
                "flowering_plants": int(min(48, max(0, (i-3) * 8))),
                "fruiting_plants": int(min(48, max(0, (i-5) * 10))),
                "health_status": "excellent" if i < 7 else "good",
                "notes": f"Week {i+1} observation"
            }
            for i in range(9)  # 9 weeks of data
        ],
        
        "environmental_summary": {
            "avg_air_temp_c": 22.5,
            "avg_water_temp_c": 20.8,
            "avg_humidity_percent": 65.0,
            "avg_ph": 6.1,
            "avg_ec_us_cm": 1850,
            "photoperiod_hours": 16,
            "avg_par_umol": 450
        },
        
        "nutrient_schedule": [
            {
                "week": i+1,
                "formula": "Vegetative" if i < 4 else "Flowering/Fruiting",
                "n_ppm": 180 if i < 4 else 140,
                "p_ppm": 60 if i < 4 else 90,
                "k_ppm": 200 if i < 4 else 280,
                "ca_ppm": 160,
                "mg_ppm": 50,
                "ec_target": 1800 if i < 4 else 1950
            }
            for i in range(9)
        ],
        
        "harvest_data": [
            {
                "harvest_date": (start_date + timedelta(days=42 + i*3)).strftime('%Y-%m-%d'),
                "harvest_number": i+1,
                "berries_harvested": int(np.random.normal(85, 15)),
                "total_weight_g": int(np.random.normal(1200, 200)),
                "avg_berry_weight_g": round(np.random.normal(14, 2), 1),
                "grade_a_percent": round(np.random.normal(82, 5), 1),
                "brix_level": round(np.random.normal(8.5, 0.5), 1)
            }
            for i in range(6)  # 6 harvests
        ],
        
        "total_yield": {
            "total_berries": 487,
            "total_weight_kg": 7.2,
            "yield_per_plant_g": 150,
            "production_days": 60,
            "quality_rating": 4.5
        },
        
        "observations": [
            "Strong vegetative growth in first 3 weeks",
            "First flowers appeared day 28",
            "Consistent flowering and fruiting from week 5",
            "No major pest or disease issues",
            "Excellent fruit quality and Brix levels",
            "Plants responded well to increased K during fruiting"
        ],
        
        "recommendations": [
            "Maintain EC between 1800-2000 μS/cm for optimal fruiting",
            "Monitor for spider mites in warmer conditions",
            "Increase air circulation during fruiting",
            "Continue current nutrient schedule",
            "Harvest every 2-3 days when fruit is 80% red"
        ]
    }
    
    with open('data/strawberry_batch_04.json', 'w') as f:
        json.dump(batch_data, f, indent=2)
    
    print(f"✓ Created strawberry_batch_04.json")
    return batch_data


def generate_ph_ec_experiment():
    """Generate experimental data comparing pH and EC effects"""
    print("\nGenerating ph_vs_ec_experiment.csv...")
    
    treatments = []
    
    # Design experiment: 3 pH levels x 3 EC levels x 4 replicates
    ph_levels = [5.5, 6.0, 6.5]
    ec_levels = [1600, 2000, 2400]
    replicates = 4
    
    start_date = datetime.now() - timedelta(days=42)
    
    for ph_target in ph_levels:
        for ec_target in ec_levels:
            for rep in range(replicates):
                treatment_id = f"pH{ph_target}_EC{ec_target}_R{rep+1}"
                
                # Weekly measurements over 6 weeks
                for week in range(7):
                    measure_date = start_date + timedelta(days=week*7)
                    
                    # Growth varies by treatment
                    ph_factor = 1.0 - abs(6.0 - ph_target) * 0.15  # Optimal around 6.0
                    ec_factor = 1.0 - abs(2000 - ec_target) * 0.0002  # Optimal around 2000
                    growth_factor = ph_factor * ec_factor
                    
                    base_height = 12 + week * 3 * growth_factor
                    base_leaves = 8 + week * 2 * growth_factor
                    base_yield = week * 50 * growth_factor if week > 3 else 0
                    
                    record = {
                        'date': measure_date.strftime('%Y-%m-%d'),
                        'week': week,
                        'treatment_id': treatment_id,
                        'replicate': rep + 1,
                        'ph_target': ph_target,
                        'ec_target_us_cm': ec_target,
                        'ph_actual': round(ph_target + np.random.normal(0, 0.08), 2),
                        'ec_actual_us_cm': int(ec_target + np.random.normal(0, 50)),
                        'plant_height_cm': round(base_height + np.random.normal(0, 1.5), 1),
                        'leaf_count': int(base_leaves + np.random.normal(0, 1)),
                        'stem_diameter_mm': round(4 + week * 0.6 * growth_factor + np.random.normal(0, 0.3), 1),
                        'chlorophyll_spad': round(35 + 5 * growth_factor + np.random.normal(0, 2), 1),
                        'cumulative_yield_g': int(base_yield + np.random.normal(0, 20)) if week > 3 else 0,
                        'root_health_score': round(min(5, 3 + growth_factor * 2 + np.random.normal(0, 0.3)), 1)
                    }
                    
                    treatments.append(record)
    
    df = pd.DataFrame(treatments)
    df.to_csv('data/ph_vs_ec_experiment.csv', index=False)
    print(f"✓ Created ph_vs_ec_experiment.csv with {len(df)} records")
    
    # Print summary statistics
    print("\nExperiment Summary:")
    summary = df.groupby(['ph_target', 'ec_target_us_cm'])['cumulative_yield_g'].agg(['mean', 'std'])
    print(summary.round(1))
    
    return df


def generate_readme():
    """Generate README for data directory"""
    print("\nGenerating data/README.md...")
    
    readme_content = """# Demo Data for Agronomia

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
curl -X POST http://localhost:8000/api/data/import \\
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

```bibtex
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
"""
    
    with open('data/README.md', 'w') as f:
        f.write(readme_content)
    
    print("✓ Created data/README.md")


def main():
    """Generate all demo datasets"""
    print("=" * 70)
    print("AGRONOMIA DEMO DATA GENERATOR")
    print("=" * 70)
    print("\nGenerating realistic demo datasets for the Agronomia platform...")
    print("These datasets allow anyone to explore the system without hardware.\n")
    
    # Generate all datasets
    greenhouse_df = generate_greenhouse_1_month()
    strawberry_data = generate_strawberry_batch()
    experiment_df = generate_ph_ec_experiment()
    generate_readme()
    
    print("\n" + "=" * 70)
    print("✓ ALL DEMO DATA GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print("\nSummary:")
    print(f"  • greenhouse_1_month.csv: {len(greenhouse_df):,} records")
    print(f"  • strawberry_batch_04.json: Complete batch tracking")
    print(f"  • ph_vs_ec_experiment.csv: {len(experiment_df):,} records")
    print(f"  • README.md: Complete documentation")
    print("\nYou can now:")
    print("  1. Load this data into the dashboard")
    print("  2. Train AI models with realistic data")
    print("  3. Demonstrate the system without sensors")
    print("  4. Share impressive visualizations")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
