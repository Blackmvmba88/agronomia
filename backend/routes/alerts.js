/**
 * Rutas para alertas
 */

const express = require('express');
const { param, query } = require('express-validator');
const { getActiveAlerts, resolveAlert } = require('../services/database');

const router = express.Router();

/**
 * GET /api/alerts
 * Obtiene alertas activas
 */
router.get('/',
  [
    query('deviceId').optional().isString()
  ],
  async (req, res) => {
    try {
      const { deviceId } = req.query;
      
      const alerts = await getActiveAlerts(deviceId);
      
      res.json({
        status: 'success',
        count: alerts.length,
        data: alerts
      });
    } catch (error) {
      console.error('Error obteniendo alertas:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error obteniendo alertas'
      });
    }
  }
);

/**
 * POST /api/alerts/:id/resolve
 * Marca una alerta como resuelta
 */
router.post('/:id/resolve',
  [
    param('id').notEmpty().withMessage('ID de alerta requerido')
  ],
  async (req, res) => {
    try {
      const { id } = req.params;
      
      await resolveAlert(id);
      
      res.json({
        status: 'success',
        message: 'Alerta resuelta correctamente'
      });
    } catch (error) {
      console.error('Error resolviendo alerta:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error resolviendo alerta'
      });
    }
  }
);

module.exports = router;
