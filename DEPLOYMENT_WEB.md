# Web Application Deployment Summary

## Overview
This document summarizes the web application setup for the Agronomia hydroponic monitoring platform.

## Available Dashboards

### 1. Landing Page
- **File**: `frontend/index.html`
- **Purpose**: Entry point to choose between dashboards
- **Access**: Open directly in browser or serve via HTTP server

### 2. Simple HTML Dashboard
- **Location**: `frontend/web/index.html`
- **Technology**: HTML, CSS, JavaScript, Chart.js
- **Features**:
  - Real-time sensor monitoring
  - Interactive charts
  - WebSocket support
  - Demo mode with simulated data
  - No installation required
- **Ideal for**: Quick demos, learning, testing

### 3. React Dashboard
- **Location**: `frontend/src/`
- **Technology**: React 18, Material-UI, Recharts, Axios
- **Features**:
  - Modern Material Design interface
  - Real-time sensor monitoring
  - Actuator controls (pump, lights)
  - Configurable alerts
  - Historical data visualization
  - Responsive design
- **Ideal for**: Production use, advanced features

## Deployment Options

### Quick Start (No Installation)
```bash
# Option 1: Landing page
cd frontend && open index.html

# Option 2: HTML Dashboard directly
cd frontend/web && open index.html

# Option 3: Simple HTTP server
cd frontend && python3 -m http.server 8080
# Visit http://localhost:8080
```

### Docker Deployment (Recommended)
```bash
# Start all services including backend
docker-compose up

# Or start specific dashboards
docker-compose up dashboard-html    # Port 8080
docker-compose up dashboard-react   # Port 3000
docker-compose up api               # Port 8000 (backend)
```

**Services:**
- `dashboard-html`: HTML dashboard on port 8080
- `dashboard-react`: React dashboard on port 3000
- `api`: Backend API on port 8000
- `postgres`: Database on port 5432
- `mosquitto`: MQTT broker on ports 1883, 9001
- `influxdb`: Time-series DB on port 8086
- `grafana`: Advanced dashboards on port 3001
- `redis`: Cache on port 6379

### Local Development

#### React App
```bash
cd frontend
./setup-web.sh    # Automated setup
# OR manually:
npm install
cp .env.example .env
npm start         # Runs on port 3000
```

#### HTML Dashboard
```bash
cd frontend/web
python3 -m http.server 8080
# OR
npx http-server . -p 8080
```

## Configuration

### Environment Variables

#### React App (`.env`)
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_DEVICE_ID=ESP32-001
```

#### Backend API (`.env`)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/agronomia
MQTT_BROKER=localhost
MQTT_PORT=1883
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### HTML Dashboard
Edit `frontend/web/index.html` around line 500:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
const DEMO_MODE = true; // Set to false when backend is ready
```

## Network Architecture

### Docker Network
```
┌─────────────────────────────────────────┐
│         Docker Network Bridge           │
│                                         │
│  ┌──────────┐      ┌──────────┐       │
│  │   HTML   │      │  React   │       │
│  │Dashboard │      │Dashboard │       │
│  │  :8080   │      │  :3000   │       │
│  └────┬─────┘      └────┬─────┘       │
│       │                 │              │
│       └────────┬────────┘              │
│                │                       │
│          ┌─────▼─────┐                │
│          │    API    │                │
│          │   :8000   │                │
│          └─────┬─────┘                │
│                │                       │
│       ┌────────┼────────┐             │
│       │        │        │             │
│  ┌────▼───┐ ┌─▼──┐ ┌───▼────┐       │
│  │Postgres│ │MQTT│ │InfluxDB│       │
│  │  :5432 │ │1883│ │  :8086 │       │
│  └────────┘ └────┘ └────────┘       │
└─────────────────────────────────────────┘
```

### External Access
- Landing Page: http://localhost:8080 (or file://)
- HTML Dashboard: http://localhost:8080
- React Dashboard: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001

## API Integration

Both dashboards connect to the same backend API:

