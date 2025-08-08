# Shop VIP Premium - Deployment Instructions

## 🚀 One-Click VPS Deployment

This repository contains everything needed to deploy the complete Shop VIP Premium e-commerce platform on a fresh Ubuntu VPS.

### Prerequisites
- Fresh Ubuntu 20.04/22.04 VPS 
- Domain name pointing to your VPS IP address
- SSH access to your VPS as root

### Deployment Steps

1. **Connect to your VPS**
   ```bash
   ssh root@your-vps-ip
   ```

2. **Download and run the deployment script**
   ```bash
   wget https://raw.githubusercontent.com/yourusername/shopvippremium/main/master-deploy.sh
   chmod +x master-deploy.sh
   sudo bash master-deploy.sh
   ```

3. **Wait for deployment to complete** (15-20 minutes)
   - The script will automatically install all dependencies
   - Configure SSL certificates with Let's Encrypt
   - Set up the database with all products
   - Configure Nginx, PM2, and security settings

### What Gets Installed

#### System Dependencies
- ✅ Node.js 20.x LTS
- ✅ Python 3.11
- ✅ MongoDB 7.0
- ✅ Nginx
- ✅ PM2 Process Manager
- ✅ UFW Firewall
- ✅ SSL Certificates (Let's Encrypt)

#### Application Components
- ✅ FastAPI Backend with NOWPayments integration
- ✅ React Frontend with modern UI
- ✅ Complete product catalog (99+ products)
- ✅ Admin panel with full management features
- ✅ User authentication system
- ✅ Dual currency support (USD/INR)
- ✅ Crypto payment processing

### Post-Deployment Access

#### Website URLs
- **Frontend**: https://shopvippremium.com
- **Admin Panel**: https://shopvippremium.com/admin

#### Admin Credentials
- **Username**: `admin`
- **Password**: `VIP@dm1n2025!`

#### Database Configuration
- **Database Name**: `shopvippremium_db`
- **Connection**: `mongodb://localhost:27017`

### Useful Commands

#### Check Service Status
```bash
# Check all services
sudo systemctl status nginx mongod
pm2 status

# View backend logs
pm2 logs shopvippremium-backend

# Check SSL certificate
sudo certbot certificates
```

#### Restart Services
```bash
# Restart web services
sudo systemctl restart nginx
pm2 restart shopvippremium-backend

# Restart database
sudo systemctl restart mongod
```

#### View Logs
```bash
# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Backend logs
pm2 logs shopvippremium-backend --lines 100

# MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log
```

### Security Features

#### Firewall Configuration
- ✅ SSH (Port 22)
- ✅ HTTP (Port 80) 
- ✅ HTTPS (Port 443)
- ❌ All other ports blocked

#### SSL Security
- ✅ Let's Encrypt SSL certificates
- ✅ Automatic renewal via cron job
- ✅ HTTPS redirect enabled
- ✅ Modern TLS configuration

#### Application Security
- ✅ JWT authentication
- ✅ bcrypt password hashing
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Security headers

### Troubleshooting

#### If SSL setup fails:
```bash
# Manual SSL setup
sudo certbot --nginx -d shopvippremium.com -d www.shopvippremium.com
```

#### If backend doesn't start:
```bash
# Check backend logs
pm2 logs shopvippremium-backend

# Restart backend
pm2 restart shopvippremium-backend

# Check Python environment
cd /var/www/shopvippremium/backend
source venv/bin/activate
python --version
```

#### If database is empty:
```bash
# Manually run database seeder
cd /var/www/shopvippremium/backend
source venv/bin/activate
python mega_product_seeder.py
```

#### If domain doesn't resolve:
1. Check DNS settings point to your VPS IP
2. Wait for DNS propagation (up to 24 hours)
3. Test with IP address temporarily

### Performance Optimization

The deployment script includes several performance optimizations:

- **Nginx**: Gzip compression, caching headers, connection optimization
- **MongoDB**: Connection pooling, operation profiling
- **PM2**: Process clustering, auto-restart, memory management
- **Frontend**: Production build with asset optimization

### Backup Recommendations

#### Database Backup
```bash
# Create daily backup
mongodump --db shopvippremium_db --out /backup/$(date +%Y-%m-%d)

# Restore from backup
mongorestore --db shopvippremium_db /backup/2024-01-01/shopvippremium_db
```

#### File Backup
```bash
# Backup entire project
tar -czf /backup/shopvippremium-$(date +%Y-%m-%d).tar.gz /var/www/shopvippremium
```

### Update Process

#### Update Application Code
```bash
# Pull latest code
cd /var/www/shopvippremium
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
pm2 restart shopvippremium-backend

# Update frontend
cd ../frontend
yarn install
yarn build
sudo systemctl reload nginx
```

### Support

For technical support, contact:
- **Telegram**: [@shopvippremium](https://t.me/shopvippremium)
- **Email**: admin@shopvippremium.com

### License

This deployment package includes all necessary components for the Shop VIP Premium e-commerce platform. All NOWPayments API keys are pre-configured for immediate use.