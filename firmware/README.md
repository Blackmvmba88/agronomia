# Firmware ESP32 - BlackMamba Smart Farming

Firmware para ESP32 que controla sensores y actuadores del sistema hidropónico.

## 🔌 Hardware Requerido

### Microcontrolador
- ESP32 DevKit v1 o compatible

### Sensores
- **DHT22**: Temperatura y humedad ambiente
- **DS18B20**: Temperatura del agua
- **Sensor de pH**: Analógico (0-14 pH)
- **Sensor de EC**: Conductividad eléctrica
- **LDR o BH1750**: Sensor de luz

### Actuadores
- **Relé para bomba**: Control de bomba de recirculación
- **Relé para LED**: Control de iluminación
- **Relés para bombas dosificadoras** (opcional)

## 📋 Conexiones

### Sensores
```
DHT22:
  - VCC → 3.3V
  - GND → GND
  - DATA → GPIO 4

DS18B20:
  - VCC → 3.3V
  - GND → GND
  - DATA → GPIO 5 (con resistencia pull-up 4.7kΩ)

Sensor pH:
  - VCC → 3.3V
  - GND → GND
  - OUT → GPIO 34 (ADC)

Sensor EC:
  - VCC → 3.3V
  - GND → GND
  - OUT → GPIO 35 (ADC)

Sensor Luz:
  - VCC → 3.3V
  - GND → GND
  - OUT → GPIO 32 (ADC)
```

### Actuadores
```
Bomba Recirculación:
  - Relé → GPIO 26

LED Grow:
  - Relé → GPIO 27

Bomba Dosificadora A:
  - Relé → GPIO 25

Bomba Dosificadora B:
  - Relé → GPIO 33
```

## 🚀 Instalación

### Opción 1: PlatformIO (Recomendado)

1. Instalar PlatformIO IDE o extension para VS Code
2. Abrir la carpeta `firmware` en PlatformIO
3. Copiar `config/config.h.example` a `config/config.h`
4. Editar `config/config.h` con tus credenciales WiFi y configuración
5. Compilar y subir:
   ```bash
   pio run --target upload
   ```

### Opción 2: Arduino IDE

1. Instalar Arduino IDE
2. Instalar soporte para ESP32:
   - Archivo → Preferencias
   - URLs de tarjetas: `https://dl.espressif.com/dl/package_esp32_index.json`
3. Instalar librerías requeridas:
   - ArduinoJson
   - DHT sensor library
   - DallasTemperature
   - OneWire
4. Abrir `src/main.cpp`
5. Copiar `config/config.h.example` a `config/config.h` y configurar
6. Seleccionar placa ESP32 Dev Module
7. Compilar y subir

## ⚙️ Configuración

Editar `config/config.h`:

```cpp
// WiFi
#define WIFI_SSID "TuWiFi"
#define WIFI_PASSWORD "TuContraseña"

// API Backend
#define API_ENDPOINT "http://192.168.1.100:3000"
#define DEVICE_ID "ESP32-001"

// Calibración de sensores (ajustar después de calibrar)
#define PH_NEUTRAL_VOLTAGE 2.5
#define EC_CONVERSION_FACTOR 1000.0
```

## 📊 Calibración de Sensores

### Sensor de pH

1. Preparar soluciones buffer de pH 4.0, 7.0 y 10.0
2. Sumergir sensor en buffer pH 7.0
3. Leer voltaje y ajustar `PH_NEUTRAL_VOLTAGE`
4. Verificar con otros buffers y ajustar la fórmula si es necesario

### Sensor de EC

1. Preparar solución de calibración (ej: 1413 µS/cm)
2. Sumergir sensor en la solución
3. Leer voltaje y calcular `EC_CONVERSION_FACTOR`
4. Verificar con diferentes soluciones conocidas

### Sensor de Temperatura

Los sensores DS18B20 y DHT22 vienen calibrados de fábrica, pero se puede verificar con un termómetro de referencia.

## 🔍 Monitoreo

El firmware imprime información por Serial a 115200 baudios:

```
BlackMamba Smart Farming - Iniciando...
Conectando a WiFi: MiWiFi
WiFi conectado!
IP: 192.168.1.150
Sistema listo!

--- Lectura de sensores ---
pH: 6.2
EC: 1200.5 µS/cm
Temp Agua: 21.3 °C
Temp Aire: 24.5 °C
Humedad: 65.2 %
Luz: 1850
Enviando datos al backend...
Respuesta del servidor: {"status":"ok"}
Bomba de recirculación: ON
```

## 🛠️ Troubleshooting

### WiFi no conecta
- Verificar SSID y contraseña
- Verificar que la red esté en 2.4 GHz (ESP32 no soporta 5 GHz)
- Verificar señal WiFi

### Sensor devuelve -127 o NaN
- Verificar conexiones
- Verificar alimentación (3.3V o 5V según sensor)
- Para DS18B20, verificar resistencia pull-up de 4.7kΩ

### No envía datos al backend
- Verificar que el backend esté corriendo
- Verificar URL en `API_ENDPOINT`
- Verificar conectividad de red
- Revisar logs en Serial Monitor

## 📝 Notas

- El sistema lee sensores cada 60 segundos por defecto
- La bomba se activa automáticamente cada hora por 10 minutos
- Las luces se encienden automáticamente cuando hay poca luz
- Los datos se envían al backend después de cada lectura

## 🔐 Seguridad

- No compartir el archivo `config/config.h` con credenciales
- Usar contraseñas seguras para WiFi
- Considerar usar HTTPS para comunicación con el backend en producción
