# Agronomia Firmware

ESP32-based firmware for autonomous hydroponic monitoring.

## Features

- Multi-sensor support (pH, EC, temperature, humidity, light)
- WiFi connectivity with automatic reconnection
- MQTT publish/subscribe
- Sensor calibration with EEPROM storage
- Over-the-air (OTA) updates support
- Watchdog timer for reliability
- JSON data format

## Hardware Requirements

- ESP32 DevKit (or compatible board)
- Sensors as listed in hardware/docs/SETUP.md
- 5V power supply (min 1A)

## Installation

### Using Arduino IDE

1. Install Arduino IDE 1.8.19 or newer
2. Install ESP32 board support:
   - Go to File → Preferences
   - Add to Additional Board Manager URLs:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Boards Manager
   - Search for "ESP32" and install

3. Install required libraries:
   - PubSubClient (by Nick O'Leary)
   - ArduinoJson (by Benoit Blanchon)
   - DHT sensor library (by Adafruit)
   - OneWire (by Jim Studt)
   - DallasTemperature (by Miles Burton)
   - Adafruit TSL2591 Library

4. Configure:
   - Copy `config.h.example` to `config.h`
   - Edit `config.h` with your WiFi and MQTT settings

5. Upload:
   - Select board: "ESP32 Dev Module"
   - Select port
   - Click Upload

### Using PlatformIO

```bash
cd firmware/esp32
pio init --board esp32dev
pio lib install "PubSubClient" "ArduinoJson" "DHT sensor library" "OneWire" "DallasTemperature" "Adafruit TSL2591 Library"
pio run --target upload
pio device monitor
```

## Configuration

Edit `config.h`:

```cpp
#define DEVICE_ID "ESP32-001"
#define WIFI_SSID "your_wifi_ssid"
#define WIFI_PASSWORD "your_wifi_password"
#define MQTT_SERVER "mqtt.agronomia.local"
#define MQTT_PORT 1883
```

## Calibration

### pH Calibration

1. Place probe in pH 7.0 buffer
2. Send MQTT command:
   ```json
   {
     "command": "calibrate_ph",
     "value": 7.0
   }
   ```

### EC Calibration

1. Place probe in 1413 μS/cm standard solution
2. Send MQTT command:
   ```json
   {
     "command": "calibrate_ec",
     "value": 1413
   }
   ```

## MQTT Topics

### Published Topics

- `agronomia/devices/{DEVICE_ID}/data` - Sensor data (every 10 seconds)
- `agronomia/devices/{DEVICE_ID}/status` - Device status

### Subscribed Topics

- `agronomia/devices/{DEVICE_ID}/control/#` - Control commands

## Data Format

```json
{
  "device_id": "ESP32-001",
  "timestamp": 1234567890,
  "sensors": {
    "ph": 6.2,
    "water_temp": 22.5,
    "air_temp": 24.3,
    "humidity": 65.2,
    "ec": 1520,
    "tds": 760,
    "lux": 25000,
    "full_spectrum": 30000,
    "infrared": 5000,
    "visible": 25000
  },
  "status": {
    "wifi_rssi": -45,
    "uptime": 3600
  }
}
```

## Troubleshooting

### WiFi won't connect
- Check SSID and password in config.h
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Check router settings (some routers block ESP devices)

### MQTT connection fails
- Verify broker address and port
- Check firewall settings
- Test broker with `mosquitto_sub -h <broker> -t '#'`

### Sensor readings show -127 or NaN
- Check sensor wiring
- Verify pull-up resistors for I2C and OneWire
- Run I2C scanner to detect devices

## Serial Commands

Monitor at 115200 baud:
- View real-time sensor data
- Debug messages
- Connection status

## OTA Updates

Coming soon - enable OTA in config.h and update over WiFi.

## Support

For issues:
- Check hardware connections
- Review serial monitor output
- See hardware/docs/SETUP.md
- GitHub Issues: https://github.com/Blackmvmba88/agronomia/issues
