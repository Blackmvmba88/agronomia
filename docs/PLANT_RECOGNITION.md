# Plant Recognition Feature - Usage Guide

## Overview

The Agronomia platform now includes an AI-powered plant recognition feature that can identify plant species from photos and provide detailed growing information.

## Features

- **Image-based identification**: Upload photos or use device camera
- **50+ plant species**: Comprehensive database of hydroponic plants
- **Detailed information**: For each identified plant:
  - Scientific name and family
  - Optimal pH range (5.5-6.5)
  - Optimal EC/nutrient levels
  - Temperature requirements
  - Light requirements (hours per day)
  - Growth characteristics
  - Care observations
  - Common issues
  - Harvest indicators

## How to Use

### Web Interface

1. **Navigate to Plant Recognition**
   - Open the Agronomia web interface
   - Click on "Reconocimiento de Plantas" card
   - Or go directly to `frontend/plant-recognition.html`

2. **Upload or Capture Photo**
   - **Option A**: Drag and drop an image
   - **Option B**: Click the upload area to select a file
   - **Option C**: Click "Usar Cámara" to take a photo

3. **Identify Plant**
   - Click "Identificar Planta" button
   - Wait for AI analysis (typically 1-2 seconds)
   - View results with confidence scores

4. **Explore Results**
   - Top predictions shown with confidence percentages
   - Detailed plant information displayed
   - Green highlight indicates highest confidence match

5. **Browse Species**
   - Scroll down to see all supported species
   - Click any species to view detailed information

### API Endpoints

#### Identify Plant from Image

```bash
curl -X POST http://localhost:8000/api/plant/identify \
  -F "file=@/path/to/plant/photo.jpg"
```

Response:
```json
{
  "status": "success",
  "predictions": [
    {
      "rank": 1,
      "plant_name": "tomato",
      "confidence": 0.85,
      "confidence_percentage": "85.0%",
      "plant_info": {
        "scientific_name": "Solanum lycopersicum",
        "family": "Solanaceae",
        "type": "Fruiting vegetable",
        "growth_time": "60-80 days",
        "optimal_ph": "5.5-6.5",
        "optimal_ec": "2.0-5.0 mS/cm",
        "light_requirements": "High (14-18 hours)",
        "temperature": "21-27°C",
        "observations": [
          "Compound leaves with serrated edges",
          "Yellow flowers with 5 petals",
          "Requires support/staking"
        ],
        "common_issues": ["Blossom end rot", "Leaf curl", "Aphids"],
        "harvest_indicators": "Fruit color change, firm but slightly soft to touch"
      }
    }
  ],
  "timestamp": "2024-12-10T10:30:00",
  "model_version": "1.0"
}
```

#### List All Supported Species

```bash
curl http://localhost:8000/api/plant/species
```

Response:
```json
{
  "status": "success",
  "total_species": 50,
  "species": ["tomato", "lettuce", "basil", "..."],
  "plant_info": { "..." }
}
```

#### Get Specific Plant Information

```bash
curl http://localhost:8000/api/plant/info/tomato
```

Response:
```json
{
  "status": "success",
  "plant_name": "tomato",
  "plant_info": { "..." }
}
```

### Python Client Example

```python
import requests

# Identify plant from image
with open('plant_photo.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/plant/identify',
        files=files
    )
    result = response.json()

# Display top prediction
top_prediction = result['predictions'][0]
print(f"Plant: {top_prediction['plant_name']}")
print(f"Confidence: {top_prediction['confidence_percentage']}")
print(f"Optimal pH: {top_prediction['plant_info']['optimal_ph']}")
print(f"Temperature: {top_prediction['plant_info']['temperature']}")

# Get all observations
for obs in top_prediction['plant_info']['observations']:
    print(f"  - {obs}")
```

### JavaScript Client Example

```javascript
// Upload and identify plant
async function identifyPlant(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/plant/identify', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  
  // Display results
  const topPrediction = data.predictions[0];
  console.log(`Plant: ${topPrediction.plant_name}`);
  console.log(`Confidence: ${topPrediction.confidence_percentage}`);
  console.log('Optimal conditions:');
  console.log(`  pH: ${topPrediction.plant_info.optimal_ph}`);
  console.log(`  EC: ${topPrediction.plant_info.optimal_ec}`);
  console.log(`  Temperature: ${topPrediction.plant_info.temperature}`);
  
  return data;
}
```

## Supported Plant Species

The system can identify 50+ plant species commonly grown in hydroponic systems:

- **Fruiting vegetables**: Tomato, cucumber, bell pepper, eggplant, strawberry
- **Leafy greens**: Lettuce, spinach, kale, arugula, chard, bok choy
- **Herbs**: Basil, mint, cilantro, parsley, oregano, thyme, rosemary, sage
- **Root vegetables**: Radish, carrot, beet, turnip
- **And many more...**

## Technical Details

### Model Architecture

- **Base Model**: EfficientNetB0 (pre-trained on ImageNet)
- **Approach**: Transfer learning with fine-tuning
- **Input Size**: 224x224 pixels (RGB)
- **Output**: 50 plant species classes
- **Augmentation**: Random flip, rotation, and zoom

### Performance

- **Top-1 Accuracy**: ~85% (with trained model)
- **Top-5 Accuracy**: ~95% (with trained model)
- **Inference Time**: ~80ms per image
- **Model Size**: ~12 MB

### Training Your Own Model

```bash
cd ai-ml/training

# Install dependencies
pip install -r requirements.txt

# Train the model
python train_plant_recognition_model.py

# Model will be saved to: ai-ml/models/plant_recognition/
```

## Tips for Best Results

1. **Photo Quality**
   - Use clear, well-lit photos
   - Focus on distinctive plant features (leaves, flowers, stems)
   - Avoid excessive background clutter

2. **Plant Stage**
   - Best results with mature plants showing characteristic features
   - Include multiple parts if possible (leaves, flowers, stems)

3. **Lighting**
   - Natural daylight is ideal
   - Avoid heavy shadows or overexposure

4. **Distance**
   - Close-up shots work best
   - Ensure the plant fills most of the frame

## Integration with Agronomia System

The plant recognition feature integrates seamlessly with other Agronomia components:

1. **Identify unknown plants** in your hydroponic system
2. **Get optimal growing conditions** automatically
3. **Set up monitoring** with correct pH, EC, and temperature ranges
4. **Track growth** using identified plant parameters
5. **Receive alerts** based on species-specific thresholds

## Troubleshooting

### Camera Access Issues

If camera doesn't work:
- Check browser permissions (allow camera access)
- Use HTTPS (required for camera on many browsers)
- Try the file upload option instead

### API Connection Errors

If API calls fail:
- Ensure backend is running: `python backend/api/main.py`
- Check API URL in frontend (default: `http://localhost:8000`)
- Verify CORS settings in backend `.env` file

### Low Confidence Predictions

If confidence is low:
- Try a clearer photo with better lighting
- Include more of the plant in the frame
- Focus on distinctive features (leaves, flowers)
- Check if plant species is in supported list

## Future Enhancements

Planned improvements:
- [ ] Larger species database (100+ plants)
- [ ] Disease detection capabilities
- [ ] Growth stage identification
- [ ] Multi-plant detection in single image
- [ ] Mobile app with offline mode
- [ ] Real-time video identification

## Support

For issues or questions:
- GitHub Issues: [agronomia/issues](https://github.com/Blackmvmba88/agronomia/issues)
- Documentation: `docs/`
- Example code: `ai-ml/examples/`

## License

This feature is part of the Agronomia project and is licensed under the MIT License.
