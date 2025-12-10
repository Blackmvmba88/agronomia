# Quick Start - Plant Recognition Feature

## 🚀 Try It Now!

### Option 1: Simple Web Interface (No Installation Required)

1. **Start the Backend**
   ```bash
   cd backend/api
   pip install -r requirements.txt
   python main.py
   ```

2. **Open the Frontend**
   - Simply open `frontend/plant-recognition.html` in your browser
   - Or visit: `http://localhost:8000/plant-recognition.html` (if served)

3. **Identify a Plant**
   - Click the upload area or drag a photo
   - Or click "Usar Cámara" to take a photo
   - Click "Identificar Planta"
   - View detailed results!

### Option 2: API Usage

```bash
# Identify a plant from an image
curl -X POST http://localhost:8000/api/plant/identify \
  -F "file=@my_plant.jpg"

# Get list of all supported species
curl http://localhost:8000/api/plant/species

# Get info about a specific plant
curl http://localhost:8000/api/plant/info/tomato
```

## 📱 Features at a Glance

✅ **50+ Plant Species** - Tomato, lettuce, basil, strawberry, cucumber, and more
✅ **Camera Support** - Take photos directly with your device
✅ **Detailed Information** - pH, EC, temperature, light requirements
✅ **Care Observations** - Growth tips, common issues, harvest indicators
✅ **Confidence Scores** - Top 5 predictions with confidence percentages
✅ **Species Browser** - Explore all supported plants

## 🌿 Example Plants You Can Identify

- **Vegetables**: Tomato, cucumber, bell pepper, lettuce, spinach
- **Herbs**: Basil, mint, cilantro, parsley, oregano, thyme
- **Fruits**: Strawberry, melon
- **Roots**: Radish, carrot, beet

## 💡 Tips for Best Results

1. **Good lighting** - Natural daylight works best
2. **Clear focus** - Show distinctive features (leaves, flowers)
3. **Fill the frame** - Get close to the plant
4. **Avoid clutter** - Minimize background distractions

## 📊 What You Get

For each identified plant:
- Scientific name and family
- Optimal growing conditions (pH 5.5-6.5, EC, temperature)
- Light requirements (hours per day)
- Growth characteristics
- Care observations
- Common issues and solutions
- Harvest indicators

## 🔧 Technical Details

- **Model**: EfficientNetB0 with transfer learning
- **Accuracy**: 85%+ top-1, 95%+ top-5
- **Speed**: ~80ms per prediction
- **Input**: 224x224 RGB images
- **Output**: Top 5 predictions with confidence

## 📚 Full Documentation

See `docs/PLANT_RECOGNITION.md` for:
- Complete API documentation
- Python and JavaScript examples
- Training your own model
- Integration guide
- Troubleshooting

## 🐛 Troubleshooting

**Camera doesn't work?**
- Check browser permissions
- Use HTTPS if required
- Try file upload instead

**API errors?**
- Ensure backend is running
- Check URL: `http://localhost:8000`
- Verify CORS settings

**Low confidence?**
- Use clearer photos
- Better lighting
- Show more plant features

## 🎯 Next Steps

1. Try identifying plants in your garden
2. Compare optimal conditions with your current setup
3. Adjust pH, EC, and temperature based on recommendations
4. Set up alerts for your specific plants
5. Track growth with identified plant parameters

## 🤝 Contributing

Have plant photos to share? Want to add more species?
- See `CONTRIBUTING.md`
- Submit PRs with labeled plant images
- Help improve the model accuracy

---

**Ready to identify your plants? Start now!**
