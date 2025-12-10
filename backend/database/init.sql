-- Initialize Agronomia Database Schema

-- Create devices table
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    plant_type VARCHAR(50),
    growth_stage VARCHAR(50),
    last_seen TIMESTAMP,
    status VARCHAR(20) DEFAULT 'offline',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sensor_readings table
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ph FLOAT,
    water_temp FLOAT,
    air_temp FLOAT,
    humidity FLOAT,
    ec FLOAT,
    tds FLOAT,
    lux INTEGER,
    full_spectrum INTEGER,
    infrared INTEGER,
    visible INTEGER,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Create alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT,
    value FLOAT,
    threshold FLOAT,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_at TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Create growth_records table for tracking plant development
CREATE TABLE IF NOT EXISTS growth_records (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    plant_height FLOAT,
    leaf_count INTEGER,
    growth_rate FLOAT,
    notes TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Create harvest_records table
CREATE TABLE IF NOT EXISTS harvest_records (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    harvest_date TIMESTAMP NOT NULL,
    yield_amount FLOAT,
    quality_rating INTEGER CHECK (quality_rating >= 1 AND quality_rating <= 5),
    notes TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_sensor_readings_device_timestamp ON sensor_readings(device_id, timestamp DESC);
CREATE INDEX idx_alerts_device_timestamp ON alerts(device_id, timestamp DESC);
CREATE INDEX idx_alerts_acknowledged ON alerts(acknowledged);
CREATE INDEX idx_growth_records_device_timestamp ON growth_records(device_id, timestamp DESC);

-- Insert sample device
INSERT INTO devices (device_id, name, location, plant_type, growth_stage, status) 
VALUES ('ESP32-001', 'Greenhouse A - Bay 1', 'Greenhouse A', 'tomato', 'vegetative', 'online')
ON CONFLICT (device_id) DO NOTHING;

-- Create view for latest sensor readings
CREATE OR REPLACE VIEW latest_sensor_readings AS
SELECT DISTINCT ON (device_id) *
FROM sensor_readings
ORDER BY device_id, timestamp DESC;

-- Create view for unacknowledged alerts
CREATE OR REPLACE VIEW active_alerts AS
SELECT *
FROM alerts
WHERE acknowledged = FALSE
ORDER BY timestamp DESC;

COMMENT ON TABLE devices IS 'Registered IoT devices and their configurations';
COMMENT ON TABLE sensor_readings IS 'Time-series sensor data from all devices';
COMMENT ON TABLE alerts IS 'System alerts and notifications';
COMMENT ON TABLE growth_records IS 'Manual plant growth measurements';
COMMENT ON TABLE harvest_records IS 'Harvest data for yield analysis';
