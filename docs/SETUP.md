# Guía de Setup - BlackMamba Smart Farming

Guía completa para configurar el sistema desde cero.

## 📋 Prerrequisitos

### Hardware
- ESP32 DevKit (o compatible)
- Sensores:
  - DHT22 (temperatura y humedad)
  - DS18B20 (temperatura del agua)
  - Sensor de pH analógico
  - Sensor de EC/TDS
  - Fotoresistencia LDR o BH1750
- Actuadores:
  - Módulo relé de 4 canales
  - Bomba sumergible 12V
  - Tira LED o lámpara de crecimiento
- Fuente de alimentación 12V/5A
- Cables jumper y protoboard

### Software
- Arduino IDE o PlatformIO
- Node.js >= 16.0.0
- Git
- Cuenta de Firebase (o Supabase)

## 🔧 Paso 1: Hardware

### 1.1 Conexiones del ESP32

#### Sensores

**DHT22 - Temperatura y Humedad Ambiente:**
```
DHT22 VCC → ESP32 3.3V
DHT22 GND → ESP32 GND
DHT22 DATA → ESP32 GPIO 4
```

**DS18B20 - Temperatura del Agua:**
```
DS18B20 VCC → ESP32 3.3V
DS18B20 GND → ESP32 GND
DS18B20 DATA → ESP32 GPIO 5
(Agregar resistencia pull-up de 4.7kΩ entre VCC y DATA)
```

**Sensor de pH:**
```
pH VCC → ESP32 3.3V
pH GND → ESP32 GND
pH OUT → ESP32 GPIO 34 (ADC1_CH6)
```

**Sensor de EC:**
```
EC VCC → ESP32 3.3V
EC GND → ESP32 GND
EC OUT → ESP32 GPIO 35 (ADC1_CH7)
```

**Sensor de Luz (LDR):**
```
LDR → ESP32 GPIO 32 (ADC1_CH4)
LDR → Resistencia 10kΩ → GND
```

#### Actuadores (a través de módulo relé)

**Módulo Relé:**
```
Relé VCC → ESP32 5V (o fuente externa)
Relé GND → ESP32 GND
Relé IN1 → ESP32 GPIO 26 (Bomba)
Relé IN2 → ESP32 GPIO 27 (LED)
Relé IN3 → ESP32 GPIO 25 (Bomba A)
Relé IN4 → ESP32 GPIO 33 (Bomba B)
```

**Bomba de Recirculación:**
```
Bomba + → Relé NO (Normalmente Abierto)
Bomba - → Fuente 12V GND
Relé COM → Fuente 12V +
```

### 1.2 Esquema de Conexión

```
ESP32                    Sensores
┌─────────┐             ┌─────────┐
│         │             │  DHT22  │
│  GPIO 4 ├─────────────┤  DATA   │
│         │             └─────────┘
│  GPIO 5 ├─────────┐   ┌─────────┐
│         │         └───┤ DS18B20 │
│ GPIO 34 ├─────────────┤   pH    │
│ GPIO 35 ├─────────────┤   EC    │
│ GPIO 32 ├─────────────┤  LDR    │
│         │             └─────────┘
│         │
│ GPIO 26 ├─────────┐   ┌─────────┐
│ GPIO 27 ├─────────┼───┤  RELÉ   │
│ GPIO 25 ├─────────┤   │  4CH    │
│ GPIO 33 ├─────────┘   └─────────┘
└─────────┘
```

## 💻 Paso 2: Firmware ESP32

### 2.1 Instalar Arduino IDE

