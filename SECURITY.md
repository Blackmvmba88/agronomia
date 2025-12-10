# Security Policy for Agronomia

## 🔒 Security Best Practices

This document outlines security recommendations for deploying and maintaining the Agronomia platform in production environments.

---

## 1. Authentication & Authorization

### API Security
- **Use JWT tokens** with short expiration times (15-60 minutes)
- **Implement refresh tokens** for seamless user experience
- **Enable API key authentication** for device-to-API communication
- **Rotate API keys** every 90 days minimum

```python
# Example: API key rotation
from datetime import datetime, timedelta

def should_rotate_key(last_rotation_date):
    days_since_rotation = (datetime.now() - last_rotation_date).days
    return days_since_rotation >= 90
```

### User Management
- **Role-Based Access Control (RBAC)**
  - `admin`: Full system access
  - `farmer`: Manage devices and view data
  - `viewer`: Read-only access
  - `device`: Limited scope for IoT devices

- **Multi-Factor Authentication (MFA)** for admin accounts
- **Strong password requirements**:
  - Minimum 12 characters
  - Mix of uppercase, lowercase, numbers, symbols
  - Password history (prevent reuse of last 5 passwords)

---

## 2. Data Security

### Encryption at Rest
- **Database encryption**: Use PostgreSQL native encryption or AWS RDS encryption
- **Backup encryption**: Encrypt all database backups
- **File storage**: Encrypt sensitive files (user data, credentials)

```bash
# Example: PostgreSQL encryption setup
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';
```

### Encryption in Transit
- **TLS/SSL for all connections**:
  - HTTPS for web traffic (minimum TLS 1.2)
  - MQTTS for MQTT traffic
  - SSL for database connections

```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### Data Anonymization
- **Remove PII** when sharing datasets
- **Hash device IDs** in public analytics
- **Aggregate data** for reporting

---

## 3. MQTT Security

### Broker Configuration
- **Enable authentication**: Username/password or certificate-based
- **Use TLS/SSL**: Enable MQTTS on port 8883
- **Access Control Lists (ACLs)**: Restrict topics per user

```conf
# Mosquitto ACL example
user device_001
topic write agronomia/devices/device_001/#
topic read agronomia/devices/device_001/control/#

user backend_service
topic readwrite agronomia/#
```

### Device Security
- **Unique credentials** per device
- **Certificate-based authentication** for production
- **Device provisioning workflow**:
  1. Generate unique device ID
  2. Create certificate/credentials
  3. Securely transfer to device (QR code, secure channel)
  4. Device authenticates and registers

---

## 4. Network Security

### Firewall Rules
```bash
# UFW firewall configuration
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp      # SSH (restrict to specific IPs in production)
sudo ufw allow 80/tcp      # HTTP (redirect to HTTPS)
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8883/tcp    # MQTTS
sudo ufw enable
```

### VPN for Remote Access
- **Use VPN** for accessing production systems remotely
- **Disable direct SSH access** from public internet
- **Bastion host** for administrative access

### DDoS Protection
- **Rate limiting** on API endpoints
- **CloudFlare** or AWS WAF for web traffic
- **Connection limits** on MQTT broker

---

## 5. Secrets Management

### Environment Variables
- **Never commit secrets** to version control
- **Use .env files** for development (excluded in .gitignore)
- **Use secret managers** for production:
  - AWS Secrets Manager
  - HashiCorp Vault
  - Kubernetes Secrets

```bash
# Example: .env file structure
DB_PASSWORD=<strong-random-password>
JWT_SECRET=<long-random-string>
MQTT_PASSWORD=<unique-per-env>
API_KEY=<rotated-regularly>
```

### Credential Rotation
- **Automated rotation** every 90 days
- **Zero-downtime rotation**:
  1. Generate new credentials
  2. Deploy with dual support (old + new)
  3. Update clients to use new credentials
  4. Deprecate old credentials

---

## 6. Application Security

### Input Validation
- **Validate all user inputs** (API, forms, MQTT messages)
- **Sanitize data** before database insertion
- **Use parameterized queries** to prevent SQL injection

```python
# Good: Parameterized query
cursor.execute("SELECT * FROM sensors WHERE device_id = %s", (device_id,))

