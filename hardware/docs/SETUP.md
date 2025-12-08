# Hardware Setup Guide

## Overview
This guide provides detailed instructions for setting up the Agronomia hardware components for hydroponic plant monitoring.

## Required Components

### Microcontrollers
- **ESP32 DevKit** (Recommended) - WiFi/Bluetooth enabled
- **Arduino Mega 2560** (Alternative) - For larger sensor arrays
- **Raspberry Pi 4** (Optional) - For advanced processing and local AI

### Sensors

#### 1. pH Sensor
- **Model**: Atlas Scientific pH Kit or DFRobot pH Meter
- **Range**: 0-14 pH
- **Accuracy**: ±0.1 pH
- **Interface**: Analog (0-5V) or I2C
- **Calibration**: Required with pH 4.0, 7.0, and 10.0 solutions

#### 2. Humidity Sensor
- **Model**: DHT22 or SHT31
- **Humidity Range**: 0-100% RH
- **Temperature Range**: -40 to 80°C
- **Accuracy**: ±2% RH, ±0.3°C
- **Interface**: Digital (One-Wire or I2C)

#### 3. Nutrient/EC Sensor
- **Model**: Atlas Scientific Conductivity Kit
- **Range**: 0.07 - 500,000+ μS/cm
- **Accuracy**: ±2%
- **Interface**: I2C or UART
- **Purpose**: Measures Total Dissolved Solids (TDS) and nutrient concentration

#### 4. Light Sensor
- **Model**: TSL2591 or BH1750
- **Range**: 0.01 to 88,000 lux
- **Interface**: I2C
- **Purpose**: Measures Photosynthetically Active Radiation (PAR)

#### 5. Temperature Sensor
- **Model**: DS18B20 (Water) + DHT22 (Air)
- **Range**: -55 to 125°C
- **Accuracy**: ±0.5°C
- **Interface**: One-Wire (DS18B20), Digital (DHT22)

### Additional Components
- 5V/3.3V Power Supply (min 2A)
- Breadboard and jumper wires
- Resistors: 4.7kΩ (for One-Wire), 10kΩ (pull-ups)
- Waterproof sensor probes
- Enclosure box (IP65 rated)
- MicroSD card module (for local data logging)

## Wiring Diagrams

### ESP32 Pin Configuration

```
ESP32 DevKit Pinout:
====================

pH Sensor (Analog):
- VCC → 3.3V
- GND → GND
- Signal → GPIO34 (ADC1_CH6)

DHT22 (Humidity/Temp):
- VCC → 3.3V
- GND → GND
- Data → GPIO4 (with 4.7kΩ pull-up to 3.3V)

DS18B20 (Water Temp):
- VCC → 3.3V
- GND → GND
- Data → GPIO5 (with 4.7kΩ pull-up to 3.3V)

I2C Sensors (TSL2591, SHT31, EC Sensor):
- VCC → 3.3V
- GND → GND
- SDA → GPIO21
- SCL → GPIO22

Status LED:
- Anode → GPIO2 (through 220Ω resistor)
- Cathode → GND

WiFi Antenna: Built-in
Power: USB or 5V via VIN pin
```

### Detailed Wiring Steps

#### Step 1: pH Sensor Connection
1. Connect pH sensor VCC to ESP32 3.3V
2. Connect pH sensor GND to ESP32 GND
3. Connect pH sensor analog output to GPIO34
4. Ensure probe is submerged in nutrient solution

#### Step 2: Humidity Sensor (DHT22)
1. Connect DHT22 pin 1 (VCC) to 3.3V
2. Connect DHT22 pin 2 (Data) to GPIO4
3. Add 4.7kΩ resistor between pins 1 and 2
4. Connect DHT22 pin 4 (GND) to GND

#### Step 3: Temperature Sensor (DS18B20)
1. Connect DS18B20 VCC (red) to 3.3V
2. Connect DS18B20 Data (yellow) to GPIO5
3. Add 4.7kΩ resistor between VCC and Data
4. Connect DS18B20 GND (black) to GND
5. Ensure waterproof probe is in nutrient solution

#### Step 4: I2C Sensors
1. All I2C devices share SDA (GPIO21) and SCL (GPIO22)
2. Connect each sensor's VCC to 3.3V
3. Connect each sensor's GND to GND
4. TSL2591: Default I2C address 0x29
5. SHT31: Default I2C address 0x44
6. EC Sensor: Default I2C address 0x64

## Sensor Calibration

### pH Sensor Calibration
```
1. Prepare calibration solutions (pH 4.0, 7.0, 10.0)
2. Rinse probe with distilled water
3. Place in pH 7.0 solution (mid-point calibration)
4. Run calibration command: calibrate_ph(7.0)
5. Rinse and place in pH 4.0 solution
6. Run: calibrate_ph(4.0)
7. Rinse and place in pH 10.0 solution
8. Run: calibrate_ph(10.0)
9. Store calibration values in EEPROM
```

