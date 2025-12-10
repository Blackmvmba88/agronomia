# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AGRONOMIA PLATFORM ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              IoT / HARDWARE LAYER                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   ESP32      │  │   Arduino    │  │ Raspberry Pi │  │   Sensors    │   │
│  │   WiFi/BLE   │  │   Mega       │  │   Camera     │  │   Array      │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                  │                 │            │
│         └─────────────────┴──────────────────┴─────────────────┘            │
│                                      │                                       │
│                                      ↓                                       │
│         ┌─────────────────────────────────────────────────┐                 │
│         │  Sensor Readings (JSON over MQTT/WiFi)         │                 │
│         │  • pH, EC, TDS, Temperature, Humidity          │                 │
│         │  • Light (Lux, PAR, Spectrum)                  │                 │
│         │  • CO₂, Water Level, Flow Rate                 │                 │
│         └─────────────────────────────────────────────────┘                 │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MESSAGE BROKER LAYER                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                        ┌──────────────────────┐                             │
│                        │   MQTT Broker        │                             │
│                        │   (Mosquitto)        │                             │
│                        │                      │                             │
│                        │  Topics:             │                             │
│                        │  agronomia/devices/  │                             │
│                        │    ├─ data           │                             │
│                        │    ├─ status         │                             │
│                        │    └─ control        │                             │
│                        └──────────┬───────────┘                             │
│                                   │                                          │
│                    ┌──────────────┼──────────────┐                          │
│                    │              │              │                          │
└────────────────────┼──────────────┼──────────────┼──────────────────────────┘
                     │              │              │
                     ↓              ↓              ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            BACKEND SERVICES                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                     FastAPI REST API                                │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌─────────────┐ ┌────────────┐ │    │
│  │  │ Device Mgmt  │ │ Sensor Data  │ │   Alerts    │ │   Users    │ │    │
│  │  │   Endpoints  │ │   Ingestion  │ │  Management │ │   & Auth   │ │    │
│  │  └──────────────┘ └──────────────┘ └─────────────┘ └────────────┘ │    │
│  │                                                                      │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌─────────────┐                │    │
│  │  │  WebSocket   │ │  Analytics   │ │   Reports   │                │    │
│  │  │  Real-time   │ │   Service    │ │  Generator  │                │    │
│  │  └──────────────┘ └──────────────┘ └─────────────┘                │    │
│  └────────────────────────────┬───────────────────────────────────────┘    │
│                                │                                             │
│                    ┌───────────┼───────────┐                                │
│                    ↓           ↓           ↓                                │
│         ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                    │
│         │ PostgreSQL  │ │  InfluxDB   │ │   Redis     │                    │
│         │  (Metadata) │ │ (Time-Series│ │  (Cache &   │                    │
│         │  • Devices  │ │  Metrics)   │ │   Sessions) │                    │
│         │  • Users    │ │  • Sensor   │ │  • Real-time│                    │
│         │  • Configs  │ │    Readings │ │    Data     │                    │
│         └─────────────┘ └─────────────┘ └─────────────┘                    │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                            AI/ML SERVICES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐  ┌────────────────────────┐                    │
│  │  Irrigation Prediction │  │  Nutrient Optimization │                    │
│  │  • LSTM Neural Network │  │  • Gradient Boosting   │                    │
│  │  • Input: 24h history  │  │  • Input: Current EC,  │                    │
│  │  • Output: Timing &    │  │    pH, plant stage     │                    │
│  │    volume              │  │  • Output: Adjustments │                    │
│  └────────────────────────┘  └────────────────────────┘                    │
│                                                                              │
│  ┌────────────────────────┐  ┌────────────────────────┐                    │
│  │  Harvest Prediction    │  │  Anomaly Detection     │                    │
│  │  • XGBoost Regressor   │  │  • Isolation Forest    │                    │
│  │  • Input: Growth data, │  │  • Input: Sensor       │                    │
│  │    environment         │  │    streams             │                    │
│  │  • Output: Days to     │  │  • Output: Alerts &    │                    │
│  │    harvest, yield      │  │    notifications       │                    │
│  └────────────────────────┘  └────────────────────────┘                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────┐           │
│  │  Model Storage & Versioning                                 │           │
│  │  • irrigation_model_v1.pkl                                  │           │
│  │  • nutrient_model_v1.pkl                                    │           │
│  │  • harvest_model_v1.pkl                                     │           │
│  └─────────────────────────────────────────────────────────────┘           │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                      Web Dashboard (React/Vue)                   │      │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │      │
│  │  │  Real-time   │ │  Historical  │ │   Device     │            │      │
│  │  │   Sensors    │ │    Charts    │ │  Management  │            │      │
│  │  └──────────────┘ └──────────────┘ └──────────────┘            │      │
│  │                                                                  │      │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │      │
│  │  │    Alerts    │ │ AI Insights  │ │   Reports    │            │      │
│  │  │ & Notifications│ │ & Predictions│ │  & Export   │            │      │
│  │  └──────────────┘ └──────────────┘ └──────────────┘            │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                    Mobile App (React Native)                     │      │
│  │  • Push notifications                                            │      │
│  │  • Offline mode                                                  │      │
│  │  • Quick actions                                                 │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                    Grafana Dashboards                            │      │
│  │  • Advanced analytics                                            │      │
│  │  • Custom queries                                                │      │
│  │  • Team collaboration                                            │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

  Sensor Reading → MQTT → Backend API → Database Storage
                                    ↓
                               AI Analysis
                                    ↓
                          Predictions/Alerts
                                    ↓
                        WebSocket Broadcast
                                    ↓
                          Frontend Update


┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEPLOYMENT OPTIONS                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  Development:
  ┌──────────────────────────────────────────────┐
  │  Local Machine                               │
  │  • Docker Compose                            │
  │  • SQLite (dev database)                     │
  │  • No SSL                                    │
  └──────────────────────────────────────────────┘

  Production:
  ┌──────────────────────────────────────────────┐
  │  Cloud Infrastructure (AWS/Azure/GCP)        │
  │  • Kubernetes Orchestration                  │
  │  • Managed PostgreSQL                        │
  │  • Load Balancing                            │
  │  • Auto-scaling                              │
  │  • TLS/SSL Encryption                        │
  │  • Multi-region (optional)                   │
  └──────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                            SECURITY LAYERS                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────┐
  │   TLS/SSL       │  All connections encrypted
  ├─────────────────┤
  │   JWT Auth      │  API authentication
  ├─────────────────┤
  │   MQTT ACL      │  Device authorization
  ├─────────────────┤
  │   RBAC          │  Role-based access
  ├─────────────────┤
  │   Firewall      │  Network protection
  └─────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                         MONITORING & LOGGING                                 │
└─────────────────────────────────────────────────────────────────────────────┘

  Prometheus  →  Grafana       (System metrics)
  Logs        →  ELK Stack     (Centralized logging)
  Alerts      →  PagerDuty     (Incident management)
  Uptime      →  UptimeRobot   (Availability monitoring)
```

## Quick Reference

### Technology Stack
- **Hardware**: ESP32, Arduino, Raspberry Pi
- **Sensors**: pH, EC, DHT22, DS18B20, TSL2591
- **Protocol**: MQTT (Mosquitto)
- **Backend**: Python FastAPI
- **Databases**: PostgreSQL, InfluxDB, Redis
- **AI/ML**: TensorFlow, scikit-learn, XGBoost
- **Frontend**: React/Vue.js, WebSocket
- **Deployment**: Docker, Kubernetes

### Ports
- `1883` - MQTT
- `8883` - MQTTS (SSL)
- `8000` - Backend API
- `3000` - Frontend Dev Server
- `5432` - PostgreSQL
- `8086` - InfluxDB
- `6379` - Redis

### Key Features
✓ Real-time sensor monitoring  
✓ AI-powered predictions  
✓ Automated alerts  
✓ Historical analytics  
✓ Multi-device support  
✓ RESTful API  
✓ WebSocket real-time updates  
✓ Mobile-ready dashboard  
