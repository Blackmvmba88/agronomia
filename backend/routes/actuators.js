/**
 * Rutas para actuadores
 */

const express = require('express');
const { body, validationResult } = require('express-validator');
const { saveActuatorState } = require('../services/database');

const router = express.Router();

/**
 * POST /api/actuators/control
 * Controla actuadores (bombas, luces, etc)
 */
router.post('/control',
  [
    body('deviceId').notEmpty().withMessage('deviceId es requerido'),
    body('actuator').isIn(['pump', 'led', 'pumpA', 'pumpB']).withMessage('Actuador no válido'),
    body('state').isBoolean().withMessage('state debe ser true o false')
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const { deviceId, actuator, state } = req.body;
      
      // Guardar estado del actuador
      const savedState = await saveActuatorState(deviceId, actuator, state);
      
      // TODO: En una implementación completa, aquí se enviaría un comando
      // al ESP32 vía MQTT o similar para cambiar el estado del actuador
      
      console.log(`🔧 Control de actuador: ${actuator} = ${state ? 'ON' : 'OFF'} (${deviceId})`);
      
      res.json({
        status: 'success',
        message: `Actuador ${actuator} ${state ? 'activado' : 'desactivado'}`,
        data: savedState
      });
    } catch (error) {
      console.error('Error controlando actuador:', error);
      res.status(500).json({
        status: 'error',
        message: 'Error controlando actuador'
      });
    }
  }
);

/**
 * GET /api/actuators/status
 * Obtiene el estado actual de los actuadores
 */
router.get('/status', async (req, res) => {
  try {
    // TODO: Implementar obtención de estado actual desde la base de datos
    // Por ahora, devolver estado de ejemplo
    
    const status = {
      pump: false,
      led: false,
      pumpA: false,
      pumpB: false
    };
    
    res.json({
      status: 'success',
      data: status
    });
  } catch (error) {
    console.error('Error obteniendo estado de actuadores:', error);
    res.status(500).json({
      status: 'error',
      message: 'Error obteniendo estado'
    });
  }
});

module.exports = router;
