# AI/ML Notebooks for Agronomia

This directory contains Jupyter notebooks for exploring data, training models, and making predictions.

## 📓 Available Notebooks

### 1. data_exploration.ipynb
**Purpose:** Explore and visualize greenhouse sensor data

**What you'll learn:**
- Load and inspect sensor data
- Visualize time series patterns
- Analyze correlations
- Detect anomalies
- Understand day/night cycles

**Prerequisites:**
```bash
pip install jupyter pandas numpy matplotlib seaborn scipy
```

**Run:**
```bash
jupyter notebook data_exploration.ipynb
```

---

### 2. train_irrigation_model.ipynb
**Purpose:** Train a machine learning model to predict optimal irrigation timing

**Features:**
- Data preprocessing and feature engineering
- Model selection (LSTM, Random Forest, XGBoost)
- Training with cross-validation
- Model evaluation and metrics
- Save trained model

**Prerequisites:**
```bash
pip install scikit-learn tensorflow xgboost
```

---

### 3. predict_irrigation.ipynb
**Purpose:** Use trained models to make irrigation predictions

**Features:**
- Load pre-trained model
- Real-time prediction from sensor data
- Recommendation generation
- Confidence scores
- Export predictions

---

### 4. plot_growth_curves.ipynb
**Purpose:** Analyze plant growth over time

**Features:**
- Growth trajectory visualization
- Compare different treatments
- Statistical analysis
- Yield prediction
- Generate reports

---

### 5. nutrient_optimization.ipynb
**Purpose:** Optimize nutrient schedules using ML

**Features:**
- pH and EC analysis
- Treatment comparison
- Recommendation engine
- Cost optimization
- Schedule generation

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd ai-ml/notebooks
pip install -r requirements.txt
```

### 2. Generate Demo Data
```bash
cd ../../data
python generate_demo_data.py
```

### 3. Launch Jupyter
```bash
jupyter notebook
```

### 4. Open a Notebook
Start with `data_exploration.ipynb` to familiarize yourself with the data.

---

## 📊 Example Workflow

### For Data Scientists:
1. **Explore** → `data_exploration.ipynb`
2. **Train** → `train_irrigation_model.ipynb`
3. **Evaluate** → Review metrics and visualizations
4. **Deploy** → Export model to production

### For Researchers:
1. **Design Experiment** → Use `ph_vs_ec_experiment.csv`
2. **Analyze Results** → `plot_growth_curves.ipynb`
3. **Statistical Tests** → `nutrient_optimization.ipynb`
4. **Report** → Generate publication-ready figures

### For Developers:
1. **Understand Data** → `data_exploration.ipynb`
2. **Test Predictions** → `predict_irrigation.ipynb`
3. **Integrate** → Use models in backend API
4. **Monitor** → Track model performance

---

## 💡 Tips

- **Start Simple:** Begin with data exploration before jumping into modeling
- **Use Demo Data:** All notebooks work with the provided demo datasets
- **Experiment:** Modify parameters and see how they affect results
- **Document:** Add your own markdown cells to explain findings
- **Share:** Export notebooks as HTML or PDF for presentations

---

## 🔧 Troubleshooting

### Kernel Issues
```bash
python -m ipykernel install --user --name=agronomia
```

### Import Errors
```bash
pip install -r requirements.txt
```

### Data Not Found
Make sure you're running from the notebooks directory or use absolute paths:
```python
df = pd.read_csv('../../data/greenhouse_1_month.csv')
```

---

## 📚 Learning Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)
- [Seaborn Gallery](https://seaborn.pydata.org/examples/index.html)

---

## 🤝 Contributing

To add new notebooks:
1. Follow the naming convention: `verb_noun.ipynb`
2. Include clear markdown documentation
3. Add to this README
4. Test with demo data
5. Submit a pull request

---

## 📝 Citation

If you use these notebooks in research:

```bibtex
@misc{agronomia_notebooks_2024,
  title={Agronomia AI/ML Notebooks},
  author={Agronomia Project Contributors},
  year={2024},
  url={https://github.com/Blackmvmba88/agronomia}
}
```

---

**Happy Data Science! 🌱📊**
