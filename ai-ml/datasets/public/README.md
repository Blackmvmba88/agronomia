# Public Agricultural Datasets

This directory contains links and information about publicly available agricultural datasets that can be used with Agronomia for training and research.

---

## 🌍 Available Public Datasets

### 1. NASA Open Data Portal - Plant Growth Studies

**Source:** [NASA Data Portal](https://data.nasa.gov/)

**Datasets:**
- **Space Agriculture Studies**: Plant growth in controlled environments
- **Mars Simulation Greenhouse**: Long-duration crop production data
- **ISS Veggie Experiments**: Lettuce and other crops grown in microgravity

**Relevant Data:**
- Environmental conditions (temp, humidity, CO₂, light)
- Plant growth measurements
- Harvest yields and quality
- Nutrient solution monitoring

**How to Use:**
```bash
# Download NASA plant growth data
wget https://data.nasa.gov/api/views/xyz/rows.csv -O nasa_veggie_experiment.csv

# Load in Agronomia
python ai-ml/training/train_harvest_model.py --data nasa_veggie_experiment.csv
```

**Citation:**
```
NASA Open Data Portal (2024). Plant Growth Experiments.
Available at: https://data.nasa.gov/
```

---

### 2. Kaggle - IoT Sensor Datasets

**Source:** [Kaggle Datasets](https://www.kaggle.com/datasets)

**Relevant Datasets:**
- **"IoT Greenhouse Monitoring"** - 6 months of sensor data
- **"Hydroponic Lettuce Growth"** - Complete growth cycles
- **"Smart Farm Sensor Network"** - Multi-sensor agricultural data

**Download:**
```bash
# Install Kaggle CLI
pip install kaggle

# Configure API key (get from kaggle.com/account)
# Then download dataset
kaggle datasets download -d username/iot-greenhouse-monitoring
unzip iot-greenhouse-monitoring.zip -d ai-ml/datasets/public/kaggle/
```

**Use Cases:**
- Train baseline models
- Validate Agronomia predictions
- Compare performance across systems

---

### 3. PlantCV Dataset Library

**Source:** [PlantCV](https://plantcv.readthedocs.io/)

**Datasets:**
- Arabidopsis phenotyping
- Tomato growth series
- Root system imaging
- Multi-spectral plant imaging

**Focus:** Computer vision and image analysis

**Integration:**
```python
# Future: integrate PlantCV for image analysis
from plantcv import plantcv as pcv
# Analyze plant health from images
```

---

### 4. Open Agriculture Data Alliance (OADA)

**Source:** [Open Ag Data Alliance](https://openag.io/)

**Datasets:**
- Weather and climate data
- Soil analysis results
- Crop yield histories
- Equipment sensor logs

**API Access:**
```python
import requests

# Example API call
response = requests.get('https://api.openag.io/datasets/hydroponics')
data = response.json()
```

---

### 5. University Research Repositories

#### Cornell University - Controlled Environment Agriculture
**URL:** [Cornell CEA-Hub](https://cea.cals.cornell.edu/)

**Datasets:**
- LED light spectrum experiments
- Nutrient solution optimization studies
- Energy usage in greenhouses

#### University of Arizona - CEAC Data
**URL:** [UA CEAC](https://ceac.arizona.edu/)

**Datasets:**
- Desert climate greenhouse operations
- Water use efficiency studies
- Temperature management strategies

---

### 6. European Commission - JRC MARS

**Source:** [JRC MARS](https://mars.jrc.ec.europa.eu/)

**Datasets:**
- Crop monitoring data across Europe
- Agricultural statistics
- Weather data integrated with yield

**Access:**
```python
# API example
import requests
url = "https://mars.jrc.ec.europa.eu/api/data"
data = requests.get(url).json()
```

---

## 📥 How to Add Public Datasets

### 1. Download to Local Directory
```bash
cd ai-ml/datasets/public/
mkdir dataset-name
cd dataset-name
wget <dataset-url>
```

### 2. Document the Dataset
Create a `README.md` in the dataset directory:
```markdown
# Dataset Name

**Source:** URL
**Date Downloaded:** YYYY-MM-DD
**License:** License type
**Description:** Brief description

## Files
- file1.csv - Description
- file2.json - Description

## Citation
[Citation information]
```

### 3. Integrate with Agronomia
```python
# Example training script
from agronomia.ml import IrrigationModel

model = IrrigationModel()
model.train(data='datasets/public/dataset-name/data.csv')
model.save('models/irrigation_model_v2.pkl')
```

---

## 🔄 Data Preprocessing

Most public datasets need preprocessing to work with Agronomia:

```python
import pandas as pd

# Load external dataset
df = pd.read_csv('public/external-data.csv')

# Standardize column names
column_mapping = {
    'temp': 'air_temp_c',
    'RH': 'humidity_percent',
    'EC': 'ec_us_cm',
    # ... more mappings
}
df = df.rename(columns=column_mapping)

# Handle missing values
df = df.fillna(method='ffill')

# Save in Agronomia format
df.to_csv('processed/external-data-agronomia.csv', index=False)
```

---

## 📊 Dataset Comparison

| Dataset | Size | Format | Update Freq | Focus Area |
|---------|------|--------|-------------|------------|
| NASA Veggie | 50K rows | CSV | Static | Space agriculture |
| Kaggle IoT | 200K rows | CSV/JSON | Static | Greenhouse sensors |
| PlantCV | Images | PNG/TIFF | Static | Plant phenotyping |
| OADA | API | JSON | Real-time | General agriculture |
| Cornell CEA | 30K rows | CSV | Quarterly | CEA research |

---

## 🎓 Educational Use

### For Students
1. Download small datasets (Kaggle, Cornell)
2. Explore with Jupyter notebooks
3. Compare with Agronomia demo data
4. Train simple models

### For Researchers
1. Access comprehensive datasets (NASA, JRC)
2. Validate research findings
3. Publish reproducible research
4. Contribute back cleaned data

### For Developers
1. Use diverse data for testing
2. Validate edge cases
3. Improve model robustness
4. Benchmark performance

---

## ⚖️ Licensing & Attribution

**Always check license before using:**
- Public domain: ✓ Free to use
- CC-BY: ✓ Free with attribution
- CC-BY-SA: ✓ Free, must share derivatives
- Proprietary: ✗ Need permission

**Best Practices:**
- Keep original README with attribution
- Cite datasets in publications
- Share improvements back to community
- Respect usage restrictions

---

## 🔍 Finding More Datasets

### Search Engines
- [Google Dataset Search](https://datasetsearch.research.google.com/)
- [Data.gov](https://data.gov/)
- [Kaggle](https://www.kaggle.com/datasets)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/)

### Keywords
- "hydroponic dataset"
- "greenhouse monitoring data"
- "plant growth measurements"
- "controlled environment agriculture"
- "IoT agriculture sensors"

---

## 🤝 Contributing Datasets

Have a public dataset to share?

1. Fork the repository
2. Add dataset information to this README
3. Include preprocessing scripts
4. Document license and citation
5. Submit pull request

---

## 📚 Research Papers with Datasets

### Papers with Public Data
- "Deep Learning for Hydroponic Lettuce Growth" - Dataset available
- "IoT-based Smart Greenhouse" - Sensor logs published
- "Nutrient Solution Optimization" - Experimental data shared

### How to Access
Usually mentioned in paper's "Data Availability" section or supplementary materials.

---

## 🌱 Integration Examples

### Example 1: Augment Training Data
```python
# Combine Agronomia data with public datasets
import pandas as pd

agronomia_data = pd.read_csv('data/greenhouse_1_month.csv')
public_data = pd.read_csv('datasets/public/kaggle/greenhouse_data.csv')

# Align schemas
public_data = preprocess_public_data(public_data)

# Combine
combined = pd.concat([agronomia_data, public_data])

# Train model with more data
model.train(combined)
```

### Example 2: Validation
```python
# Validate model on external data
test_data = pd.read_csv('datasets/public/cornell/test_set.csv')
predictions = model.predict(test_data)
accuracy = evaluate(predictions, test_data['actual'])
print(f"External validation accuracy: {accuracy}")
```

---

## 📞 Questions?

- GitHub Issues for dataset suggestions
- Email: research@agronomia.example.com
- Community forum for discussions

---

**Open data accelerates innovation. Share and contribute! 📊🌍**

*Last Updated: 2024-12-10*
