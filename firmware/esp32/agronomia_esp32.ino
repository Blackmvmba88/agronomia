/*
 * Agronomia ESP32 Firmware
 * Autonomous Hydroponic Monitoring System
 * 
 * This firmware collects data from multiple sensors and publishes to MQTT broker:
 * - pH sensor (analog)
 * - Temperature sensors (DS18B20, DHT22)
 * - Humidity sensor (DHT22)
 * - EC/TDS sensor (I2C)
 * - Light sensor (TSL2591)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <DHT.h>
#include <Adafruit_TSL2591.h>
#include <ArduinoJson.h>
#include <EEPROM.h>
#include "config.h"

// Pin Definitions
#define PH_PIN 34           // Analog pin for pH sensor
#define DHT_PIN 4           // DHT22 data pin
#define DS18B20_PIN 5       // DS18B20 data pin
#define STATUS_LED 2        // Built-in LED
#define DHT_TYPE DHT22      // DHT sensor type

// I2C Addresses
#define EC_SENSOR_ADDR 0x64
#define TSL2591_ADDR 0x29

// Timing
#define SENSOR_INTERVAL 5000    // Read sensors every 5 seconds
#define PUBLISH_INTERVAL 10000  // Publish data every 10 seconds
#define WIFI_RETRY_DELAY 5000   // Retry WiFi connection every 5 seconds

// Sensor objects
OneWire oneWire(DS18B20_PIN);
DallasTemperature waterTempSensor(&oneWire);
DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591);

// WiFi and MQTT
WiFiClient espClient;
PubSubClient mqtt(espClient);

// Sensor data structure
struct SensorData {
  float ph;
  float waterTemp;
  float airTemp;
  float humidity;
  float ec;
  float tds;
  uint32_t lux;
  uint16_t fullSpectrum;
  uint16_t infrared;
  uint16_t visible;
  unsigned long timestamp;
} sensorData;

// Calibration data (stored in EEPROM)
struct CalibrationData {
  float phOffset;
  float phSlope;
  float ecCalibration;
  bool isCalibrated;
} calibration;

unsigned long lastSensorRead = 0;
unsigned long lastPublish = 0;
bool wifiConnected = false;
bool mqttConnected = false;

void setup() {
  Serial.begin(115200);
  Serial.println("Agronomia ESP32 Firmware v1.0");
  
  // Initialize pins
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(STATUS_LED, LOW);
  
  // Initialize EEPROM
  EEPROM.begin(512);
  loadCalibration();
  
  // Initialize I2C
  Wire.begin(21, 22); // SDA, SCL
  
  // Initialize sensors
  initSensors();
  
  // Connect to WiFi
  connectWiFi();
  
  // Configure MQTT
  mqtt.setServer(MQTT_SERVER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  mqtt.setBufferSize(1024);
  
  Serial.println("Setup complete!");
  blinkLED(3, 200);
}

void loop() {
  // Maintain WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
    connectWiFi();
  } else {
    wifiConnected = true;
  }
  
  // Maintain MQTT connection
  if (wifiConnected && !mqtt.connected()) {
    mqttConnected = false;
    reconnectMQTT();
  } else if (wifiConnected) {
    mqttConnected = true;
    mqtt.loop();
  }
  
  // Read sensors at defined interval
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = currentMillis;
    readAllSensors();
    printSensorData();
  }
  
  // Publish data at defined interval
  if (mqttConnected && (currentMillis - lastPublish >= PUBLISH_INTERVAL)) {
    lastPublish = currentMillis;
    publishSensorData();
    blinkLED(1, 50);
  }
  
  delay(100);
}

void initSensors() {
  Serial.println("Initializing sensors...");
  
  // Initialize water temperature sensor
  waterTempSensor.begin();
  Serial.print("DS18B20 devices: ");
  Serial.println(waterTempSensor.getDeviceCount());
  
  // Initialize DHT22
  dht.begin();
  Serial.println("DHT22 initialized");
  
  // Initialize light sensor
  if (tsl.begin()) {
    Serial.println("TSL2591 found");
    tsl.setGain(TSL2591_GAIN_MED);
    tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
  } else {
    Serial.println("TSL2591 not found!");
  }
  
  // Scan I2C bus
  Serial.println("Scanning I2C bus...");
  scanI2C();
}

void readAllSensors() {
  sensorData.timestamp = millis();
  
  // Read pH sensor
  sensorData.ph = readPH();
  
  // Read water temperature
  sensorData.waterTemp = readWaterTemperature();
  
  // Read air temperature and humidity
  sensorData.airTemp = dht.readTemperature();
  sensorData.humidity = dht.readHumidity();
  
  // Read EC/TDS
  readEC();
  
  // Read light sensor
  readLightSensor();
}

float readPH() {
  // Read analog value from pH sensor
  int rawValue = 0;
  for (int i = 0; i < 10; i++) {
    rawValue += analogRead(PH_PIN);
    delay(10);
  }
  rawValue /= 10;
  
  // Convert to voltage (ESP32 ADC: 0-4095 = 0-3.3V)
  float voltage = rawValue * (3.3 / 4095.0);
  
  // Apply calibration (typical: pH = 7 at 2.5V, slope -0.18V/pH)
  float ph = 7.0 - ((voltage - 2.5) / 0.18);
  
  // Apply stored calibration
  if (calibration.isCalibrated) {
    ph = (ph - calibration.phOffset) * calibration.phSlope;
  }
  
  // Clamp to valid range
  if (ph < 0) ph = 0;
  if (ph > 14) ph = 14;
  
  return ph;
}

float readWaterTemperature() {
  waterTempSensor.requestTemperatures();
  float temp = waterTempSensor.getTempCByIndex(0);
  
  // Check for sensor error
  if (temp == DEVICE_DISCONNECTED_C || temp < -50 || temp > 100) {
    Serial.println("Error reading water temperature!");
    return -127.0;
  }
  
  return temp;
}

void readEC() {
  // Request EC reading from I2C sensor
  Wire.beginTransmission(EC_SENSOR_ADDR);
  Wire.write('R'); // Read command
  Wire.endTransmission();
  
  delay(600); // Wait for reading
  
  Wire.requestFrom(EC_SENSOR_ADDR, 32);
  byte code = Wire.read();
  
  if (code == 1) { // Success
    char ecString[32];
    int i = 0;
    while (Wire.available()) {
      char c = Wire.read();
      if (c != 0) {
        ecString[i++] = c;
      }
    }
    ecString[i] = '\0';
    
    sensorData.ec = atof(ecString);
    sensorData.tds = sensorData.ec * 0.5; // Approximate TDS conversion
    
    // Apply calibration
    if (calibration.isCalibrated) {
      sensorData.ec *= calibration.ecCalibration;
      sensorData.tds = sensorData.ec * 0.5;
    }
  } else {
    Serial.println("Error reading EC sensor");
    sensorData.ec = 0;
    sensorData.tds = 0;
  }
}

void readLightSensor() {
  uint32_t lum = tsl.getFullLuminosity();
  sensorData.infrared = lum >> 16;
  sensorData.fullSpectrum = lum & 0xFFFF;
  sensorData.visible = sensorData.fullSpectrum - sensorData.infrared;
  sensorData.lux = tsl.calculateLux(sensorData.fullSpectrum, sensorData.infrared);
}

void publishSensorData() {
  // Create JSON document
  StaticJsonDocument<512> doc;
  
  doc["device_id"] = DEVICE_ID;
  doc["timestamp"] = sensorData.timestamp;
  
  JsonObject sensors = doc.createNestedObject("sensors");
  sensors["ph"] = round(sensorData.ph * 100) / 100.0;
  sensors["water_temp"] = round(sensorData.waterTemp * 10) / 10.0;
  sensors["air_temp"] = round(sensorData.airTemp * 10) / 10.0;
  sensors["humidity"] = round(sensorData.humidity * 10) / 10.0;
  sensors["ec"] = round(sensorData.ec);
  sensors["tds"] = round(sensorData.tds);
  sensors["lux"] = sensorData.lux;
  sensors["full_spectrum"] = sensorData.fullSpectrum;
  sensors["infrared"] = sensorData.infrared;
  sensors["visible"] = sensorData.visible;
  
  JsonObject status = doc.createNestedObject("status");
  status["wifi_rssi"] = WiFi.RSSI();
  status["uptime"] = millis() / 1000;
  
  // Serialize to string
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer);
  
  // Publish to MQTT
  char topic[64];
  snprintf(topic, sizeof(topic), "%s/%s/data", MQTT_TOPIC_BASE, DEVICE_ID);
  
  if (mqtt.publish(topic, jsonBuffer, false)) {
    Serial.println("Data published successfully");
  } else {
    Serial.println("Failed to publish data");
  }
}

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Signal strength: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
    digitalWrite(STATUS_LED, HIGH);
  } else {
    Serial.println("\nWiFi connection failed!");
    digitalWrite(STATUS_LED, LOW);
  }
}

void reconnectMQTT() {
  if (!mqtt.connected()) {
    Serial.print("Connecting to MQTT broker...");
    
    String clientId = "agronomia-" + String(DEVICE_ID);
    
    if (mqtt.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      Serial.println("connected!");
      
      // Subscribe to control topics
      char topic[64];
      snprintf(topic, sizeof(topic), "%s/%s/control/#", MQTT_TOPIC_BASE, DEVICE_ID);
      mqtt.subscribe(topic);
      
      // Publish online status
      snprintf(topic, sizeof(topic), "%s/%s/status", MQTT_TOPIC_BASE, DEVICE_ID);
      mqtt.publish(topic, "online", true);
      
    } else {
      Serial.print("failed, rc=");
      Serial.println(mqtt.state());
    }
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("]: ");
  
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  Serial.println(message);
  
  // Parse JSON command
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, message);
  
  if (!error) {
    const char* command = doc["command"];
    
    if (strcmp(command, "calibrate_ph") == 0) {
      float refValue = doc["value"];
      calibratePH(refValue);
    } else if (strcmp(command, "calibrate_ec") == 0) {
      float refValue = doc["value"];
      calibrateEC(refValue);
    } else if (strcmp(command, "restart") == 0) {
      ESP.restart();
    }
  }
}

void calibratePH(float referenceValue) {
  Serial.print("Calibrating pH to reference: ");
  Serial.println(referenceValue);
  
  float currentReading = readPH();
  calibration.phOffset = currentReading - referenceValue;
  calibration.isCalibrated = true;
  
  saveCalibration();
  Serial.println("pH calibration complete!");
}

void calibrateEC(float referenceValue) {
  Serial.print("Calibrating EC to reference: ");
  Serial.println(referenceValue);
  
  readEC();
  if (sensorData.ec > 0) {
    calibration.ecCalibration = referenceValue / sensorData.ec;
    calibration.isCalibrated = true;
    saveCalibration();
    Serial.println("EC calibration complete!");
  } else {
    Serial.println("EC calibration failed - no reading");
  }
}

void loadCalibration() {
  EEPROM.get(0, calibration);
  
  // Check if calibration is valid
  if (isnan(calibration.phOffset) || isnan(calibration.phSlope) || 
      isnan(calibration.ecCalibration)) {
    // Initialize with defaults
    calibration.phOffset = 0.0;
    calibration.phSlope = 1.0;
    calibration.ecCalibration = 1.0;
    calibration.isCalibrated = false;
    saveCalibration();
  }
  
  Serial.print("Calibration loaded - Calibrated: ");
  Serial.println(calibration.isCalibrated ? "Yes" : "No");
}

void saveCalibration() {
  EEPROM.put(0, calibration);
  EEPROM.commit();
  Serial.println("Calibration saved to EEPROM");
}

void printSensorData() {
  Serial.println("\n=== Sensor Readings ===");
  Serial.print("pH: "); Serial.println(sensorData.ph, 2);
  Serial.print("Water Temp: "); Serial.print(sensorData.waterTemp, 1); Serial.println(" °C");
  Serial.print("Air Temp: "); Serial.print(sensorData.airTemp, 1); Serial.println(" °C");
  Serial.print("Humidity: "); Serial.print(sensorData.humidity, 1); Serial.println(" %");
  Serial.print("EC: "); Serial.print(sensorData.ec, 0); Serial.println(" μS/cm");
  Serial.print("TDS: "); Serial.print(sensorData.tds, 0); Serial.println(" ppm");
  Serial.print("Light: "); Serial.print(sensorData.lux); Serial.println(" lux");
  Serial.print("WiFi RSSI: "); Serial.print(WiFi.RSSI()); Serial.println(" dBm");
  Serial.println("=======================\n");
}

void scanI2C() {
  byte error, address;
  int nDevices = 0;
  
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("I2C device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  
  if (nDevices == 0) {
    Serial.println("No I2C devices found");
  } else {
    Serial.print("Found ");
    Serial.print(nDevices);
    Serial.println(" I2C device(s)");
  }
}

void blinkLED(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(STATUS_LED, HIGH);
    delay(delayMs);
    digitalWrite(STATUS_LED, LOW);
    delay(delayMs);
  }
}
