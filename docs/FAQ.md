# Frequently Asked Questions (FAQ)

## General Questions

### What is Agronomia?
Agronomia is an open-source autonomous hydroponic plant monitoring and optimization platform. It combines IoT sensors, cloud APIs, and AI/ML models to help farmers and researchers optimize plant growth.

### Who is it for?
- Hydroponic farmers (hobby and commercial)
- Agricultural researchers
- Educational institutions
- Indoor farming operations
- Anyone interested in precision agriculture

### Is it free?
Yes! Agronomia is open-source under the MIT License. You can use, modify, and distribute it freely.

### What languages/frameworks are used?
- Firmware: Arduino C++ (ESP32)
- Backend: Python (FastAPI)
- Frontend: HTML/CSS/JavaScript
- AI/ML: Python (TensorFlow, scikit-learn)
- Database: PostgreSQL, InfluxDB

## Hardware Questions

### What hardware do I need?
Minimum setup:
- ESP32 DevKit (~$5)
- pH sensor (~$50)
- DHT22 sensor (~$5)
- DS18B20 sensor (~$3)
- Light sensor (~$7)
- EC/TDS sensor (~$50)

Total: ~$120 for complete sensor suite

### Can I use Arduino instead of ESP32?
Yes, but you'll need an Ethernet or WiFi shield for connectivity. ESP32 is recommended because it has built-in WiFi and is cost-effective.

### Do I need a Raspberry Pi?
No, ESP32 is sufficient for most use cases. Raspberry Pi can be added later for advanced features like computer vision.

### Where can I buy sensors?
- Amazon
- AliExpress
- SparkFun
- Adafruit
- DFRobot
- Atlas Scientific (high-quality but pricier)

### How accurate are the sensors?
Typical accuracy:
- pH: ±0.1 pH
- Temperature: ±0.5°C
- Humidity: ±2% RH
- EC: ±2%
- Light: ±10%

Calibration improves accuracy significantly.

## Software Questions

### Do I need to know programming?
Basic setup requires minimal programming. Just edit configuration files. Advanced customization requires:
- Python (backend/AI)
- C++ (firmware)
- JavaScript (frontend)

### Can I run it on Windows?
Yes! Docker works on Windows 10/11 with WSL2. Alternatively, install Python and Node.js directly.

### What about Mac/Linux?
Fully supported on both macOS and Linux.

### Do I need a server?
For testing: No, run locally on your computer
For production: Yes, recommended to use a cloud server or dedicated machine

### Can multiple devices connect?
Yes! The system supports unlimited devices. Each device gets a unique ID.

### How is data stored?
- PostgreSQL: Device info, alerts, harvest records
- InfluxDB: Time-series sensor data (optional)
- SQLite: Lightweight alternative for testing

## Features Questions

### What sensors are supported?
Currently:
- pH
- Temperature (water and air)
- Humidity
- EC/TDS (nutrient concentration)
- Light intensity

Easily extensible for more sensors.

### What AI features are included?
1. **Irrigation Prediction**: When and how much to water
2. **Nutrient Optimization**: EC/pH adjustment recommendations
3. **Harvest Prediction**: Days to harvest and expected yield

### Can I control actuators (pumps, lights)?
Not in current version, but architecture supports it. You can add MQTT-controlled relays.

### Does it work offline?
Partially. ESP32 can log data locally to SD card, but real-time monitoring and AI predictions require internet connectivity.

### Can I access it remotely?
Yes, with proper network configuration:
- Port forwarding on router
- VPN access
- Cloud deployment

### Is there a mobile app?
Not yet, but the web dashboard is mobile-responsive. Native mobile apps are on the roadmap.

## Deployment Questions

### How do I deploy to production?
See [Deployment Guide](DEPLOYMENT.md) for detailed instructions. Recommended:
- Docker Compose for small-scale
- Kubernetes for large-scale
- Cloud providers: AWS, Azure, DigitalOcean, Heroku

### What are the hosting costs?
Approximate monthly costs:
- DigitalOcean Droplet (2GB): $12
- AWS t2.micro: ~$10
- Heroku Hobby: $7
- Self-hosted: $0 (just electricity)

### How much bandwidth does it use?
Per device:
- Sensor data: ~1 KB every 10 seconds
- Daily: ~8.6 MB
- Monthly: ~260 MB

Very low bandwidth requirements.

### What about security?
Built-in security features:
- HTTPS/TLS support
- JWT authentication
- Environment variable secrets
- SQL injection protection
- CORS configuration

See security best practices in documentation.

## AI/ML Questions

### Do I need to train models?
Pre-trained models are included. You can use them immediately or retrain with your own data.

