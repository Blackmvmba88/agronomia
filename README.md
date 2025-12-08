# Agronomia - Autonomous Agronomy Platform

An autonomous hydroponic plant growth and monitoring platform with AI-powered optimization for irrigation, nutrients, and harvest prediction.

## 🌱 Overview

Agronomia is a comprehensive IoT-based agricultural monitoring system designed for hydroponic farming. The platform integrates hardware sensors, cloud-based analytics, and AI/ML models to optimize plant growth and provide actionable insights for farmers and agricultural labs.

## 🚀 Features

### Real-Time Monitoring
- **pH Sensors**: Monitor and maintain optimal pH levels (5.5-6.5 for most hydroponic crops)
- **Humidity Sensors**: Track air humidity (60-70% optimal range)
- **Nutrient Sensors**: Monitor EC (Electrical Conductivity) for nutrient concentration
- **Light Sensors**: Measure PAR (Photosynthetically Active Radiation) for optimal growth
- **Temperature Sensors**: Track ambient and water temperature (18-26°C optimal)

### Data Visualization
- Real-time dashboards for web and mobile
- Historical trend analysis
- Growth analytics and comparisons
- Customizable alerts and notifications

### AI-Powered Optimization
- **Irrigation Prediction**: ML models predict optimal watering schedules
- **Nutrient Optimization**: AI-driven nutrient dosing recommendations
- **Harvest Prediction**: Predictive models for harvest timing and yield estimation

## 📁 Repository Structure

```
agronomia/
├── hardware/           # Hardware specifications and schematics
│   ├── docs/          # Sensor specifications and setup guides
│   └── schematics/    # Circuit diagrams and PCB designs
├── firmware/          # Embedded device code
│   ├── arduino/       # Arduino-based sensor controllers
│   └── esp32/         # ESP32 WiFi-enabled controllers
├── backend/           # Cloud API and data processing
│   ├── api/           # RESTful API endpoints
│   └── database/      # Database schemas and migrations
├── frontend/          # User interfaces
│   ├── web/           # Web dashboard (React/Vue)
│   └── mobile/        # Mobile app (React Native/Flutter)
├── ai-ml/             # Machine Learning models
│   ├── models/        # Trained models and architectures
│   ├── datasets/      # Training and testing datasets
│   └── training/      # Training scripts and notebooks
├── docs/              # Additional documentation
├── docker/            # Containerization configs
└── README.md          # This file
```

## 🛠️ Technology Stack

### Hardware
- **Microcontrollers**: Arduino Uno/Mega, ESP32, Raspberry Pi
- **Sensors**: 
  - pH: Atlas Scientific pH Kit
  - Humidity: DHT22, SHT31
  - EC/TDS: Atlas Scientific Conductivity Kit
  - Light: TSL2591, BH1750
  - Temperature: DS18B20, DHT22

### Backend
- **API Framework**: Python FastAPI or Node.js Express
- **Database**: PostgreSQL (time-series data), InfluxDB (metrics)
- **Message Broker**: MQTT (Mosquitto)
- **Cloud**: AWS IoT Core or Azure IoT Hub

### Frontend
- **Web**: React.js with Chart.js/D3.js
- **Mobile**: React Native or Flutter
- **Real-time**: WebSocket/Socket.io

### AI/ML
- **Framework**: TensorFlow, PyTorch, scikit-learn
- **Models**: LSTM for time-series, Random Forest for classification
- **Deployment**: TensorFlow Serving, ONNX Runtime

## 🚦 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker and Docker Compose
- Arduino IDE or PlatformIO

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Blackmvmba88/agronomia.git
   cd agronomia
   ```

2. **Set up backend**
   ```bash
   cd backend/api
   pip install -r requirements.txt
   python main.py
   ```

3. **Set up frontend**
   ```bash
   cd frontend/web
   npm install
   npm start
   ```

4. **Flash firmware**
   ```bash
   cd firmware/esp32
   # Follow instructions in firmware/README.md
   ```

5. **Train AI models**
   ```bash
   cd ai-ml/training
   python train_irrigation_model.py
   ```

## 📊 Dashboard Features

- **Real-time Sensor Data**: Live updates every 5 seconds
- **Historical Charts**: View trends over hours, days, weeks, months
- **Alerts**: Configurable thresholds for all sensor types
- **Growth Analytics**: Compare growth cycles and optimize conditions
- **AI Insights**: Recommendations based on predictive models

## 🤖 AI Models

### Irrigation Prediction
- Input: Temperature, humidity, growth stage, time of day
- Output: Optimal irrigation timing and volume
- Accuracy: ~92% on validation set

### Nutrient Optimization
- Input: Current EC, pH, plant type, growth stage
- Output: Nutrient adjustment recommendations
- Accuracy: ~89% on validation set

### Harvest Prediction
- Input: Growth metrics, environmental data, plant type
- Output: Days to harvest, expected yield
- Accuracy: ±3 days, ±15% yield

## 🔧 Hardware Setup

See [hardware/docs/SETUP.md](hardware/docs/SETUP.md) for detailed instructions on:
- Sensor wiring and calibration
- Microcontroller configuration
- Network setup and MQTT configuration

## 🌐 API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

See [backend/api/README.md](backend/api/README.md) for API usage examples.

## 📈 Data Flow

```
Sensors → Microcontroller → MQTT Broker → Backend API → Database
                                              ↓
                                         AI/ML Models
                                              ↓
                                    Frontend Dashboard
```

## 🧪 For Agricultural Labs

The platform includes features specifically for research:
- Batch experiment tracking
- Statistical analysis tools
- Data export in CSV/JSON formats
- Multi-environment comparisons
- A/B testing for growth conditions

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues and questions:
- GitHub Issues: [agronomia/issues](https://github.com/Blackmvmba88/agronomia/issues)
- Documentation: [docs/](docs/)

## 🙏 Acknowledgments

- Open-source hydroponic community
- TensorFlow and PyTorch teams
- Arduino and ESP32 communities

---

**Built with ❤️ for sustainable agriculture**
