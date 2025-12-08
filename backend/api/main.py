"""
Agronomia Backend API
FastAPI-based REST API for hydroponic monitoring platform
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
import json
from collections import defaultdict

# Database imports (using SQLAlchemy)
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# MQTT client for receiving sensor data
import paho.mqtt.client as mqtt

# Initialize FastAPI app
app = FastAPI(
    title="Agronomia API",
    description="Autonomous Hydroponic Monitoring and Control API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite:///./agronomia.db"  # Use PostgreSQL in production
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ph = Column(Float)
    water_temp = Column(Float)
    air_temp = Column(Float)
    humidity = Column(Float)
    ec = Column(Float)
    tds = Column(Float)
    lux = Column(Integer)
    full_spectrum = Column(Integer)
    infrared = Column(Integer)
    visible = Column(Integer)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    alert_type = Column(String)
    severity = Column(String)  # info, warning, critical
    message = Column(String)
    value = Column(Float)
    threshold = Column(Float)
    acknowledged = Column(Boolean, default=False)

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    name = Column(String)
    location = Column(String)
    plant_type = Column(String)
    growth_stage = Column(String)
    last_seen = Column(DateTime)
    status = Column(String)  # online, offline, warning, critical

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for API
class SensorData(BaseModel):
    device_id: str
    timestamp: datetime
    ph: float = Field(..., ge=0, le=14)
    water_temp: float
    air_temp: float
    humidity: float = Field(..., ge=0, le=100)
    ec: float
    tds: float
    lux: int
    full_spectrum: Optional[int] = None
    infrared: Optional[int] = None
    visible: Optional[int] = None

class AlertCreate(BaseModel):
    device_id: str
    alert_type: str
    severity: str
    message: str
    value: float
    threshold: float

class DeviceInfo(BaseModel):
    device_id: str
    name: str
    location: Optional[str] = None
    plant_type: Optional[str] = None
    growth_stage: Optional[str] = None

class ThresholdConfig(BaseModel):
    ph_min: float = 5.5
    ph_max: float = 6.5
    temp_min: float = 18.0
    temp_max: float = 26.0
    humidity_min: float = 60.0
    humidity_max: float = 70.0
    ec_min: float = 1000
    ec_max: float = 2500

# In-memory storage for real-time data
latest_readings: Dict[str, Dict] = {}
websocket_connections: List[WebSocket] = []
threshold_configs: Dict[str, ThresholdConfig] = defaultdict(ThresholdConfig)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "agronomia/devices/+/data"

mqtt_client = mqtt.Client()

def on_mqtt_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_mqtt_message(client, userdata, msg):
    """Handle incoming MQTT messages from sensors"""
    try:
        payload = json.loads(msg.payload.decode())
        device_id = payload.get("device_id")
        
        # Store latest reading
        latest_readings[device_id] = payload
        
        # Save to database
        asyncio.create_task(save_sensor_reading(payload))
        
        # Check thresholds and create alerts
        asyncio.create_task(check_thresholds(device_id, payload))
        
        # Broadcast to WebSocket clients
        asyncio.create_task(broadcast_to_websockets(payload))
        
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message

@app.on_event("startup")
async def startup_event():
    """Initialize MQTT connection on startup"""
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print("MQTT client started")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

# API Endpoints

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Agronomia API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "sensors": "/api/sensors",
            "devices": "/api/devices",
            "alerts": "/api/alerts",
            "analytics": "/api/analytics"
        }
    }

@app.get("/api/sensors/latest")
async def get_latest_readings():
    """Get latest sensor readings for all devices"""
    return latest_readings

@app.get("/api/sensors/latest/{device_id}")
async def get_latest_reading(device_id: str):
    """Get latest sensor reading for a specific device"""
    if device_id not in latest_readings:
        raise HTTPException(status_code=404, detail="Device not found")
    return latest_readings[device_id]

@app.get("/api/sensors/history/{device_id}")
async def get_sensor_history(
    device_id: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get historical sensor data for a device"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    readings = db.query(SensorReading).filter(
        SensorReading.device_id == device_id,
        SensorReading.timestamp >= start_time
    ).order_by(SensorReading.timestamp.desc()).all()
    
    return [{
        "timestamp": r.timestamp.isoformat(),
        "ph": r.ph,
        "water_temp": r.water_temp,
        "air_temp": r.air_temp,
        "humidity": r.humidity,
        "ec": r.ec,
        "tds": r.tds,
        "lux": r.lux
    } for r in readings]

@app.post("/api/sensors/data")
async def post_sensor_data(data: SensorData, db: Session = Depends(get_db)):
    """Manually post sensor data (for testing)"""
    reading = SensorReading(**data.dict())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    
    # Update latest readings
    latest_readings[data.device_id] = data.dict()
    
    return {"status": "success", "id": reading.id}

@app.get("/api/devices")
async def get_devices(db: Session = Depends(get_db)):
    """Get all registered devices"""
    devices = db.query(Device).all()
    return devices

@app.post("/api/devices")
async def register_device(device: DeviceInfo, db: Session = Depends(get_db)):
    """Register a new device"""
    db_device = Device(**device.dict(), status="offline")
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/api/devices/{device_id}")
async def get_device(device_id: str, db: Session = Depends(get_db)):
    """Get device information"""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.put("/api/devices/{device_id}")
async def update_device(device_id: str, device: DeviceInfo, db: Session = Depends(get_db)):
    """Update device information"""
    db_device = db.query(Device).filter(Device.device_id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    for key, value in device.dict(exclude_unset=True).items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device

@app.get("/api/alerts")
async def get_alerts(
    device_id: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get alerts with optional filtering"""
    query = db.query(Alert)
    
    if device_id:
        query = query.filter(Alert.device_id == device_id)
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    
    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()
    return alerts

