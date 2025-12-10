/**
 * Rutas para sensores
 */

const express = require('express');
const { body, query, validationResult } = require('express-validator');
const { saveSensorData, getSensorHistory } = require('../services/database');
const { evaluateSensorData } = require('../services/alerts');

const router = express.Router();

/**
 * POST /api/sensors/data
 * Recibe datos de sensores del ESP32
 */
router.post('/data',
  [
    body('deviceId').notEmpty().withMessage('deviceId es requerido'),
    body('pH').isFloat({ min: 0, max: 14 }).withMessage('pH debe estar entre 0 y 14'),
    body('ec').isFloat({ min: 0 }).withMessage('EC debe ser un número positivo'),
    body('waterTemp').isFloat().withMessage('waterTemp debe ser un número'),
    body('airTemp').isFloat().withMessage('airTemp debe ser un número'),
    body('humidity').isFloat({ min: 0, max: 100 }).withMessage('humidity debe estar entre 0 y 100'),
    body('lightLevel').isInt({ min: 0 }).withMessage('lightLevel debe ser un número entero positivo')
  ],
  async (req, res) => {
    // Validar entrada
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const sensorData = req.body;
      
      // Guardar datos
      const savedData = await saveSensorData(sensorData);
      
      // Evaluar y generar alertas si es necesario
      const alerts = await evaluateSensorData(sensorData);
      
      res.status(201).json({
        status: 'success',
        message: 'Datos guardados correctamente',
        data: savedData,
        alerts: alerts.filter(a => a !== null)
      });
    } catch (error) {
      console.error('Error guardando datos de sensores:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error guardando datos'
      });
    }
  }
);

/**
 * GET /api/sensors/history
 * Obtiene histórico de datos de sensores
 */
router.get('/history',
  [
    query('deviceId').optional().isString(),
    query('limit').optional().isInt({ min: 1, max: 1000 }).toInt()
  ],
  async (req, res) => {
    try {
      const { deviceId, limit = 100 } = req.query;
      
      const history = await getSensorHistory(deviceId, limit);
      
      res.json({
        status: 'success',
        count: history.length,
        data: history
      });
    } catch (error) {
      console.error('Error obteniendo histórico:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error obteniendo histórico'
      });
    }
  }
);

/**
 * GET /api/sensors/latest
 * Obtiene la última lectura de sensores
 */
router.get('/latest',
  [
    query('deviceId').optional().isString()
  ],
  async (req, res) => {
    try {
      const { deviceId } = req.query;
      
      const history = await getSensorHistory(deviceId, 1);
      
      if (history.length === 0) {
        return res.status(404).json({
          status: 'error',
          message: 'No se encontraron datos'
        });
      }
      
      res.json({
        status: 'success',
        data: history[0]
      });
    } catch (error) {
      console.error('Error obteniendo última lectura:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error obteniendo datos'
      });
    }
  }
);

/**
 * GET /api/sensors/stats
 * Obtiene estadísticas de sensores
 */
router.get('/stats',
  [
    query('deviceId').optional().isString(),
    query('hours').optional().isInt({ min: 1, max: 168 }).toInt() // Máximo 1 semana
  ],
  async (req, res) => {
    try {
      const { deviceId, hours = 24 } = req.query;
      
      const history = await getSensorHistory(deviceId, 1000);
      
      // Filtrar por tiempo
      const cutoffTime = Date.now() - (hours * 60 * 60 * 1000);
      const recentData = history.filter(d => d.timestamp > cutoffTime);
      
      if (recentData.length === 0) {
        return res.json({
          status: 'success',
          message: 'No hay datos en el período especificado',
          stats: null
        });
      }
      
      // Calcular estadísticas
      const stats = {
        pH: calculateStats(recentData, 'pH'),
        ec: calculateStats(recentData, 'ec'),
        waterTemp: calculateStats(recentData, 'waterTemp'),
        airTemp: calculateStats(recentData, 'airTemp'),
        humidity: calculateStats(recentData, 'humidity'),
        lightLevel: calculateStats(recentData, 'lightLevel'),
        dataPoints: recentData.length
      };
      
      res.json({
        status: 'success',
        period: `${hours} horas`,
        stats
      });
    } catch (error) {
      console.error('Error calculando estadísticas:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error calculando estadísticas'
      });
    }
  }
);

/**
 * Función auxiliar para calcular estadísticas
 */
function calculateStats(data, field) {
  const values = data.map(d => d[field]).filter(v => v !== null && v !== undefined);
  
  if (values.length === 0) {
    return null;
  }
  
  const sum = values.reduce((a, b) => a + b, 0);
  const avg = sum / values.length;
  const min = Math.min(...values);
  const max = Math.max(...values);
  
  return {
    avg: parseFloat(avg.toFixed(2)),
    min: parseFloat(min.toFixed(2)),
    max: parseFloat(max.toFixed(2)),
    current: values[0]
  };
}

module.exports = router;
