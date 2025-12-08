# BlackMamba Smart Farming – MVP Hidropónico Autónomo

Sistema modular para cultivo hidropónico con monitoreo y control automatizado. Mide sensores en tiempo real (pH, EC, temperatura, humedad, luminosidad) y permite operar bombas, válvulas y luces desde una app o dashboard web.

## 🎯 Objetivo del MVP

Crear un ecosistema hidropónico autónomo con:

* Sensores y actuadores conectados
* Dashboard de datos en tiempo real
* Alertas automáticas según condiciones fuera de rango
* Control remoto básico de bombas y luces

## 🏗️ Arquitectura General

* **Hardware:** ESP32 + sensores (pH, EC, temperatura agua y ambiente, luminosidad), actuadores (bomba, válvulas, LEDs)
* **Conectividad:** WiFi para comunicación con backend
* **Backend:** Node.js con Express y Firestore/Supabase para almacenamiento
* **Frontend:** React Web para dashboard de visualización, alertas y control

## 📊 Sensores Iniciales

* pH del agua
* Conductividad eléctrica (EC)
* Temperatura del agua
* Temperatura y humedad ambiente
* Luminosidad

## ⚙️ Actuadores Iniciales

* Bomba de recirculación
* Bombas dosificadoras de nutrientes A/B (opcional en MVP)
* Iluminación LED

## 🚀 Funciones del Sistema

* Registro periódico de sensores
* Gráficas históricas de condiciones
* Alarmas cuando algo sale de rango
* Control remoto de bomba e iluminación

## 📁 Estructura del Proyecto

```
agronomia/
├── firmware/              # Código para ESP32
│   ├── src/              # Código principal
│   ├── lib/              # Librerías personalizadas
│   └── config/           # Configuraciones
├── backend/              # API y servidor
│   ├── src/              # Código fuente
│   ├── routes/           # Endpoints API
│   └── services/         # Lógica de negocio
├── frontend/             # Dashboard web
│   ├── src/              # Código React
│   ├── components/       # Componentes reutilizables
│   └── pages/            # Páginas principales
└── docs/                 # Documentación
```

## 🔧 Stack Tecnológico

* **Firmware:** Arduino/PlatformIO para ESP32
* **Backend:** Node.js con Express
* **Base de Datos:** Firestore o Supabase
* **Frontend:** React con Chart.js para visualización

## 📡 API / Comunicación

El ESP32 envía datos en intervalos configurables:
* POST `/api/sensors/data` - Enviar lectura de sensores
* GET `/api/sensors/history` - Obtener histórico
* POST `/api/actuators/control` - Controlar actuadores
* GET `/api/alerts` - Obtener alertas activas

## 🛠️ Instalación

### Backend
```bash
cd backend
npm install
cp .env.example .env
# Configurar variables de entorno
npm run dev
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Firmware
```bash
cd firmware
# Configurar WiFi y endpoints en config/config.h
# Usar PlatformIO o Arduino IDE para cargar a ESP32
```

## 📋 Roadmap

1. ✅ Configurar estructura del proyecto
2. ⏳ Configurar y calibrar sensores
3. ⏳ Programar firmware del ESP32
4. ⏳ Backend con endpoints básicos y almacenamiento
5. ⏳ Dashboard y control remoto
6. ⏳ Validación con cultivo real

## 📝 Licencia

MIT – Abierto para colaboración

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**BlackMamba Smart Farming** - Cultivo inteligente para el futuro 🌱
