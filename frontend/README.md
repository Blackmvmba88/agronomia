# Frontend - BlackMamba Smart Farming

Aplicaciones web para visualización y control del sistema hidropónico.

## 🎯 Dos Opciones de Dashboard

Este proyecto incluye **dos dashboards** para adaptarse a diferentes necesidades:

### 📊 Dashboard Simple (HTML/JS)
- **Ubicación**: `web/index.html`
- **Sin instalación**: Abrir directamente en el navegador
- **Características**: Gráficos en tiempo real, WebSocket, Chart.js
- **Ideal para**: Pruebas rápidas, demos, aprendizaje

### ⚛️ Dashboard React (Aplicación Moderna)
- **Ubicación**: `src/`
- **Requiere instalación**: npm install
- **Características**: Material-UI, control de actuadores, alertas
- **Ideal para**: Producción, uso avanzado

## 🚀 Inicio Rápido

### Opción 1: Abrir landing page
```bash
# Abrir index.html en el navegador desde el directorio frontend
open index.html
# o con un servidor simple:
python3 -m http.server 8080
# Luego visita http://localhost:8080
```

### Opción 2: Script automático (Dashboard React)
```bash
./setup-web.sh
```

### Opción 3: Manual (Dashboard React)
```bash
npm install
cp .env.example .env
# Editar .env si es necesario
npm start
```

## 📋 Requisitos

### Dashboard Simple (web/index.html)
- ✅ Navegador web moderno
- ✅ Sin dependencias

### Dashboard React (src/)
- Node.js >= 16.0.0
- npm o yarn
- Backend API corriendo

## 🔧 Instalación Detallada

1. Instalar dependencias (solo para React app):
```bash
npm install
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
```

3. Editar `.env`:
```env
REACT_APP_API_URL=http://localhost:3000/api
REACT_APP_DEVICE_ID=ESP32-001
```

## 🏃 Ejecutar

### Dashboard Simple
```bash
# Opción 1: Abrir directamente
open web/index.html

# Opción 2: Con servidor Python
python3 -m http.server 8080 --directory web
# Visita http://localhost:8080

# Opción 3: Con servidor Node
npx http-server web -p 8080
```

### Dashboard React

#### Modo desarrollo
```bash
npm start
```

La aplicación se abrirá en `http://localhost:3000`

#### Compilar para producción
```bash
npm run build
```

Los archivos compilados estarán en la carpeta `build/`

## 📱 Características del Dashboard

### Tarjetas de Sensores
- **pH**: Acidez/alcalinidad del agua
- **EC**: Conductividad eléctrica (nutrientes)
- **Temperatura del agua**: Control de temperatura de la solución
- **Temperatura ambiente**: Temperatura del aire
- **Humedad**: Humedad relativa del aire
- **Luz**: Nivel de luminosidad

### Gráficas Históricas
- Visualización de tendencias en tiempo real
- Hasta 50 puntos de datos recientes
- Actualización automática cada 30 segundos
- Múltiples series en una misma gráfica

### Control de Actuadores
- **Bomba de Recirculación**: Encender/apagar bomba de agua
- **Iluminación LED**: Controlar luces de crecimiento
- Switches interactivos con feedback visual
- Estado sincronizado con el backend

### Sistema de Alertas
- Notificaciones visuales cuando los valores están fuera de rango
- Diferentes niveles de severidad (warning, error)
- Alertas en tiempo real

## 🎨 Tecnologías

- **React 18**: Framework principal
- **Material-UI**: Componentes UI
- **Recharts**: Gráficas y visualizaciones
- **Axios**: Cliente HTTP
- **React Router**: Navegación

## 📊 Estructura del Proyecto

```
frontend/
├── public/              # Archivos estáticos
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/      # Componentes reutilizables
│   │   └── SensorChart.js
│   ├── pages/          # Páginas principales
│   │   └── Dashboard.js
│   ├── services/       # Servicios API
│   │   └── api.js
│   ├── App.js          # Componente principal
│   ├── index.js        # Punto de entrada
│   └── index.css       # Estilos globales
└── package.json
```

## 🔄 Flujo de Datos

1. **Componente Dashboard** se monta y solicita datos al backend
2. **Servicio API** hace peticiones HTTP al backend
3. Los datos se actualizan en el estado del componente
4. Los componentes hijos (tarjetas, gráficas) se renderizan con los nuevos datos
5. Actualización automática cada 30 segundos

## 🎨 Personalización

### Cambiar colores del tema
Editar `src/App.js`:
```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#4caf50', // Verde
    },
    secondary: {
      main: '#2196f3', // Azul
    },
  },
});
```

### Cambiar intervalo de actualización
Editar `src/pages/Dashboard.js`:
```javascript
const interval = setInterval(loadData, 30000); // Cambiar 30000 ms
```

### Agregar nuevos sensores
1. Agregar tarjeta en `Dashboard.js`
2. Agregar gráfica correspondiente
3. Actualizar servicio API si es necesario

## 🐛 Troubleshooting

### Error de conexión con el backend
- Verificar que el backend esté corriendo
- Verificar `REACT_APP_API_URL` en `.env`
- Verificar configuración de CORS en el backend

### Las gráficas no se muestran
- Verificar que haya datos en el backend
- Abrir la consola del navegador para ver errores
- Verificar formato de datos retornados por el API

### Los actuadores no responden
- Verificar conexión con el backend
- Verificar que el ESP32 esté conectado y recibiendo comandos
- Revisar logs del backend

## 🚢 Deployment

### Netlify
```bash
npm run build
# Subir carpeta build/ a Netlify
```

### Vercel
```bash
npm install -g vercel
vercel
```

### Servidor tradicional (Nginx)
```bash
npm run build
# Copiar build/ a /var/www/html
```

Configuración Nginx:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:3000;
    }
}
```

## 📱 Versión Móvil

Este dashboard es responsivo y funciona en dispositivos móviles. Para una aplicación nativa, considerar:
- React Native (compartir lógica de negocio)
- PWA (agregar service worker para funcionalidad offline)

## 🔐 Seguridad

- No exponer claves de API en el código
- Usar variables de entorno para configuración
- Implementar autenticación (próximamente)
- HTTPS en producción

## 📝 Roadmap

- [ ] Autenticación de usuarios
- [ ] Múltiples dispositivos
- [ ] Notificaciones push
- [ ] Modo oscuro
- [ ] Exportar datos a CSV/PDF
- [ ] Configuración de umbrales desde UI
- [ ] Historial de actuaciones
- [ ] Modo offline con Service Worker

## 📄 Licencia

MIT
