# 🚀 Quick Start Guide - Web Applications

This guide will help you get the web applications running in minutes.

## Option 1: Landing Page (Recommended for First Time)

The easiest way to explore both dashboards:

```bash
cd frontend
# Open index.html in your browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows

# Or use a simple HTTP server:
python3 -m http.server 8080
# Then visit http://localhost:8080
```

This landing page lets you:
- ✅ Choose between Simple HTML Dashboard and React Dashboard
- ✅ See instructions for each option
- ✅ Get started without installation

---

## Option 2: Simple HTML Dashboard

**Perfect for quick demos and testing without installation**

### Start in 10 seconds:

```bash
cd frontend/web
# Open directly in browser
open index.html

# Or with a server:
python3 -m http.server 8080
# Visit http://localhost:8080
```

### Features:
- ✅ No installation required
- ✅ Real-time charts with Chart.js
- ✅ WebSocket support
- ✅ Demo mode included
- ✅ Works offline with demo data

### Configure Backend URL:
Edit `frontend/web/index.html` around line 500:
```javascript
const API_BASE_URL = 'http://localhost:3000/api';
```

---

## Option 3: React Dashboard

**Full-featured modern application with Material-UI**

### Quick Setup (1 minute):

```bash
cd frontend

# Automated setup
./setup-web.sh

# Or manual:
npm install
cp .env.example .env
npm start
```

The app will open at `http://localhost:3000`

### Features:
- ✅ Modern Material-UI interface
- ✅ Real-time sensor monitoring
- ✅ Actuator controls
- ✅ Alert system
- ✅ Responsive design
- ✅ Production-ready

### Configure:
Edit `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:3000/api
REACT_APP_DEVICE_ID=ESP32-001
```

---

## Backend Setup

Both dashboards need the backend API running:

```bash
cd backend/api
pip install -r requirements.txt
python main.py
```

The API will run at `http://localhost:3000`

### Without Real Hardware?
No problem! The dashboards have demo mode that generates fake data.

---

## Comparison

| Feature | Simple HTML | React App |
|---------|-------------|-----------|
| Installation | ❌ None | ✅ npm install |
| Load Time | ⚡ Instant | 🔄 ~3 seconds |
| Features | Basic | Advanced |
| Charts | Chart.js | Recharts |
| Actuators | ❌ View only | ✅ Control |
| Alerts | ⚠️ Basic | ✅ Advanced |
| Mobile | ✅ Yes | ✅ Yes |
| Offline | ✅ Demo mode | ❌ Needs API |
| Best For | Demos, Learning | Production |

---

## Troubleshooting

### Dashboard shows no data
1. Check backend is running: `curl http://localhost:3000/api/health`
2. Check browser console for errors (F12)
3. Enable demo mode (toggle in dashboard)

### React app won't start
1. Check Node.js version: `node --version` (need ≥16)
2. Delete node_modules and reinstall: `rm -rf node_modules && npm install`
3. Check for port conflicts: `lsof -i :3000`

### Backend connection error
1. Verify backend URL in `.env` or HTML file
2. Check CORS settings in backend
3. Verify firewall isn't blocking port 3000

---

## Next Steps

1. ✅ **Explore the dashboards** - Try both options
2. 📊 **View demo data** - See the interface with simulated data
3. 🔌 **Connect real hardware** - Follow `hardware/docs/SETUP.md`
4. 🤖 **Train AI models** - See `ai-ml/README.md`
5. 🚀 **Deploy to production** - Follow `docs/DEPLOYMENT.md`

---

## Need Help?

- 📖 Full documentation: `README.md`
- 🐛 Issues: https://github.com/Blackmvmba88/agronomia/issues
- 💬 Discussions: https://github.com/Blackmvmba88/agronomia/discussions

---

**Ready to grow smarter? 🌱**

Start with the landing page and choose your preferred dashboard!
