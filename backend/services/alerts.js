/**
 * Servicio de alertas
 * 
 * Evalúa datos de sensores y genera alertas cuando los valores
 * están fuera de rango
 */

const { saveAlert } = require('./database');

// Configuración de rangos desde variables de entorno
const RANGES = {
  pH: {
    min: parseFloat(process.env.ALERT_PH_MIN) || 5.5,
    max: parseFloat(process.env.ALERT_PH_MAX) || 6.5
  },
  ec: {
    min: parseFloat(process.env.ALERT_EC_MIN) || 800,
    max: parseFloat(process.env.ALERT_EC_MAX) || 1500
  },
  waterTemp: {
    min: parseFloat(process.env.ALERT_WATER_TEMP_MIN) || 18,
    max: parseFloat(process.env.ALERT_WATER_TEMP_MAX) || 24
  },
  airTemp: {
    min: parseFloat(process.env.ALERT_AIR_TEMP_MIN) || 18,
    max: parseFloat(process.env.ALERT_AIR_TEMP_MAX) || 28
  },
  humidity: {
    min: parseFloat(process.env.ALERT_HUMIDITY_MIN) || 50,
    max: parseFloat(process.env.ALERT_HUMIDITY_MAX) || 70
  }
};

/**
 * Evalúa datos de sensores y genera alertas si es necesario
 */
async function evaluateSensorData(data) {
  const alerts = [];

  // Evaluar pH
  if (data.pH < RANGES.pH.min) {
    alerts.push(await createAlert(data.deviceId, 'pH', 'bajo', data.pH, RANGES.pH.min));
  } else if (data.pH > RANGES.pH.max) {
    alerts.push(await createAlert(data.deviceId, 'pH', 'alto', data.pH, RANGES.pH.max));
  }

  // Evaluar EC
  if (data.ec < RANGES.ec.min) {
    alerts.push(await createAlert(data.deviceId, 'EC', 'baja', data.ec, RANGES.ec.min));
  } else if (data.ec > RANGES.ec.max) {
    alerts.push(await createAlert(data.deviceId, 'EC', 'alta', data.ec, RANGES.ec.max));
  }

  // Evaluar temperatura del agua
  if (data.waterTemp < RANGES.waterTemp.min) {
    alerts.push(await createAlert(data.deviceId, 'Temperatura del agua', 'baja', data.waterTemp, RANGES.waterTemp.min));
  } else if (data.waterTemp > RANGES.waterTemp.max) {
    alerts.push(await createAlert(data.deviceId, 'Temperatura del agua', 'alta', data.waterTemp, RANGES.waterTemp.max));
  }

  // Evaluar temperatura del aire
  if (data.airTemp < RANGES.airTemp.min) {
    alerts.push(await createAlert(data.deviceId, 'Temperatura del aire', 'baja', data.airTemp, RANGES.airTemp.min));
  } else if (data.airTemp > RANGES.airTemp.max) {
    alerts.push(await createAlert(data.deviceId, 'Temperatura del aire', 'alta', data.airTemp, RANGES.airTemp.max));
  }

  // Evaluar humedad
  if (data.humidity < RANGES.humidity.min) {
    alerts.push(await createAlert(data.deviceId, 'Humedad', 'baja', data.humidity, RANGES.humidity.min));
  } else if (data.humidity > RANGES.humidity.max) {
    alerts.push(await createAlert(data.deviceId, 'Humedad', 'alta', data.humidity, RANGES.humidity.max));
  }

  return alerts;
}

/**
 * Crea una alerta
 */
async function createAlert(deviceId, parameter, condition, value, threshold) {
  const alertData = {
    deviceId,
    parameter,
    condition,
    value,
    threshold,
    message: `${parameter} ${condition}: ${value} (umbral: ${threshold})`,
    severity: getSeverity(parameter, condition, value, threshold),
    timestamp: Date.now()
  };

  try {
    const alert = await saveAlert(alertData);
    console.log(`⚠️  Alerta generada: ${alertData.message}`);
    return alert;
  } catch (error) {
    console.error('Error creando alerta:', error);
    return null;
  }
}

/**
 * Determina la severidad de una alerta
 */
function getSeverity(parameter, condition, value, threshold) {
  const diff = Math.abs(value - threshold);
  const percentDiff = (diff / threshold) * 100;

  if (percentDiff > 20) {
    return 'critical';
  } else if (percentDiff > 10) {
    return 'high';
  } else {
    return 'medium';
  }
}

module.exports = {
  evaluateSensorData,
  RANGES
};
