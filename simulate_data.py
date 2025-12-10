#!/usr/bin/env python3
"""
Simulate real-time sensor data for Agronomia
This allows testing the system without physical hardware

Dependencies:
    pip install paho-mqtt requests  # For MQTT and HTTP modes

Usage:
    python simulate_data.py              # MQTT simulation
    python simulate_data.py --mode http  # HTTP API simulation
    python simulate_data.py --help       # Show all options
"""

import json
import time
import random
import argparse
from datetime import datetime
import sys

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import paho.mqtt.client as mqtt
    HAS_MQTT = True
except ImportError:
    HAS_MQTT = False


class SensorSimulator:
    """Simulates realistic hydroponic sensor readings"""
    
    # Configuration constants
    PH_MIN = 5.5
    PH_MAX = 7.0
    EC_MIN = 1500
    EC_MAX = 2500
    TEMP_MIN = 15
    TEMP_MAX = 35
    
    def __init__(self, device_id="SIM-ESP32-001", plant_type="tomato"):
        self.device_id = device_id
        self.plant_type = plant_type
        self.time_offset = 0
        self.start_time = time.time()  # Track device start for uptime
        
        # Base values
        self.ph_base = 6.0
        self.ec_base = 2000
        self.temp_base = 22
        self.humidity_base = 65
        
    def get_sensor_data(self):
        """Generate realistic sensor readings"""
        now = datetime.now()
        hour = now.hour
        
        # Simulate day/night cycle
        is_day = 6 <= hour <= 20
        
        # Light follows day/night cycle
        if is_day:
            lux = random.gauss(25000, 3000)
            par = int(lux * 0.0185)
        else:
            lux = random.gauss(0, 50)
            par = 0
        
        # Temperature varies with light
        if is_day:
            air_temp = self.temp_base + 2 + (hour - 13) * 0.4 + random.gauss(0, 1)
            water_temp = self.temp_base + (hour - 13) * 0.2 + random.gauss(0, 0.5)
        else:
            air_temp = self.temp_base - 2 + random.gauss(0, 0.8)
            water_temp = self.temp_base + random.gauss(0, 0.4)
        
        # Humidity inversely related to temperature
        humidity = self.humidity_base - (air_temp - self.temp_base) * 1.5 + random.gauss(0, 3)
        
        # pH slowly drifts
        ph_drift = random.gauss(0, 0.05)
        self.ph_base = max(self.PH_MIN, min(self.PH_MAX, self.ph_base + ph_drift))
        
        # EC slowly decreases (nutrient consumption)
        ec_drift = random.gauss(-2, 10)
        self.ec_base = max(self.EC_MIN, min(self.EC_MAX, self.ec_base + ec_drift))
        
        # CO2 levels
        co2 = random.gauss(800 if is_day else 600, 100)
        
        return {
            "timestamp": now.isoformat(),
            "device_id": self.device_id,
            "plant_type": self.plant_type,
            "sensors": {
                "air_temp_c": round(max(self.TEMP_MIN, min(self.TEMP_MAX, air_temp)), 2),
                "water_temp_c": round(max(18, min(28, water_temp)), 2),
                "humidity_percent": round(max(40, min(90, humidity)), 1),
                "ph": round(self.ph_base, 2),
                "ec_us_cm": int(self.ec_base),
                "tds_ppm": int(self.ec_base * 0.5),
                "light_lux": int(max(0, lux)),
                "par_umol": max(0, par),
                "co2_ppm": int(max(400, co2)),
                "water_level_cm": round(random.gauss(45, 1), 1),
                "flow_rate_lpm": round(random.gauss(2.5, 0.2), 2)
            },
            "status": {
                "battery_percent": random.randint(85, 100),
                "wifi_rssi": random.randint(-70, -40),
                "uptime_seconds": int(time.time() - self.start_time)
            }
        }


