/**
 * Servicio API - Cliente para comunicación con el backend
 */

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Obtiene el histórico de datos de sensores
 */
export const getSensorHistory = async (limit = 50, deviceId = null) => {
  try {
    const params = { limit };
    if (deviceId) params.deviceId = deviceId;
    
    const response = await api.get('/sensors/history', { params });
    return response.data.data || [];
  } catch (error) {
    console.error('Error obteniendo histórico:', error);
    return [];
  }
};

/**
 * Obtiene la última lectura de sensores
 */
export const getLatestData = async (deviceId = null) => {
  try {
    const params = {};
    if (deviceId) params.deviceId = deviceId;
    
    const response = await api.get('/sensors/latest', { params });
    return response.data.data || null;
  } catch (error) {
    console.error('Error obteniendo última lectura:', error);
    return null;
  }
};

/**
 * Obtiene estadísticas de sensores
 */
export const getSensorStats = async (hours = 24, deviceId = null) => {
  try {
    const params = { hours };
    if (deviceId) params.deviceId = deviceId;
    
    const response = await api.get('/sensors/stats', { params });
    return response.data.stats || null;
  } catch (error) {
    console.error('Error obteniendo estadísticas:', error);
    return null;
  }
};

/**
 * Controla un actuador
 */
export const controlActuator = async (deviceId, actuator, state) => {
  try {
    const response = await api.post('/actuators/control', {
      deviceId,
      actuator,
      state
    });
    return response.data;
  } catch (error) {
    console.error('Error controlando actuador:', error);
    throw error;
  }
};

/**
 * Obtiene el estado de los actuadores
 */
export const getActuatorStatus = async () => {
  try {
    const response = await api.get('/actuators/status');
    return response.data.data || {};
  } catch (error) {
    console.error('Error obteniendo estado de actuadores:', error);
    return {};
  }
};

/**
 * Obtiene alertas activas
 */
export const getActiveAlerts = async (deviceId = null) => {
  try {
    const params = {};
    if (deviceId) params.deviceId = deviceId;
    
    const response = await api.get('/alerts', { params });
    return response.data.data || [];
  } catch (error) {
    console.error('Error obteniendo alertas:', error);
    return [];
  }
};

/**
 * Resuelve una alerta
 */
export const resolveAlert = async (alertId) => {
  try {
    const response = await api.post(`/alerts/${alertId}/resolve`);
    return response.data;
  } catch (error) {
    console.error('Error resolviendo alerta:', error);
    throw error;
  }
};

/**
 * Obtiene lista de dispositivos
 */
export const getDevices = async () => {
  try {
    const response = await api.get('/devices');
    return response.data.data || [];
  } catch (error) {
    console.error('Error obteniendo dispositivos:', error);
    return [];
  }
};

export default api;