# Bad: String concatenation (SQL injection risk)
cursor.execute(f"SELECT * FROM sensors WHERE device_id = '{device_id}'")
```

### Dependency Management
- **Keep dependencies updated**: Use `pip-audit`, `npm audit`
- **Vulnerability scanning**: GitHub Dependabot, Snyk
- **Pin versions** in production

```bash
# Scan for vulnerabilities
pip-audit
npm audit

# Update dependencies safely
pip install --upgrade package-name
npm update
```

### Error Handling
- **Don't expose stack traces** in production
- **Log errors securely** (no sensitive data in logs)
- **Rate limit error responses** to prevent enumeration attacks

---

## 7. Monitoring & Auditing

### Security Logging
- **Log all authentication attempts** (success and failure)
- **Track API access** with user IDs and timestamps
- **Monitor for suspicious activity**:
  - Multiple failed login attempts
  - Unusual data access patterns
  - Unexpected API calls

### Alerting
```yaml
# Example: Alert rules
alerts:
  - name: "Multiple Failed Logins"
    condition: "failed_logins > 5 in 5 minutes"
    action: "Lock account, notify admin"
  
  - name: "Unusual Data Export"
    condition: "data_export_size > 10GB"
    action: "Require admin approval"
```

### Regular Audits
- **Quarterly security reviews**
- **Penetration testing** annually
- **Code security audits** for major releases

---

## 8. Backup & Recovery

### Backup Strategy
- **Automated daily backups** of database
- **Test restore procedures** monthly
- **Offsite backup storage** (different region/cloud provider)
- **Retention policy**: 30 days daily, 12 months monthly

### Disaster Recovery
- **Recovery Time Objective (RTO)**: < 4 hours
- **Recovery Point Objective (RPO)**: < 24 hours
- **Documented recovery procedures**
- **Regular disaster recovery drills**

---

## 9. Compliance

### GDPR Compliance (if applicable)
- **Data minimization**: Collect only necessary data
- **Right to erasure**: Implement data deletion workflows
- **Data portability**: Export user data on request
- **Privacy policy**: Clear documentation of data usage

### Industry Standards
- **ISO 27001**: Information security management
- **NIST Cybersecurity Framework**: Risk management
- **OWASP Top 10**: Web application security

---

## 10. Incident Response

### Response Plan
1. **Detect**: Monitor alerts and logs
2. **Contain**: Isolate affected systems
3. **Investigate**: Determine scope and cause
4. **Remediate**: Fix vulnerability, restore services
5. **Document**: Post-mortem and lessons learned

### Contact Information
- **Security Team**: security@agronomia.example.com
- **On-call Engineer**: Use PagerDuty/OpsGenie
- **Emergency Contacts**: Maintain updated list

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** open a public GitHub issue
2. **Email** security@agronomia.example.com with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Allow time** for us to address the issue before public disclosure

We aim to respond within 48 hours and provide a fix within 30 days.

---

## Security Checklist for Production Deployment

- [ ] All credentials stored securely (not in code)
- [ ] TLS/SSL enabled for all connections
- [ ] Authentication and authorization configured
- [ ] Firewall rules configured
- [ ] Rate limiting enabled
- [ ] Logging and monitoring configured
- [ ] Automated backups configured and tested
- [ ] Dependencies up to date and scanned
- [ ] Security headers configured (HSTS, CSP, etc.)
- [ ] MQTT broker secured with ACLs
- [ ] Database access restricted to application only
- [ ] Admin interfaces protected (MFA, IP whitelist)
- [ ] Incident response plan documented
- [ ] Security training completed for team

---

## Additional Resources

- [OWASP IoT Security](https://owasp.org/www-project-internet-of-things/)
- [NIST IoT Security](https://www.nist.gov/itl/applied-cybersecurity/nist-cybersecurity-iot-program)
- [CIS Controls](https://www.cisecurity.org/controls)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)

---

**Security is everyone's responsibility. Stay vigilant! 🔒**

*Last Updated: 2024-12-10*