### Key Endpoints
- `GET /api/sensors/latest` - Latest sensor readings
- `GET /api/sensors/history/{device_id}` - Historical data
- `POST /api/actuators/control` - Control actuators
- `GET /api/alerts` - Active alerts
- `WS /ws` - WebSocket for real-time updates

See `docs/API.md` for complete documentation.

## Features Comparison

| Feature | HTML Dashboard | React Dashboard |
|---------|----------------|-----------------|
| Installation | ❌ None | ✅ npm install |
| Load Time | ⚡ Instant | 🔄 ~3 seconds |
| Real-time Data | ✅ Yes | ✅ Yes |
| Charts | ✅ Chart.js | ✅ Recharts |
| Sensor Cards | ✅ 6 sensors | ✅ 6 sensors |
| Actuator Control | ❌ View only | ✅ Full control |
| Alerts | ⚠️ Basic | ✅ Advanced |
| Mobile | ✅ Responsive | ✅ Responsive |
| Offline Mode | ✅ Demo data | ❌ Needs API |
| Customization | 🔧 Edit HTML | 🔧 React components |
| Production Ready | ✅ Yes | ✅ Yes |

## Security Considerations

### Development
- CORS is configured for localhost
- No authentication (to be added)
- Demo mode available

### Production
- Enable HTTPS
- Configure proper CORS origins
- Implement JWT authentication
- Use strong passwords
- Update all default credentials
- Enable firewall rules
- Regular security updates

### Docker Security
- Non-root containers
- Health checks enabled
- Network isolation
- Volume permissions
- Secret management via environment variables

## Monitoring

### Health Checks
```bash
# Backend API
curl http://localhost:8000/

# HTML Dashboard
curl http://localhost:8080/

# React Dashboard
curl http://localhost:3000/
```

### Logs
```bash
# Docker logs
docker-compose logs -f dashboard-react
docker-compose logs -f dashboard-html
docker-compose logs -f api

# Container status
docker-compose ps
```

## Troubleshooting

### Dashboard shows no data
1. Check backend is running: `curl http://localhost:8000/`
2. Check browser console (F12) for errors
3. Enable demo mode in dashboard
4. Verify API URL in configuration

### React app won't start
1. Check Node.js version: `node --version` (need ≥16)
2. Clean install: `rm -rf node_modules && npm install`
3. Check port 3000 is available: `lsof -i :3000`
4. Review `.env` file configuration

### Docker containers fail
1. Check Docker is running: `docker ps`
2. View logs: `docker-compose logs`
3. Rebuild images: `docker-compose build --no-cache`
4. Check port conflicts: `docker-compose ps`

### Backend connection error
1. Verify backend URL in configuration
2. Check CORS settings in backend
3. Verify firewall rules
4. Check network connectivity

## Maintenance

### Updates
```bash
# Update dependencies
cd frontend && npm update

# Rebuild Docker images
docker-compose build

# Pull latest images
docker-compose pull
```

### Backups
- Database: PostgreSQL backups via `pg_dump`
- Time-series: InfluxDB backups via `influx backup`
- Configuration: Backup `.env` files and `docker-compose.yml`

## Resources

- **Documentation**: `README.md`, `QUICKSTART_WEB.md`, `docs/API.md`
- **Setup Script**: `frontend/setup-web.sh`
- **Landing Page**: `frontend/index.html`
- **Docker Compose**: `docker-compose.yml`
- **API Docs**: http://localhost:8000/docs (when running)

## Support

For issues and questions:
- Check documentation in `docs/` folder
- Review `CONTRIBUTING.md` for contribution guidelines
- Open an issue on GitHub
- Check existing issues for solutions

## Next Steps

1. ✅ Start with landing page to explore options
2. ✅ Try HTML dashboard for quick demo
3. ✅ Set up React dashboard for full features
4. 🔄 Connect real hardware (ESP32 + sensors)
5. 🔄 Train AI models with real data
6. 🔄 Deploy to production server
7. 🔄 Implement authentication
8. 🔄 Add mobile app

---

**Built with ❤️ for sustainable agriculture**

Agronomia v1.0.0 | MIT License | 2024
