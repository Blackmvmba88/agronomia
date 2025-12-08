# Agronomia Backend API

FastAPI-based REST API for the Agronomia hydroponic monitoring platform.

## Features

- RESTful API for sensor data management
- Real-time WebSocket connections
- MQTT integration for IoT devices
- Time-series data storage
- Alert system with configurable thresholds
- Device management
- Analytics and reporting

## Requirements

- Python 3.8+
- PostgreSQL or SQLite
- MQTT Broker (Mosquitto)

## Installation

### Local Development

```bash
cd backend/api
pip install -r requirements.txt
python main.py
```

### Docker

```bash
cd ../..
docker-compose up -d api
```

## Configuration

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/agronomia
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_USER=agronomia
MQTT_PASSWORD=secure_password
SECRET_KEY=your_secret_key_here
```

## API Endpoints

### Sensors

- `GET /api/sensors/latest` - Get latest readings for all devices
- `GET /api/sensors/latest/{device_id}` - Get latest reading for device
- `GET /api/sensors/history/{device_id}?hours=24` - Get historical data
- `POST /api/sensors/data` - Post sensor data manually

### Devices

- `GET /api/devices` - List all devices
- `POST /api/devices` - Register new device
- `GET /api/devices/{device_id}` - Get device info
- `PUT /api/devices/{device_id}` - Update device info

### Alerts

- `GET /api/alerts?device_id=xxx&acknowledged=false` - Get alerts
- `POST /api/alerts` - Create alert
- `PUT /api/alerts/{alert_id}/acknowledge` - Acknowledge alert

### Analytics

- `GET /api/analytics/summary/{device_id}?hours=24` - Get statistics

### Thresholds

- `GET /api/thresholds/{device_id}` - Get alert thresholds
- `PUT /api/thresholds/{device_id}` - Update thresholds

### WebSocket

- `WS /ws` - Real-time sensor data stream

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Schema

See `backend/database/init.sql` for complete schema.

Main tables:
- `devices` - Registered IoT devices
- `sensor_readings` - Time-series sensor data
- `alerts` - System alerts
- `growth_records` - Plant growth tracking
- `harvest_records` - Harvest data

## MQTT Integration

The API subscribes to:
- `agronomia/devices/+/data` - Sensor data from all devices

Data is automatically:
1. Stored in database
2. Checked against thresholds
3. Broadcast to WebSocket clients

## Development

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black main.py
isort main.py
```

### Database Migrations

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Production Deployment

### Using Docker

```bash
docker-compose up -d
```

### Using Systemd

Create `/etc/systemd/system/agronomia-api.service`:

```ini
[Unit]
Description=Agronomia API
After=network.target postgresql.service

[Service]
Type=simple
User=agronomia
WorkingDirectory=/opt/agronomia/backend/api
Environment="PATH=/opt/agronomia/venv/bin"
ExecStart=/opt/agronomia/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.agronomia.local;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
```

## Performance Optimization

- Use PostgreSQL with proper indexes
- Enable Redis caching for frequent queries
- Use connection pooling
- Implement rate limiting
- Monitor with Prometheus/Grafana

## Security

- Use HTTPS in production
- Implement authentication (JWT)
- Validate all inputs
- Use environment variables for secrets
- Regular security updates

## Support

For issues and questions:
- GitHub Issues: https://github.com/Blackmvmba88/agronomia/issues
- Documentation: https://agronomia.readthedocs.io
