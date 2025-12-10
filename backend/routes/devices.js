/**
 * Rutas para dispositivos
 */

const express = require('express');

const router = express.Router();

/**
 * GET /api/devices
 * Lista dispositivos registrados
 */
router.get('/', (req, res) => {
  // TODO: Implementar listado real desde base de datos
  const devices = [
    {
      id: 'ESP32-001',
      name: 'Sistema Principal',
      status: 'online',
      lastSeen: Date.now()
    }
  ];
  
  res.json({
    status: 'success',
    count: devices.length,
    data: devices
  });
});

/**
 * GET /api/devices/:id
 * Obtiene información de un dispositivo específico
 */
router.get('/:id', (req, res) => {
  const { id } = req.params;
  
  // TODO: Implementar obtención desde base de datos
  const device = {
    id: id,
    name: 'Sistema Principal',
    status: 'online',
    lastSeen: Date.now(),
    firmware: '1.0.0'
  };
  
  res.json({
    status: 'success',
    data: device
  });
});

module.exports = router;