### How accurate are the predictions?
- Irrigation: 92% accuracy
- Nutrients: 89% accuracy
- Harvest: ±3 days, ±15% yield

Improves with more training data from your system.

### Can I improve the models?
Yes! Collect data from your system and retrain:
```python
predictor.train(data=your_data, epochs=100)
```

### What data is needed for training?
- Sensor readings (temperature, humidity, light, etc.)
- Manual measurements (plant height, leaf count)
- Harvest records (date, yield)

Minimum: 30 days of data recommended

### Do predictions run locally?
Yes, after training. Models are loaded and run on your server. No external API calls needed.

## Plant-Specific Questions

### What plants are supported?
Currently optimized for:
- Lettuce
- Tomato
- Cucumber
- Pepper
- Herbs (basil, mint, etc.)

Can be adapted for any hydroponic crop.

### Can I grow multiple plant types?
Yes! Each device can be assigned a plant type. Different thresholds and recommendations per type.

### What about soil-based growing?
System is designed for hydroponics but can be adapted for soil with appropriate sensors (soil moisture, etc.)

### How does it handle different growth stages?
AI models consider growth stage:
- Seedling
- Vegetative
- Flowering
- Fruiting

Recommendations adjust automatically.

## Troubleshooting

### Sensors show incorrect readings
1. Check wiring
2. Verify calibration
3. Look for interference
4. Check power supply
5. Test sensors individually

### WiFi keeps disconnecting
1. Check signal strength
2. Move closer to router
3. Use WiFi repeater
4. Check 2.4GHz band (ESP32 requirement)
5. Verify router settings

### Dashboard not updating
1. Check MQTT broker status
2. Verify device connectivity
3. Check API logs
4. Clear browser cache
5. Check WebSocket connection

### Database errors
1. Verify connection string
2. Check database is running
3. Run migrations
4. Check disk space
5. Review logs

### AI predictions seem wrong
1. Check input data quality
2. Verify sensor calibration
3. Retrain with more data
4. Check model version
5. Validate against manual observations

## Contributing

### How can I contribute?
- Report bugs
- Suggest features
- Submit code improvements
- Improve documentation
- Share your success stories
- Help other users

See [CONTRIBUTING.md](../CONTRIBUTING.md)

### I found a bug. What should I do?
1. Check if already reported in Issues
2. Gather information (logs, screenshots, steps to reproduce)
3. Create a new GitHub Issue
4. Be as detailed as possible

### Can I add new sensors?
Yes! Follow these steps:
1. Update firmware to read new sensor
2. Add fields to database schema
3. Update API endpoints
4. Add to dashboard display
5. Submit pull request

### How do I get help?
- Read documentation
- Search existing Issues
- Ask in GitHub Discussions
- Create new Issue with "question" label

## Future Plans

### What's on the roadmap?
- [ ] Mobile apps (iOS/Android)
- [ ] Computer vision for plant health
- [ ] Automated actuator control
- [ ] Multi-site management
- [ ] Voice assistant integration
- [ ] Marketplace features
- [ ] More AI models

### When will feature X be released?
Check GitHub Projects and Milestones for timeline. Contributions welcome to speed up development!

### Can I request a feature?
Absolutely! Create a Feature Request issue on GitHub.

## Commercial Use

### Can I use this commercially?
Yes! MIT License allows commercial use. No restrictions.

### Can I sell products based on this?
Yes! You can build commercial products, consultancies, or services using Agronomia.

### Do I need to credit Agronomia?
While not required by license, attribution is appreciated:
```
Built with Agronomia - https://github.com/Blackmvmba88/agronomia
```

### Can I offer paid support?
Yes! Many open-source projects have commercial support offerings.

## Data and Privacy

### What data is collected?
Only sensor readings and system metrics. No personal information unless you add user accounts.

### Is my data private?
Yes, it's stored on your own server. We don't collect or transmit data anywhere.

### Can I export my data?
Yes! Data can be exported as CSV or JSON through the API:
```bash
curl http://localhost:8000/api/sensors/history/DEVICE_ID > export.json
```

### GDPR compliance?
If you collect user data, you're responsible for GDPR compliance. Core system doesn't collect personal data.

## Support

### Where can I get help?
1. Read documentation (docs/)
2. Check FAQ (this file)
3. Search GitHub Issues
4. Create new Issue
5. GitHub Discussions

### Is there paid support?
Not officially, but community members may offer consulting services.

### How do I report security issues?
Email security concerns to: [create a SECURITY.md file for proper disclosure]

---

**Still have questions? Create an issue or discussion on GitHub!**
