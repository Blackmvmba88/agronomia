/**
 * Servicio de base de datos - Firestore
 * 
 * Maneja la conexión y operaciones con Firebase Firestore
 */

const admin = require('firebase-admin');

let db;

/**
 * Inicializa la conexión con Firebase
 */
function initializeFirebase() {
  try {
    // Inicializar Firebase Admin
    if (process.env.FIREBASE_PROJECT_ID) {
      const serviceAccount = {
        projectId: process.env.FIREBASE_PROJECT_ID,
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
        privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n')
      };

      admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
      });

      db = admin.firestore();
      console.log('✅ Firebase Firestore inicializado');
    } else {
      console.warn('⚠️  Firebase no configurado. Usando modo local.');
      // En desarrollo sin Firebase, usar datos en memoria
      db = null;
    }
  } catch (error) {
    console.error('❌ Error inicializando Firebase:', error.message);
    db = null;
  }
}

/**
 * Guarda datos de sensores
 */
async function saveSensorData(data) {
  if (!db) {
    console.log('Modo local: Datos recibidos', data);
    return { id: Date.now().toString(), ...data };
  }

  try {
    const docRef = await db.collection('sensorData').add({
      ...data,
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    console.log('Datos guardados con ID:', docRef.id);
    return { id: docRef.id, ...data };
  } catch (error) {
    console.error('Error guardando datos:', error);
    throw error;
  }
}

/**
 * Obtiene histórico de datos de sensores
 */
async function getSensorHistory(deviceId, limit = 100) {
  if (!db) {
    return [];
  }

  try {
    let query = db.collection('sensorData')
      .orderBy('createdAt', 'desc')
      .limit(limit);

    if (deviceId) {
      query = query.where('deviceId', '==', deviceId);
    }

    const snapshot = await query.get();
    const data = [];
    
    snapshot.forEach(doc => {
      data.push({
        id: doc.id,
        ...doc.data()
      });
    });

    return data;
  } catch (error) {
    console.error('Error obteniendo histórico:', error);
    throw error;
  }
}

/**
 * Guarda una alerta
 */
async function saveAlert(alertData) {
  if (!db) {
    console.log('Modo local: Alerta generada', alertData);
    return { id: Date.now().toString(), ...alertData };
  }

  try {
    const docRef = await db.collection('alerts').add({
      ...alertData,
      createdAt: admin.firestore.FieldValue.serverTimestamp(),
      resolved: false
    });
    
    return { id: docRef.id, ...alertData };
  } catch (error) {
    console.error('Error guardando alerta:', error);
    throw error;
  }
}

/**
 * Obtiene alertas activas
 */
async function getActiveAlerts(deviceId) {
  if (!db) {
    return [];
  }

  try {
    let query = db.collection('alerts')
      .where('resolved', '==', false)
      .orderBy('createdAt', 'desc');

    if (deviceId) {
      query = query.where('deviceId', '==', deviceId);
    }

    const snapshot = await query.get();
    const alerts = [];
    
    snapshot.forEach(doc => {
      alerts.push({
        id: doc.id,
        ...doc.data()
      });
    });

    return alerts;
  } catch (error) {
    console.error('Error obteniendo alertas:', error);
    throw error;
  }
}

/**
 * Marca una alerta como resuelta
 */
async function resolveAlert(alertId) {
  if (!db) {
    return { success: true };
  }

  try {
    await db.collection('alerts').doc(alertId).update({
      resolved: true,
      resolvedAt: admin.firestore.FieldValue.serverTimestamp()
    });
    
    return { success: true };
  } catch (error) {
    console.error('Error resolviendo alerta:', error);
    throw error;
  }
}

/**
 * Guarda estado de actuador
 */
async function saveActuatorState(deviceId, actuator, state) {
  if (!db) {
    console.log('Modo local: Estado de actuador', { deviceId, actuator, state });
    return { deviceId, actuator, state };
  }

  try {
    const docRef = await db.collection('actuatorStates').add({
      deviceId,
      actuator,
      state,
      timestamp: admin.firestore.FieldValue.serverTimestamp()
    });
    
    return { id: docRef.id, deviceId, actuator, state };
  } catch (error) {
    console.error('Error guardando estado de actuador:', error);
    throw error;
  }
}

module.exports = {
  initializeFirebase,
  saveSensorData,
  getSensorHistory,
  saveAlert,
  getActiveAlerts,
  resolveAlert,
  saveActuatorState
};
