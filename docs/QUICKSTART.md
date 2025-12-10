# Quick Start Guide

Get Agronomia running in 5 minutes!

## Prerequisites

- **Docker** and **Docker Compose** installed
- **OR** Python 3.8+ and Node.js 16+ (for local development)
- **Arduino IDE** (for hardware, optional)

## Option 1: Docker (Recommended)

### 1. Clone Repository

```bash
git clone https://github.com/Blackmvmba88/agronomia.git
cd agronomia
```

### 2. Start Services

```bash
docker-compose up -d
```

This starts:
- MQTT Broker (port 1883)
- PostgreSQL Database (port 5432)
- InfluxDB (port 8086)
- Backend API (port 8000)
- Frontend Web App (port 3000)
- Grafana (port 3001)

### 3. Access Applications

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/agronomia)

### 4. Verify Services

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f api
```

### 5. Test with Demo Data

The dashboard will show demo data automatically if no real devices are connected.

## Option 2: Local Development

### Backend Setup

```bash
cd backend/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start API server
python main.py
```

API will be available at http://localhost:8000

### Frontend Setup

```bash
cd frontend/web

# Open in browser or use local server
python -m http.server 3000
# OR
npx http-server -p 3000
```

Frontend will be available at http://localhost:3000

### MQTT Broker (Optional)

```bash
# Install Mosquitto
# Ubuntu/Debian:
sudo apt install mosquitto mosquitto-clients

# macOS:
brew install mosquitto

# Start broker
mosquitto -v
```

## Option 3: Hardware Setup (ESP32)

### 1. Hardware Requirements

- ESP32 DevKit board
- pH sensor
- DHT22 (temperature/humidity)
- DS18B20 (water temperature)
- TSL2591 (light sensor)
- EC/TDS sensor
- Breadboard and jumper wires

### 2. Install Arduino IDE

Download from https://www.arduino.cc/en/software

### 3. Install ESP32 Board Support

1. Open Arduino IDE
2. File → Preferences
3. Add to "Additional Board Manager URLs":
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Tools → Board → Boards Manager
5. Search "ESP32" and install

### 4. Install Libraries

Tools → Manage Libraries, install:
- PubSubClient
- ArduinoJson
- DHT sensor library
- OneWire
- DallasTemperature
- Adafruit TSL2591 Library

### 5. Configure Firmware

```bash
cd firmware/esp32
cp config.h.example config.h
# Edit config.h with your WiFi and MQTT settings
```

### 6. Upload Firmware

1. Connect ESP32 via USB
2. Tools → Board → "ESP32 Dev Module"
3. Tools → Port → Select your ESP32 port
4. Click Upload button
5. Open Serial Monitor (115200 baud) to verify

## Verify Installation

### Check API

```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "name": "Agronomia API",
  "version": "1.0.0",
  "status": "online"
}
```

### Check MQTT

```bash
# Subscribe to all topics
mosquitto_sub -h localhost -t 'agronomia/#' -v

# In another terminal, publish test data
mosquitto_pub -h localhost -t 'agronomia/devices/ESP32-001/data' -m '{"device_id":"ESP32-001","sensors":{"ph":6.2,"temp":23}}'
```

### Check Database

```bash
# Connect to PostgreSQL
docker exec -it agronomia-db psql -U agronomia

# List tables
\dt

# Query devices
SELECT * FROM devices;
```

## Quick Test Workflow

### 1. Generate Sample Data

```bash
cd ai-ml/datasets
pip install pandas numpy
python generate_sample_data.py
```

### 2. Import to Database

```bash
# Use API to import data
curl -X POST http://localhost:8000/api/sensors/data \
  -H "Content-Type: application/json" \
  -d @sensor_data_sample.json
```

### 3. View in Dashboard

Open http://localhost:3000 and you'll see:
- Real-time sensor values
- Historical charts
- AI recommendations
- Alert status

## Train AI Models

```bash
cd ai-ml/training
pip install -r requirements.txt

# Train all models (takes 2-5 minutes)
python train_irrigation_model.py
python train_nutrient_model.py
python train_harvest_model.py
```

Models will be saved to `ai-ml/models/`

## Common Issues

### Port Already in Use

```bash
# Change port in docker-compose.yml or kill process
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Docker Services Not Starting

```bash
# Check logs
docker-compose logs service_name

# Restart specific service
docker-compose restart api

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### ESP32 Won't Connect to WiFi

- Verify 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Check SSID/password in config.h
- Ensure router allows new devices
- Check serial monitor for error messages

### Sensors Show -127 or NaN

- Check wiring connections
- Verify pull-up resistors (4.7kΩ for I2C/OneWire)
- Test sensors individually
- Run I2C scanner

## Next Steps

1. **Read Documentation**
   - [Hardware Setup](hardware/docs/SETUP.md)
   - [API Documentation](backend/api/README.md)
   - [Deployment Guide](docs/DEPLOYMENT.md)
   - [Architecture](docs/ARCHITECTURE.md)

2. **Customize Configuration**
   - Update alert thresholds
   - Configure plant types
   - Set up notifications
   - Add more devices

3. **Explore Features**
   - View historical data
   - Test AI predictions
   - Configure alerts
   - Export data

4. **Production Deployment**
   - Follow [Deployment Guide](docs/DEPLOYMENT.md)
   - Set up SSL/TLS
   - Configure backups
   - Enable monitoring

## Getting Help

- **Documentation**: Browse `docs/` directory
- **Issues**: https://github.com/Blackmvmba88/agronomia/issues
- **Discussions**: GitHub Discussions tab
- **API Docs**: http://localhost:8000/docs

## Success! 🎉

You now have a fully functional autonomous agronomy platform!

### What's Working:
✅ Real-time sensor monitoring
✅ Historical data tracking
✅ AI-powered predictions
✅ Alert system
✅ Web dashboard
✅ API endpoints
✅ Database storage

### What's Next:
- Connect real hardware
- Collect actual data
- Train models on real data
- Deploy to production
- Monitor your hydroponic system!

---

**Happy Farming! 🌱**