### EC/TDS Sensor Calibration
```
1. Prepare standard solution (1413 μS/cm)
2. Rinse probe with distilled water
3. Submerge in standard solution
4. Run: calibrate_ec(1413)
5. Store calibration in EEPROM
```

### Temperature Compensation
- pH and EC readings are temperature-dependent
- Enable automatic temperature compensation in firmware
- DS18B20 provides reference temperature

## Network Configuration

### MQTT Setup
```cpp
// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MQTT Broker
const char* mqtt_server = "mqtt.agronomia.local";
const int mqtt_port = 1883;
const char* mqtt_user = "agronomia";
const char* mqtt_password = "your_secure_password";

// MQTT Topics
const char* topic_ph = "agronomia/sensors/ph";
const char* topic_temp = "agronomia/sensors/temperature";
const char* topic_humidity = "agronomia/sensors/humidity";
const char* topic_ec = "agronomia/sensors/ec";
const char* topic_light = "agronomia/sensors/light";
```

### WiFi Configuration
1. Edit `firmware/esp32/config.h` with your credentials
2. Set static IP (optional but recommended):
   ```cpp
   IPAddress local_IP(192, 168, 1, 100);
   IPAddress gateway(192, 168, 1, 1);
   IPAddress subnet(255, 255, 255, 0);
   ```

## Power Considerations

### Power Budget
- ESP32: ~160mA (WiFi active), ~80mA (WiFi sleep)
- DHT22: ~2.5mA
- DS18B20: ~1.5mA
- TSL2591: ~0.5mA
- pH Sensor: ~5mA
- EC Sensor: ~10mA
- **Total**: ~180mA peak

### Power Supply Options
1. **USB Power**: 5V/1A USB adapter (easiest for testing)
2. **Battery**: 18650 Li-ion with solar panel (for remote)
3. **Wall Adapter**: 5V/2A regulated power supply (production)

## Enclosure and Mounting

### Waterproofing
- Use IP65-rated enclosure for electronics
- Cable glands for sensor wires
- Silicone sealant around openings
- Mount away from water spray

### Sensor Placement
- **pH Probe**: Submerged in nutrient solution, away from air pump
- **EC Probe**: Submerged, near nutrient injection point
- **Water Temp**: Submerged, away from heater/chiller
- **Air Temp/Humidity**: Above plant canopy, shaded from direct light
- **Light Sensor**: Canopy level, facing upward

## Testing and Verification

### Pre-deployment Checklist
- [ ] All sensors respond on correct I2C addresses
- [ ] pH readings stable in buffer solutions
- [ ] Temperature readings accurate (compare with thermometer)
- [ ] WiFi connection stable
- [ ] MQTT messages publishing successfully
- [ ] Data visible in backend dashboard
- [ ] Alert thresholds configured
- [ ] Calibration values stored in EEPROM

### Debug Commands
```bash
# Test I2C devices
i2cdetect -y 1

# Monitor MQTT messages
mosquitto_sub -h mqtt.agronomia.local -t agronomia/sensors/#

# Check WiFi signal
iwconfig wlan0

# Serial monitor (Arduino IDE)
Tools > Serial Monitor (115200 baud)
```

## Maintenance

### Weekly
- Clean sensor probes with distilled water
- Check for algae buildup on probes
- Verify WiFi connection stability

### Monthly
- Re-calibrate pH sensor
- Check EC sensor calibration
- Clean light sensor lens
- Inspect wiring for corrosion

### Quarterly
- Replace pH probe electrolyte solution
- Deep clean all probes with cleaning solution
- Check power supply voltage stability
- Update firmware if available

## Troubleshooting

### Issue: pH readings unstable
- **Solution**: Calibrate sensor, check for air bubbles, ensure proper immersion

### Issue: WiFi disconnects
- **Solution**: Move router closer, use WiFi repeater, check for interference

### Issue: I2C sensor not detected
- **Solution**: Check wiring, verify pull-up resistors, scan I2C bus

### Issue: Temperature reading -127°C (DS18B20)
- **Solution**: Check pull-up resistor, verify wiring, sensor may be damaged

## Safety

- **Electrical Safety**: Keep electronics away from water
- **Chemical Safety**: Wear gloves when handling calibration solutions
- **Probe Care**: Always store pH probe in storage solution (not distilled water)
- **Ventilation**: Ensure adequate airflow around electronics

## Support

For hardware support:
- GitHub Issues: [agronomia/issues](https://github.com/Blackmvmba88/agronomia/issues)
- Hardware Docs: [hardware/docs/](../)
- Schematics: [hardware/schematics/](../schematics/)

## Next Steps

After hardware setup:
1. Flash firmware: See [firmware/esp32/README.md](../../firmware/esp32/README.md)
2. Configure backend: See [backend/api/README.md](../../backend/api/README.md)
3. Set up dashboard: See [frontend/web/README.md](../../frontend/web/README.md)