@app.post("/api/alerts")
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert"""
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@app.put("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.acknowledged = True
    db.commit()
    return {"status": "acknowledged"}

@app.get("/api/analytics/summary/{device_id}")
async def get_analytics_summary(
    device_id: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get analytics summary for a device"""
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    readings = db.query(SensorReading).filter(
        SensorReading.device_id == device_id,
        SensorReading.timestamp >= start_time
    ).all()
    
    if not readings:
        raise HTTPException(status_code=404, detail="No data available")
    
    # Calculate statistics
    ph_values = [r.ph for r in readings if r.ph is not None]
    temp_values = [r.water_temp for r in readings if r.water_temp is not None]
    humidity_values = [r.humidity for r in readings if r.humidity is not None]
    
    return {
        "device_id": device_id,
        "period_hours": hours,
        "total_readings": len(readings),
        "ph": {
            "avg": sum(ph_values) / len(ph_values) if ph_values else None,
            "min": min(ph_values) if ph_values else None,
            "max": max(ph_values) if ph_values else None
        },
        "temperature": {
            "avg": sum(temp_values) / len(temp_values) if temp_values else None,
            "min": min(temp_values) if temp_values else None,
            "max": max(temp_values) if temp_values else None
        },
        "humidity": {
            "avg": sum(humidity_values) / len(humidity_values) if humidity_values else None,
            "min": min(humidity_values) if humidity_values else None,
            "max": max(humidity_values) if humidity_values else None
        }
    }

@app.get("/api/thresholds/{device_id}")
async def get_thresholds(device_id: str):
    """Get alert thresholds for a device"""
    return threshold_configs[device_id]

@app.put("/api/thresholds/{device_id}")
async def update_thresholds(device_id: str, config: ThresholdConfig):
    """Update alert thresholds for a device"""
    threshold_configs[device_id] = config
    return {"status": "updated", "config": config}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        # Send current data on connection
        await websocket.send_json(latest_readings)
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)

# Helper functions

async def save_sensor_reading(data: dict):
    """Save sensor reading to database"""
    db = SessionLocal()
    try:
        sensors = data.get("sensors", {})
        reading = SensorReading(
            device_id=data.get("device_id"),
            timestamp=datetime.fromtimestamp(data.get("timestamp", 0) / 1000),
            ph=sensors.get("ph"),
            water_temp=sensors.get("water_temp"),
            air_temp=sensors.get("air_temp"),
            humidity=sensors.get("humidity"),
            ec=sensors.get("ec"),
            tds=sensors.get("tds"),
            lux=sensors.get("lux"),
            full_spectrum=sensors.get("full_spectrum"),
            infrared=sensors.get("infrared"),
            visible=sensors.get("visible")
        )
        db.add(reading)
        db.commit()
    except Exception as e:
        print(f"Error saving sensor reading: {e}")
    finally:
        db.close()

async def check_thresholds(device_id: str, data: dict):
    """Check sensor values against thresholds and create alerts"""
    db = SessionLocal()
    try:
        sensors = data.get("sensors", {})
        config = threshold_configs[device_id]
        
        # Check pH
        if sensors.get("ph"):
            ph = sensors["ph"]
            if ph < config.ph_min or ph > config.ph_max:
                alert = Alert(
                    device_id=device_id,
                    alert_type="pH",
                    severity="warning" if abs(ph - (config.ph_min + config.ph_max) / 2) < 0.5 else "critical",
                    message=f"pH out of range: {ph:.2f}",
                    value=ph,
                    threshold=config.ph_min if ph < config.ph_min else config.ph_max
                )
                db.add(alert)
        
        # Check temperature
        if sensors.get("water_temp"):
            temp = sensors["water_temp"]
            if temp < config.temp_min or temp > config.temp_max:
                alert = Alert(
                    device_id=device_id,
                    alert_type="temperature",
                    severity="warning",
                    message=f"Temperature out of range: {temp:.1f}°C",
                    value=temp,
                    threshold=config.temp_min if temp < config.temp_min else config.temp_max
                )
                db.add(alert)
        
        # Check humidity
        if sensors.get("humidity"):
            humidity = sensors["humidity"]
            if humidity < config.humidity_min or humidity > config.humidity_max:
                alert = Alert(
                    device_id=device_id,
                    alert_type="humidity",
                    severity="info",
                    message=f"Humidity out of range: {humidity:.1f}%",
                    value=humidity,
                    threshold=config.humidity_min if humidity < config.humidity_min else config.humidity_max
                )
                db.add(alert)
        
        db.commit()
    except Exception as e:
        print(f"Error checking thresholds: {e}")
    finally:
        db.close()

async def broadcast_to_websockets(data: dict):
    """Broadcast sensor data to all connected WebSocket clients"""
    if websocket_connections:
        disconnected = []
        for websocket in websocket_connections:
            try:
                await websocket.send_json(data)
            except:
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for ws in disconnected:
            websocket_connections.remove(ws)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