class MQTTSimulator:
    """Publishes simulated data via MQTT"""
    
    def __init__(self, broker="localhost", port=1883, topic_prefix="agronomia"):
        if not HAS_MQTT:
            raise ImportError("paho-mqtt not installed. Install with: pip install paho-mqtt")
        
        self.broker = broker
        self.port = port
        self.topic_prefix = topic_prefix
        self.client = mqtt.Client()
        self.connected = False
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"✓ Connected to MQTT broker at {self.broker}:{self.port}")
        else:
            print(f"✗ Connection failed with code {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        self.connected = False
        print(f"✗ Disconnected from MQTT broker")
    
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            # Wait for connection
            timeout = 5
            while not self.connected and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
            return self.connected
        except Exception as e:
            print(f"✗ Failed to connect to MQTT broker: {e}")
            return False
    
    def publish(self, device_id, data):
        """Publish sensor data to MQTT topic"""
        topic = f"{self.topic_prefix}/devices/{device_id}/data"
        payload = json.dumps(data)
        
        result = self.client.publish(topic, payload, qos=1)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            return True
        else:
            print(f"✗ Failed to publish to {topic}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()


class HTTPSimulator:
    """Sends simulated data via HTTP API"""
    
    def __init__(self, api_url="http://localhost:8000"):
        if not HAS_REQUESTS:
            raise ImportError("requests not installed. Install with: pip install requests")
        
        self.api_url = api_url.rstrip('/')
        self.endpoint = f"{self.api_url}/api/sensor-data"
    
    def publish(self, device_id, data):
        """Send sensor data to HTTP API"""
        try:
            response = requests.post(
                self.endpoint,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code in (200, 201):
                return True
            else:
                print(f"✗ API returned status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ HTTP request failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Simulate sensor data for Agronomia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python simulate_data.py                        # MQTT mode (default)
  python simulate_data.py --mode http            # HTTP API mode
  python simulate_data.py --interval 5           # Publish every 5 seconds
  python simulate_data.py --broker 192.168.1.10  # Custom MQTT broker
  python simulate_data.py --device ESP32-GROW-01 # Custom device ID
        """
    )
    
    parser.add_argument('--mode', choices=['mqtt', 'http'], default='mqtt',
                        help='Simulation mode (default: mqtt)')
    parser.add_argument('--interval', type=int, default=10,
                        help='Publish interval in seconds (default: 10)')
    parser.add_argument('--device', default='SIM-ESP32-001',
                        help='Device ID (default: SIM-ESP32-001)')
    parser.add_argument('--plant', default='tomato',
                        help='Plant type (default: tomato)')
    parser.add_argument('--broker', default='localhost',
                        help='MQTT broker address (default: localhost)')
    parser.add_argument('--port', type=int, default=1883,
                        help='MQTT broker port (default: 1883)')
    parser.add_argument('--api-url', default='http://localhost:8000',
                        help='HTTP API URL (default: http://localhost:8000)')
    parser.add_argument('--count', type=int, default=0,
                        help='Number of messages to send (0 = infinite)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("AGRONOMIA SENSOR SIMULATOR")
    print("=" * 70)
    print(f"\nMode: {args.mode.upper()}")
    print(f"Device ID: {args.device}")
    print(f"Plant Type: {args.plant}")
    print(f"Interval: {args.interval}s")
    
    # Initialize simulator
    sensor_sim = SensorSimulator(device_id=args.device, plant_type=args.plant)
    
    # Initialize publisher
    publisher = None
    if args.mode == 'mqtt':
        print(f"MQTT Broker: {args.broker}:{args.port}")
        publisher = MQTTSimulator(broker=args.broker, port=args.port)
        if not publisher.connect():
            print("\n✗ Failed to connect to MQTT broker")
            print("  Make sure the MQTT broker is running:")
            print("    docker run -p 1883:1883 eclipse-mosquitto")
            sys.exit(1)
    else:
        print(f"API URL: {args.api_url}")
        publisher = HTTPSimulator(api_url=args.api_url)
    
    print("\n" + "=" * 70)
    print("Simulation running... Press Ctrl+C to stop")
    print("=" * 70 + "\n")
    
    # Simulation loop
    count = 0
    try:
        while True:
            # Generate sensor data
            data = sensor_sim.get_sensor_data()
            
            # Publish
            success = publisher.publish(args.device, data)
            
            # Print status
            count += 1
            status = "✓" if success else "✗"
            timestamp = datetime.now().strftime("%H:%M:%S")
            temp = data['sensors']['air_temp_c']
            humidity = data['sensors']['humidity_percent']
            ph = data['sensors']['ph']
            ec = data['sensors']['ec_us_cm']
            
            print(f"[{timestamp}] {status} #{count:04d} | "
                  f"Temp: {temp}°C | Humidity: {humidity}% | "
                  f"pH: {ph} | EC: {ec} μS/cm")
            
            # Check if we've sent enough messages
            if args.count > 0 and count >= args.count:
                break
            
            # Wait for next interval
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print(f"Simulation stopped. Sent {count} messages.")
        print("=" * 70)
    
    finally:
        # Cleanup
        if args.mode == 'mqtt' and publisher:
            publisher.disconnect()


if __name__ == "__main__":
    main()
