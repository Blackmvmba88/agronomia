# API Documentation - BlackMamba Smart Farming

Documentación completa de los endpoints de la API REST.

## Base URL

```
http://localhost:3000/api
```

## Endpoints

### 📊 Sensores

#### POST `/sensors/data`

Recibe y almacena datos de sensores desde el ESP32.

**Request Body:**
```json
{
  "deviceId": "ESP32-001",
  "pH": 6.2,
  "ec": 1200.5,
  "waterTemp": 21.3,
  "airTemp": 24.5,
  "humidity": 65.2,
  "lightLevel": 1850,
  "timestamp": 1234567890
}
```

**Response:** `201 Created`
```json
{
  "status": "success",
  "message": "Datos guardados correctamente",
  "data": {
    "id": "abc123",
    "deviceId": "ESP32-001",
    "pH": 6.2,
    ...
  },
  "alerts": []
}
```

**Validaciones:**
- `deviceId`: Requerido, string
- `pH`: Número entre 0 y 14
- `ec`: Número positivo
- `waterTemp`: Número
- `airTemp`: Número
- `humidity`: Número entre 0 y 100
- `lightLevel`: Entero positivo

---

#### GET `/sensors/history`

Obtiene el histórico de datos de sensores.

**Query Parameters:**
- `deviceId` (opcional): ID del dispositivo
- `limit` (opcional): Número de registros (default: 100, max: 1000)

**Response:** `200 OK`
```json
{
  "status": "success",
  "count": 50,
  "data": [
    {
      "id": "abc123",
      "deviceId": "ESP32-001",
      "pH": 6.2,
      "ec": 1200.5,
      "waterTemp": 21.3,
      "airTemp": 24.5,
      "humidity": 65.2,
      "lightLevel": 1850,
      "timestamp": 1234567890,
      "createdAt": "2024-01-01T12:00:00Z"
    },
    ...
  ]
}
```

---

#### GET `/sensors/latest`

Obtiene la última lectura de sensores.

**Query Parameters:**
- `deviceId` (opcional): ID del dispositivo

**Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "abc123",
    "deviceId": "ESP32-001",
    "pH": 6.2,
    "ec": 1200.5,
    "waterTemp": 21.3,
    "airTemp": 24.5,
    "humidity": 65.2,
    "lightLevel": 1850,
    "timestamp": 1234567890
  }
}
```

---

#### GET `/sensors/stats`

Obtiene estadísticas de sensores (promedio, mínimo, máximo).

**Query Parameters:**
- `deviceId` (opcional): ID del dispositivo
- `hours` (opcional): Período en horas (default: 24, max: 168)

**Response:** `200 OK`
```json
{
  "status": "success",
  "period": "24 horas",
  "stats": {
    "pH": {
      "avg": 6.15,
      "min": 5.8,
      "max": 6.5,
      "current": 6.2
    },
    "ec": {
      "avg": 1180.5,
      "min": 1050.0,
      "max": 1300.0,
      "current": 1200.5
    },
    "waterTemp": {
      "avg": 21.2,
      "min": 19.5,
      "max": 23.0,
      "current": 21.3
    },
    ...
  }
}
```

---

### ⚙️ Actuadores

#### POST `/actuators/control`

Controla el estado de un actuador (bomba, luz, etc).

**Request Body:**
```json
{
  "deviceId": "ESP32-001",
  "actuator": "pump",
  "state": true
}
```

**Actuadores válidos:**
- `pump`: Bomba de recirculación
- `led`: Iluminación LED
- `pumpA`: Bomba dosificadora A
- `pumpB`: Bomba dosificadora B

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Actuador pump activado",
  "data": {
    "id": "xyz789",
    "deviceId": "ESP32-001",
    "actuator": "pump",
    "state": true
  }
}
```

---

#### GET `/actuators/status`

Obtiene el estado actual de todos los actuadores.

**Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "pump": false,
    "led": true,
    "pumpA": false,
    "pumpB": false
  }
}
```

---

### 🚨 Alertas

#### GET `/alerts`

Obtiene todas las alertas activas (no resueltas).

**Query Parameters:**
- `deviceId` (opcional): ID del dispositivo

**Response:** `200 OK`
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "id": "alert123",
      "deviceId": "ESP32-001",
      "parameter": "pH",
      "condition": "bajo",
      "value": 5.2,
      "threshold": 5.5,
      "message": "pH bajo: 5.2 (umbral: 5.5)",
      "severity": "high",
      "resolved": false,
      "timestamp": 1234567890,
      "createdAt": "2024-01-01T12:00:00Z"
    },
    ...
  ]
}
```

**Niveles de severidad:**
- `critical`: Diferencia > 20% del umbral
- `high`: Diferencia > 10% del umbral
- `medium`: Diferencia < 10% del umbral

---

#### POST `/alerts/:id/resolve`

Marca una alerta como resuelta.

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Alerta resuelta correctamente"
}
```

---

### 📱 Dispositivos

#### GET `/devices`

Lista todos los dispositivos registrados.

**Response:** `200 OK`
```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": "ESP32-001",
      "name": "Sistema Principal",
      "status": "online",
      "lastSeen": 1234567890
    }
  ]
}
```

---

#### GET `/devices/:id`

Obtiene información detallada de un dispositivo.

**Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "ESP32-001",
    "name": "Sistema Principal",
    "status": "online",
    "lastSeen": 1234567890,
    "firmware": "1.0.0"
  }
}
```

---

## Códigos de Estado HTTP

- `200 OK`: Petición exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos enviados
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Manejo de Errores

Todos los endpoints devuelven errores en el siguiente formato:

```json
{
  "status": "error",
  "message": "Descripción del error",
  "errors": [
    {
      "field": "pH",
      "message": "pH debe estar entre 0 y 14"
    }
  ]
}
```

## Rate Limiting

Por implementar en versiones futuras.

## Autenticación

Por implementar en versiones futuras. Actualmente la API es abierta.

## Ejemplos con cURL

### Enviar datos de sensores
```bash
curl -X POST http://localhost:3000/api/sensors/data \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "ESP32-001",
    "pH": 6.2,
    "ec": 1200,
    "waterTemp": 21.5,
    "airTemp": 24.0,
    "humidity": 65,
    "lightLevel": 1850,
    "timestamp": 1234567890
  }'
```

### Obtener histórico
```bash
curl http://localhost:3000/api/sensors/history?limit=10
```

### Controlar actuador
```bash
curl -X POST http://localhost:3000/api/actuators/control \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "ESP32-001",
    "actuator": "pump",
    "state": true
  }'
```

### Obtener alertas
```bash
curl http://localhost:3000/api/alerts
```

## WebSocket (Próximamente)

Se planea agregar soporte para WebSocket para actualizaciones en tiempo real sin polling.
