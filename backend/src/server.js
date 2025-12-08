/**
 * BlackMamba Smart Farming - Backend Server
 * 
 * API REST para recibir datos de sensores del ESP32 y servir
 * información al dashboard web
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const bodyParser = require('body-parser');
require('dotenv').config();

// Importar rutas
const sensorRoutes = require('./routes/sensors');
const actuatorRoutes = require('./routes/actuators');
const alertRoutes = require('./routes/alerts');
const deviceRoutes = require('./routes/devices');

// Importar servicios
const { initializeFirebase } = require('./services/database');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(helmet()); // Seguridad HTTP headers
app.use(cors({
  origin: process.env.CORS_ORIGIN?.split(',') || '*'
}));
app.use(morgan('dev')); // Logs de peticiones
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Inicializar base de datos
initializeFirebase();

// Rutas
app.get('/', (req, res) => {
  res.json({
    message: 'BlackMamba Smart Farming API',
    version: '1.0.0',
    endpoints: {
      sensors: '/api/sensors',
      actuators: '/api/actuators',
      alerts: '/api/alerts',
      devices: '/api/devices'
    }
  });
});

app.use('/api/sensors', sensorRoutes);
app.use('/api/actuators', actuatorRoutes);
app.use('/api/alerts', alertRoutes);
app.use('/api/devices', deviceRoutes);

// Manejador de errores
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Manejador 404
app.use((req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: 'Endpoint no encontrado'
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 BlackMamba Smart Farming API corriendo en puerto ${PORT}`);
  console.log(`🌐 Entorno: ${process.env.NODE_ENV || 'development'}`);
  console.log(`📡 Endpoints disponibles en http://localhost:${PORT}`);
});

module.exports = app;
