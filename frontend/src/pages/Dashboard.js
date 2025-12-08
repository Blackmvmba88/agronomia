import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Switch,
  FormControlLabel,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Opacity,
  Bolt,
  DeviceThermostat,
  Air,
  WbSunny,
  Water,
  Lightbulb
} from '@mui/icons-material';
import SensorChart from '../components/SensorChart';
import { getSensorHistory, getLatestData, controlActuator, getActiveAlerts } from '../services/api';

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [latestData, setLatestData] = useState(null);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [actuators, setActuators] = useState({
    pump: false,
    led: false
  });

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000); // Actualizar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [latest, hist, alertsData] = await Promise.all([
        getLatestData(),
        getSensorHistory(50),
        getActiveAlerts()
      ]);
      
      setLatestData(latest);
      setHistory(hist);
      setAlerts(alertsData);
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleActuatorToggle = async (actuator) => {
    try {
      const newState = !actuators[actuator];
      await controlActuator('ESP32-001', actuator, newState);
      setActuators(prev => ({
        ...prev,
        [actuator]: newState
      }));
    } catch (error) {
      console.error('Error controlando actuador:', error);
    }
  };

  if (loading && !latestData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" gutterBottom>
        🌱 BlackMamba Smart Farming
      </Typography>
      <Typography variant="subtitle1" gutterBottom color="text.secondary">
        Sistema de Monitoreo Hidropónico
      </Typography>

      {/* Alertas */}
      {alerts.length > 0 && (
        <Box sx={{ mb: 3 }}>
          {alerts.map((alert, index) => (
            <Alert severity={alert.severity === 'critical' ? 'error' : 'warning'} key={index} sx={{ mb: 1 }}>
              {alert.message}
            </Alert>
          ))}
        </Box>
      )}

      {/* Tarjetas de sensores actuales */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="pH"
            value={latestData?.pH?.toFixed(2)}
            unit=""
            icon={<Opacity />}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="EC"
            value={latestData?.ec?.toFixed(0)}
            unit="µS/cm"
            icon={<Bolt />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="Temp. Agua"
            value={latestData?.waterTemp?.toFixed(1)}
            unit="°C"
            icon={<Water />}
            color="#00bcd4"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="Temp. Ambiente"
            value={latestData?.airTemp?.toFixed(1)}
            unit="°C"
            icon={<DeviceThermostat />}
            color="#f44336"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="Humedad"
            value={latestData?.humidity?.toFixed(1)}
            unit="%"
            icon={<Air />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <SensorCard
            title="Luz"
            value={latestData?.lightLevel}
            unit="lux"
            icon={<WbSunny />}
            color="#ffeb3b"
          />
        </Grid>
      </Grid>

      {/* Gráficas de histórico */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>pH - Histórico</Typography>
            <SensorChart data={history} dataKey="pH" color="#2196f3" />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>EC - Histórico</Typography>
            <SensorChart data={history} dataKey="ec" color="#ff9800" />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Temperatura - Histórico</Typography>
            <SensorChart 
              data={history} 
              dataKey="waterTemp" 
              dataKey2="airTemp"
              color="#00bcd4"
              color2="#f44336"
              legend1="Agua"
              legend2="Ambiente"
            />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Humedad - Histórico</Typography>
            <SensorChart data={history} dataKey="humidity" color="#4caf50" />
          </Paper>
        </Grid>
      </Grid>

      {/* Control de actuadores */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Control de Actuadores
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box display="flex" alignItems="center">
                    <Water sx={{ mr: 1, fontSize: 40, color: '#2196f3' }} />
                    <Typography variant="h6">Bomba Recirculación</Typography>
                  </Box>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={actuators.pump}
                        onChange={() => handleActuatorToggle('pump')}
                        color="primary"
                      />
                    }
                    label={actuators.pump ? 'ON' : 'OFF'}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box display="flex" alignItems="center">
                    <Lightbulb sx={{ mr: 1, fontSize: 40, color: '#ffeb3b' }} />
                    <Typography variant="h6">Iluminación LED</Typography>
                  </Box>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={actuators.led}
                        onChange={() => handleActuatorToggle('led')}
                        color="primary"
                      />
                    }
                    label={actuators.led ? 'ON' : 'OFF'}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
}

function SensorCard({ title, value, unit, icon, color }) {
  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box sx={{ color, mr: 1 }}>
            {icon}
          </Box>
          <Typography variant="h6" component="div">
            {title}
          </Typography>
        </Box>
        <Typography variant="h3" component="div">
          {value || '--'}
          {value && <Typography variant="h6" component="span" sx={{ ml: 1 }}>{unit}</Typography>}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default Dashboard;