1. Descargar desde [arduino.cc](https://www.arduino.cc/en/software)
2. Instalar soporte para ESP32:
   - Archivo → Preferencias
   - URLs de tarjetas: `https://dl.espressif.com/dl/package_esp32_index.json`
   - Herramientas → Placa → Gestor de tarjetas
   - Buscar "esp32" e instalar "esp32 by Espressif Systems"

### 2.2 Instalar Librerías

En Arduino IDE:
- Programa → Incluir Librería → Administrar Bibliotecas
- Instalar:
  - ArduinoJson
  - DHT sensor library
  - Adafruit Unified Sensor
  - DallasTemperature
  - OneWire

### 2.3 Configurar y Subir Firmware

1. Copiar `firmware/config/config.h.example` a `firmware/config/config.h`
2. Editar `config.h` con tu WiFi y endpoint:
```cpp
#define WIFI_SSID "TuWiFi"
#define WIFI_PASSWORD "TuPassword"
#define API_ENDPOINT "http://192.168.1.100:3000"
```
3. Abrir `firmware/src/main.cpp` en Arduino IDE
4. Seleccionar placa: Herramientas → Placa → ESP32 Dev Module
5. Seleccionar puerto COM correcto
6. Subir código (botón →)
7. Abrir Monitor Serial (115200 baudios) para ver logs

## 🗄️ Paso 3: Backend

### 3.1 Configurar Firebase

1. Ir a [Firebase Console](https://console.firebase.google.com/)
2. Crear nuevo proyecto
3. Habilitar Firestore Database:
   - Build → Firestore Database → Crear base de datos
   - Iniciar en modo de prueba
4. Crear cuenta de servicio:
   - Configuración del proyecto → Cuentas de servicio
   - Generar nueva clave privada
   - Guardar archivo JSON

### 3.2 Instalar y Configurar Backend

```bash
cd backend
npm install
cp .env.example .env
```

Editar `.env`:
```env
PORT=3000
NODE_ENV=development

FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_CLIENT_EMAIL=tu-email@proyecto.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

ALERT_PH_MIN=5.5
ALERT_PH_MAX=6.5
ALERT_EC_MIN=800
ALERT_EC_MAX=1500
```

### 3.3 Iniciar Backend

```bash
npm run dev
```

Verificar que esté corriendo en `http://localhost:3000`

## 🎨 Paso 4: Frontend

### 4.1 Instalar y Configurar

```bash
cd frontend
npm install
cp .env.example .env
```

Editar `.env`:
```env
REACT_APP_API_URL=http://localhost:3000/api
```

### 4.2 Iniciar Frontend

```bash
npm start
```

El dashboard se abrirá en `http://localhost:3001`

## 🧪 Paso 5: Calibración de Sensores

### 5.1 Calibrar pH

1. Preparar soluciones buffer de pH 4.0, 7.0 y 10.0
2. Sumergir sensor en buffer pH 7.0
3. En Monitor Serial del ESP32, observar el voltaje
4. Ajustar `PH_NEUTRAL_VOLTAGE` en `config.h` con ese voltaje
5. Volver a subir el código
6. Verificar con los otros buffers

### 5.2 Calibrar EC

1. Preparar solución de calibración conocida (ej: 1413 µS/cm)
2. Sumergir sensor
3. Observar voltaje en Monitor Serial
4. Calcular: `EC_CONVERSION_FACTOR = EC_conocido / voltaje`
5. Ajustar en `config.h`
6. Volver a subir el código

### 5.3 Verificar Temperatura

Los sensores DS18B20 y DHT22 vienen calibrados. Verificar con termómetro de referencia si es necesario.

## ✅ Paso 6: Prueba del Sistema

### 6.1 Verificar Comunicación

1. Encender ESP32
2. Observar en Monitor Serial:
   - Conexión WiFi exitosa
   - Lecturas de sensores cada 60 segundos
   - Envío de datos al backend

### 6.2 Verificar Backend

1. Ver logs del backend
2. Verificar que recibe datos del ESP32
3. Revisar Firestore Database para ver datos almacenados

### 6.3 Verificar Dashboard

1. Abrir `http://localhost:3001`
2. Ver tarjetas de sensores con datos actuales
3. Ver gráficas históricas
4. Probar control de actuadores

## 🚀 Paso 7: Producción (Opcional)

### 7.1 Configurar IP Estática

En tu router, asigna IP estática al ESP32 basado en su MAC address.

### 7.2 Deploy del Backend

Opciones:
- **Heroku**: `git push heroku main`
- **Railway**: Conectar repo y deploy automático
- **VPS**: Usar PM2 para mantener proceso corriendo

### 7.3 Deploy del Frontend

Opciones:
- **Netlify**: Conectar repo o subir carpeta `build/`
- **Vercel**: `vercel --prod`
- **GitHub Pages**: Configurar en settings del repo

### 7.4 Actualizar Config del ESP32

Cambiar `API_ENDPOINT` en `config.h` a la URL de producción del backend.

## 🔒 Paso 8: Seguridad

1. Cambiar reglas de Firestore a modo seguro
2. Implementar autenticación en backend
3. Usar HTTPS en producción
4. No compartir credenciales en el código

## 📱 Paso 9: Monitoreo

1. Configurar alertas en Firebase
2. Agregar logging en producción
3. Configurar backups automáticos de Firestore

## 🐛 Troubleshooting

Ver sección de troubleshooting en cada README:
- `firmware/README.md`
- `backend/README.md`
- `frontend/README.md`

## 🎉 ¡Sistema Listo!

Tu sistema BlackMamba Smart Farming está funcionando. Ahora puedes:
- Monitorear condiciones en tiempo real
- Ver tendencias históricas
- Controlar actuadores remotamente
- Recibir alertas automáticas

## 📚 Próximos Pasos

- Calibrar umbrales de alertas según tu cultivo
- Ajustar tiempos de activación de bombas
- Personalizar dashboard
- Agregar más sensores o actuadores
