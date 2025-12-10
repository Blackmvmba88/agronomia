/**
 * BlackMamba Smart Farming - ESP32 Firmware
 * 
 * Sistema de monitoreo y control para cultivo hidropónico
 * 
 * Sensores:
 * - pH del agua
 * - Conductividad eléctrica (EC)
 * - Temperatura del agua (DS18B20)
 * - Temperatura y humedad ambiente (DHT22)
 * - Luminosidad (LDR o BH1750)
 * 
 * Actuadores:
 * - Bomba de recirculación
 * - Iluminación LED
 * - Bombas dosificadoras (opcional)
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "config/config.h"

// Pines de sensores
#define DHT_PIN 4           // DHT22 - Temperatura y humedad ambiente
#define DHT_TYPE DHT22
#define WATER_TEMP_PIN 5    // DS18B20 - Temperatura del agua
#define PH_PIN 34           // Sensor de pH (analógico)
#define EC_PIN 35           // Sensor de EC (analógico)
#define LIGHT_PIN 32        // Sensor de luz (analógico)

// Pines de actuadores
#define PUMP_PIN 26         // Bomba de recirculación
#define LED_PIN 27          // Iluminación LED
#define PUMP_A_PIN 25       // Bomba dosificadora A
#define PUMP_B_PIN 33       // Bomba dosificadora B

// Inicialización de sensores
DHT dht(DHT_PIN, DHT_TYPE);
OneWire oneWire(WATER_TEMP_PIN);
DallasTemperature waterTempSensor(&oneWire);

// Variables globales
unsigned long lastReadTime = 0;
const unsigned long readInterval = 60000; // Leer cada 60 segundos

// Estructura de datos de sensores
struct SensorData {
  float pH;
  float ec;
  float waterTemp;
  float airTemp;
  float humidity;
  int lightLevel;
  unsigned long timestamp;
};

SensorData currentData;

// Prototipos de funciones
void connectWiFi();
void readSensors();
float readPH();
float readEC();
float readWaterTemperature();
void sendDataToBackend();
void controlActuators();

void setup() {
  Serial.begin(115200);
  Serial.println("BlackMamba Smart Farming - Iniciando...");
  
  // Configurar pines de actuadores
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(PUMP_A_PIN, OUTPUT);
  pinMode(PUMP_B_PIN, OUTPUT);
  
  // Estado inicial de actuadores (apagados)
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  digitalWrite(PUMP_A_PIN, LOW);
  digitalWrite(PUMP_B_PIN, LOW);
  
  // Inicializar sensores
  dht.begin();
  waterTempSensor.begin();
  
  // Conectar a WiFi
  connectWiFi();
  
  Serial.println("Sistema listo!");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Leer sensores en intervalos regulares
  if (currentTime - lastReadTime >= readInterval) {
    lastReadTime = currentTime;
    
    Serial.println("\n--- Lectura de sensores ---");
    readSensors();
    
    // Enviar datos al backend
    sendDataToBackend();
    
    // Control de actuadores basado en condiciones
    controlActuators();
  }
  
  delay(1000);
}

void connectWiFi() {
  Serial.print("Conectando a WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nError al conectar WiFi");
  }
}

void readSensors() {
  // Leer timestamp
  currentData.timestamp = millis();
  
  // Leer pH
  currentData.pH = readPH();
  Serial.print("pH: ");
  Serial.println(currentData.pH);
  
  // Leer EC
  currentData.ec = readEC();
  Serial.print("EC: ");
  Serial.print(currentData.ec);
  Serial.println(" µS/cm");
  
  // Leer temperatura del agua
  currentData.waterTemp = readWaterTemperature();
  Serial.print("Temp Agua: ");
  Serial.print(currentData.waterTemp);
  Serial.println(" °C");
  
  // Leer temperatura y humedad del aire
  currentData.airTemp = dht.readTemperature();
  currentData.humidity = dht.readHumidity();
  Serial.print("Temp Aire: ");
  Serial.print(currentData.airTemp);
  Serial.println(" °C");
  Serial.print("Humedad: ");
  Serial.print(currentData.humidity);
  Serial.println(" %");
  
  // Leer nivel de luz
  currentData.lightLevel = analogRead(LIGHT_PIN);
  Serial.print("Luz: ");
  Serial.println(currentData.lightLevel);
}

float readPH() {
  // Leer voltaje del sensor de pH
  int rawValue = analogRead(PH_PIN);
  float voltage = rawValue * (3.3 / 4095.0);
  
  // Calibración del pH (ajustar según sensor específico)
  // Fórmula típica: pH = 7 + ((2.5 - voltage) / 0.18)
  float pH = 7.0 + ((PH_NEUTRAL_VOLTAGE - voltage) / 0.18);
  
  // Limitar valores entre 0 y 14
  if (pH < 0) pH = 0;
  if (pH > 14) pH = 14;
  
  return pH;
}

float readEC() {
  // Leer voltaje del sensor de EC
  int rawValue = analogRead(EC_PIN);
  float voltage = rawValue * (3.3 / 4095.0);
  
  // Calibración de EC (ajustar según sensor específico)
  // Conversión a µS/cm
  float ec = voltage * EC_CONVERSION_FACTOR;
  
  return ec;
}

float readWaterTemperature() {
  waterTempSensor.requestTemperatures();
  float temp = waterTempSensor.getTempCByIndex(0);
  
  // Validar lectura
  if (temp == DEVICE_DISCONNECTED_C) {
    Serial.println("Error leyendo temperatura del agua");
    return -127.0;
  }
  
  return temp;
}

void sendDataToBackend() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi no conectado, no se pueden enviar datos");
    return;
  }
  
  HTTPClient http;
  
  // Construir URL del endpoint
  String url = String(API_ENDPOINT) + "/api/sensors/data";
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  // Crear JSON con datos
  StaticJsonDocument<512> doc;
  doc["pH"] = currentData.pH;
  doc["ec"] = currentData.ec;
  doc["waterTemp"] = currentData.waterTemp;
  doc["airTemp"] = currentData.airTemp;
  doc["humidity"] = currentData.humidity;
  doc["lightLevel"] = currentData.lightLevel;
  doc["timestamp"] = currentData.timestamp;
  doc["deviceId"] = DEVICE_ID;
  
  String jsonData;
  serializeJson(doc, jsonData);
  
  Serial.println("Enviando datos al backend...");
  Serial.println(jsonData);
  
  // Enviar POST request
  int httpResponseCode = http.POST(jsonData);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("Respuesta del servidor: ");
    Serial.println(response);
  } else {
    Serial.print("Error en la petición: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

void controlActuators() {
  // Control automático basado en condiciones
  
  // Control de bomba de recirculación
  // Encender bomba cada hora por 10 minutos
  unsigned long currentTime = millis();
  unsigned long hourMillis = currentTime % 3600000; // Posición en la hora actual
  
  if (hourMillis < 600000) { // Primeros 10 minutos de cada hora
    digitalWrite(PUMP_PIN, HIGH);
    Serial.println("Bomba de recirculación: ON");
  } else {
    digitalWrite(PUMP_PIN, LOW);
  }
  
  // Control de iluminación LED
  // Encender si el nivel de luz es bajo (< 1000)
  if (currentData.lightLevel < 1000) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("Iluminación LED: ON");
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  // Alertas de condiciones fuera de rango
  if (currentData.pH < PH_MIN || currentData.pH > PH_MAX) {
    Serial.println("ALERTA: pH fuera de rango!");
  }
  
  if (currentData.ec < EC_MIN || currentData.ec > EC_MAX) {
    Serial.println("ALERTA: EC fuera de rango!");
  }
  
  if (currentData.waterTemp < WATER_TEMP_MIN || currentData.waterTemp > WATER_TEMP_MAX) {
    Serial.println("ALERTA: Temperatura del agua fuera de rango!");
  }
}
