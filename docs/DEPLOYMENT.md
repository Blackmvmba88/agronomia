# Deployment Guide

This guide covers deploying Agronomia in various environments.

## Quick Start with Docker

The easiest way to deploy Agronomia:

```bash
# Clone repository
git clone https://github.com/Blackmvmba88/agronomia.git
cd agronomia

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001 (admin/agronomia)

## Production Deployment

### Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt)
- Min 2GB RAM, 20GB storage

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Clone and Configure

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/Blackmvmba88/agronomia.git
cd agronomia

# Create environment file
cp .env.example .env
nano .env
```

Edit `.env`:
```env
# Database
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://agronomia:your_secure_password_here@postgres:5432/agronomia

# MQTT
MQTT_USER=agronomia
MQTT_PASSWORD=mqtt_secure_password_here

# API
SECRET_KEY=generate_random_secret_key_here
API_HOST=api.yourdomain.com

# Frontend
FRONTEND_HOST=yourdomain.com
```

### Step 3: Configure SSL (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

### Step 4: Start Services

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f

# Verify all services running
docker-compose ps
```

### Step 5: Nginx Configuration

Create `/etc/nginx/sites-available/agronomia`:

```nginx
# API
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/agronomia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 1883/tcp  # MQTT (if external devices)
sudo ufw enable
```

### Step 7: Setup Monitoring

```bash
# Install monitoring tools
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
# http://yourdomain.com:3001
# Default: admin/agronomia
```

## Hardware Deployment

### ESP32 Configuration

1. Update firmware configuration:
```cpp
#define WIFI_SSID "your_wifi"
#define WIFI_PASSWORD "your_password"
#define MQTT_SERVER "yourdomain.com"
#define DEVICE_ID "ESP32-GREENHOUSE-1"
```

2. Flash firmware:
```bash
cd firmware/esp32
pio run --target upload
```

3. Monitor logs:
```bash
pio device monitor
```

## Backup and Recovery

### Database Backup

```bash
# Backup
docker exec agronomia-db pg_dump -U agronomia agronomia > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i agronomia-db psql -U agronomia agronomia < backup.sql
```

### Automated Backups

Create cron job:
```bash
crontab -e

# Daily backup at 2 AM
0 2 * * * /opt/agronomia/scripts/backup.sh
```

## Scaling

### Horizontal Scaling

For multiple instances:

```yaml
# docker-compose.scale.yml
services:
  api:
    deploy:
      replicas: 3
    
  nginx:
    image: nginx:alpine
    depends_on:
      - api
```

Run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d --scale api=3
```

### Load Balancing

Use Nginx for load balancing:

```nginx
upstream api_backend {
    least_conn;
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    location / {
        proxy_pass http://api_backend;
    }
}
```

## Monitoring and Maintenance

### Health Checks

```bash
# API health
curl http://localhost:8000/

# Database connection
docker exec agronomia-db psql -U agronomia -c "SELECT 1"

# MQTT broker
mosquitto_sub -h localhost -t '$SYS/#' -C 1
```

### Log Management

```bash
# View logs
docker-compose logs -f api
docker-compose logs -f mosquitto

# Rotate logs
docker-compose logs --tail=100 api > api_logs.txt
```

### Updates

```bash
# Pull latest changes
cd /opt/agronomia
git pull

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

## Troubleshooting

### Service won't start

```bash
# Check logs
docker-compose logs service_name

# Check resource usage
docker stats

# Restart specific service
docker-compose restart api
```

### Database connection issues

```bash
# Check database status
docker-compose ps postgres

# Test connection
docker exec agronomia-db psql -U agronomia -c "SELECT version()"
```

### MQTT not receiving data

```bash
# Test MQTT broker
mosquitto_sub -h localhost -t agronomia/# -v

# Check device connectivity
# Review firmware logs via serial monitor
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/TLS
- [ ] Configure firewall
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Monitor access logs
- [ ] Implement rate limiting
- [ ] Use strong authentication

## Performance Optimization

- Enable Redis caching
- Use PostgreSQL connection pooling
- Optimize database indexes
- CDN for frontend assets
- Compress API responses
- Monitor query performance

## Support

For deployment issues:
- GitHub Issues
- Documentation: docs/
- Community Forum

---

**Deployment checklist completed! Your Agronomia platform is ready for production use. 🚀**
