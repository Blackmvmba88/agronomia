# Backend - BlackMamba Smart Farming

API REST para el sistema de cultivo hidropónico BlackMamba Smart Farming.

## 🚀 Características

- Recepción de datos de sensores desde ESP32
- Almacenamiento en Firestore
- API REST para consulta de datos
- Sistema de alertas automático
- Control de actuadores
- Histórico y estadísticas

## 📋 Requisitos

- Node.js >= 16.0.0
- npm o yarn
- Cuenta de Firebase (Firestore) o Supabase

## 🔧 Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
```

3. Editar `.env` con tus credenciales:
```env
PORT=3000
NODE_ENV=development

# Firebase (opción recomendada)
FIREBASE_PROJECT_ID=tu-proyecto-id
FIREBASE_CLIENT_EMAIL=tu-email@proyecto.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

# Configuración de alertas
ALERT_PH_MIN=5.5
ALERT_PH_MAX=6.5
# ... (ver .env.example para más opciones)
```

## 🏃 Ejecutar

### Modo desarrollo (con auto-reload)
```bash
npm run dev
```

### Modo producción
```bash
npm start
```

El servidor iniciará en `http://localhost:3000`

## 📡 API Endpoints

### Sensores

#### POST `/api/sensors/data`
Recibe datos de sensores del ESP32

**Body:**
```json
{
  "deviceId": "ESP32-001",
  "pH": 6.2,
  "ec": 1200,
  "waterTemp": 21.5,
  "airTemp": 24.0,
  "humidity": 65,
  "lightLevel": 1850,
  "timestamp": 1234567890
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Datos guardados correctamente",
  "data": { ... },
  "alerts": []
}
```

#### GET `/api/sensors/history?deviceId=ESP32-001&limit=100`
Obtiene histórico de datos

**Response:**
```json
{
  "status": "success",
  "count": 100,
  "data": [...]
}
```

#### GET `/api/sensors/latest?deviceId=ESP32-001`
Obtiene la última lectura

#### GET `/api/sensors/stats?deviceId=ESP32-001&hours=24`
Obtiene estadísticas (promedio, min, max)

### Actuadores

#### POST `/api/actuators/control`
Controla actuadores

**Body:**
```json
{
  "deviceId": "ESP32-001",
  "actuator": "pump",
  "state": true
}
```

Actuadores disponibles: `pump`, `led`, `pumpA`, `pumpB`

#### GET `/api/actuators/status`
Obtiene estado actual de actuadores

### Alertas

#### GET `/api/alerts?deviceId=ESP32-001`
Obtiene alertas activas

#### POST `/api/alerts/:id/resolve`
Marca una alerta como resuelta

### Dispositivos

#### GET `/api/devices`
Lista dispositivos registrados

#### GET `/api/devices/:id`
Información de un dispositivo específico

## 🗄️ Configuración de Firebase

1. Crear proyecto en [Firebase Console](https://console.firebase.google.com/)
2. Habilitar Firestore Database
3. Crear cuenta de servicio:
   - Ir a Project Settings → Service Accounts
   - Generar nueva clave privada
   - Descargar archivo JSON
4. Copiar credenciales al archivo `.env`

### Estructura de datos en Firestore

**Colección `sensorData`:**
```json
{
  "deviceId": "ESP32-001",
  "pH": 6.2,
  "ec": 1200,
  "waterTemp": 21.5,
  "airTemp": 24.0,
  "humidity": 65,
  "lightLevel": 1850,
  "timestamp": 1234567890,
  "createdAt": "2024-01-01T12:00:00Z"
}
```

**Colección `alerts`:**
```json
{
  "deviceId": "ESP32-001",
  "parameter": "pH",
  "condition": "bajo",
  "value": 5.2,
  "threshold": 5.5,
  "message": "pH bajo: 5.2 (umbral: 5.5)",
  "severity": "high",
  "resolved": false,
  "createdAt": "2024-01-01T12:00:00Z"
}
```

**Colección `actuatorStates`:**
```json
{
  "deviceId": "ESP32-001",
  "actuator": "pump",
  "state": true,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧪 Testing

```bash
npm test
```

## 🔒 Seguridad

- Helmet.js para headers HTTP seguros
- CORS configurado
- Validación de entrada con express-validator
- Variables de entorno para credenciales

## 🐛 Troubleshooting

### Error: Firebase not configured
- Verificar variables de entorno en `.env`
- Asegurar que las credenciales de Firebase sean correctas
- El sistema puede funcionar en modo local sin Firebase para desarrollo

### Error de CORS
- Verificar `CORS_ORIGIN` en `.env`
- Agregar origen del frontend a la lista

### Puerto ya en uso
- Cambiar `PORT` en `.env`
- O detener el proceso que usa el puerto 3000

## 📚 Dependencias Principales

- **express**: Framework web
- **firebase-admin**: SDK de Firebase
- **cors**: Middleware CORS
- **helmet**: Seguridad HTTP
- **express-validator**: Validación de datos
- **morgan**: Logger de peticiones

## 🚢 Deployment

### Heroku
```bash
heroku create blackmamba-api
heroku config:set FIREBASE_PROJECT_ID=...
git push heroku main
```

### Railway/Render
1. Conectar repositorio
2. Configurar variables de entorno
3. Deploy automático

### Docker (Próximamente)
```bash
docker build -t blackmamba-api .
docker run -p 3000:3000 blackmamba-api
```

## 📝 Roadmap

- [ ] Autenticación con JWT
- [ ] WebSocket para datos en tiempo real
- [ ] Integración con MQTT para control bidireccional
- [ ] Notificaciones push
- [ ] Dashboard de administración
- [ ] Backup automático de datos

## 📄 Licencia

MIT
