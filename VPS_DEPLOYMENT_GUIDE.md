# Shop VIP Premium - VPS Deployment Guide

## Server Details
- **Host**: 31.97.65.193
- **Username**: root
- **Password**: @FlashRocks23xshop

## Step-by-Step Deployment Process

### Phase 1: Initial Server Setup

```bash
# 1. Connect to your VPS
ssh root@31.97.65.193
# Enter password: @FlashRocks23xshop

# 2. Update system
apt update && apt upgrade -y

# 3. Install essential packages
apt install -y curl wget git nginx software-properties-common

# 4. Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# 5. Install Python 3.11 and pip
apt install -y python3.11 python3.11-venv python3-pip

# 6. Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org

# 7. Start and enable services
systemctl start mongod
systemctl enable mongod
systemctl start nginx
systemctl enable nginx

# 8. Install PM2 globally
npm install -g pm2
```

### Phase 2: Create Application Directory

```bash
# 1. Create app directory
mkdir -p /var/www/shopvippremium
cd /var/www/shopvippremium

# 2. Initialize git (we'll transfer files)
git init
```

### Phase 3: Transfer Application Files

**From your local environment, create a deployment package:**

```bash
# Run this on your LOCAL machine (not VPS)
cd /app
tar -czf shopvippremium-deploy.tar.gz \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='*.log' \
  backend/ frontend/ package.json
```

**Transfer to VPS (multiple options):**

**Option A: SCP Transfer**
```bash
# From your local machine
scp shopvippremium-deploy.tar.gz root@31.97.65.193:/var/www/shopvippremium/
```

**Option B: Direct file creation (I'll help you with this)**

### Phase 4: Backend Setup

```bash
# On VPS - Extract files (if using tar)
cd /var/www/shopvippremium
tar -xzf shopvippremium-deploy.tar.gz

# Setup Python virtual environment
cd /var/www/shopvippremium/backend
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create production .env file
cat > .env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="shopvippremium_prod"

# Nowpayments API Configuration
NOWPAYMENTS_IPN_SECRET="CRKTwqWfAbLGLeWdrsGZ4ZMES0DtTdD3"
NOWPAYMENTS_PRIVATE_KEY="S8QWJ1C-SDZ4WRE-QKZBRSJ-HJ9SQ7C"
NOWPAYMENTS_PUBLIC_KEY="66f018a4-4c91-4fdf-b8a0-275d63bc3d97"

# Production URLs (will be updated after domain setup)
BACKEND_URL="http://31.97.65.193:8001"
FRONTEND_URL="http://31.97.65.193:3000"
EOF
```

### Phase 5: Frontend Setup

```bash
# Setup frontend
cd /var/www/shopvippremium/frontend

# Install dependencies
npm install
# or
yarn install

# Create production .env
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://31.97.65.193:8001
EOF

# Build for production
npm run build
# or 
yarn build
```

### Phase 6: Nginx Configuration

```bash
# Create Nginx configuration
cat > /etc/nginx/sites-available/shopvippremium << 'EOF'
server {
    listen 80;
    server_name 31.97.65.193;
    
    # Frontend (React build)
    location / {
        root /var/www/shopvippremium/frontend/build;
        try_files $uri $uri/ /index.html;
        
        # Add security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /var/www/shopvippremium/frontend/build;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the site
ln -s /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx
```

### Phase 7: PM2 Process Management

```bash
# Create PM2 ecosystem file
cd /var/www/shopvippremium
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'shopvippremium-backend',
      script: 'venv/bin/python',
      args: '-m uvicorn server:app --host 0.0.0.0 --port 8001 --workers 2',
      cwd: '/var/www/shopvippremium/backend',
      env: {
        NODE_ENV: 'production'
      },
      instances: 1,
      exec_mode: 'fork',
      watch: false,
      autorestart: true,
      max_memory_restart: '1G',
      error_file: '/var/log/pm2/shopvippremium-backend-error.log',
      out_file: '/var/log/pm2/shopvippremium-backend-out.log',
      log_file: '/var/log/pm2/shopvippremium-backend.log'
    }
  ]
};
EOF

# Create log directory
mkdir -p /var/log/pm2

# Start application with PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Phase 8: Database Setup & Seeding

```bash
# Connect to MongoDB and create admin user
mongosh
use shopvippremium_prod
# Copy your existing data or run seeding scripts
```

### Phase 9: Domain Setup (Optional)

If you have a domain, update these files:
1. `/var/www/shopvippremium/backend/.env` - Update BACKEND_URL and FRONTEND_URL
2. `/var/www/shopvippremium/frontend/.env` - Update REACT_APP_BACKEND_URL  
3. `/etc/nginx/sites-available/shopvippremium` - Update server_name
4. Rebuild frontend: `cd /var/www/shopvippremium/frontend && npm run build`
5. Restart services: `pm2 restart all && systemctl reload nginx`

### Phase 10: SSL Setup (Recommended)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
certbot --nginx -d yourdomain.com

# Auto-renewal
systemctl enable certbot.timer
```

## Testing & Verification

```bash
# Check services
systemctl status nginx
systemctl status mongod
pm2 status

# Check logs
pm2 logs
tail -f /var/log/nginx/error.log

# Test endpoints
curl http://31.97.65.193
curl http://31.97.65.193/api/health
```

## Security Recommendations

```bash
# 1. Setup firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable

# 2. Disable root SSH login (after creating sudo user)
# 3. Change default SSH port
# 4. Setup fail2ban
apt install -y fail2ban
```

## Maintenance Commands

```bash
# Restart backend
pm2 restart shopvippremium-backend

# Update code
cd /var/www/shopvippremium
# Update files
pm2 restart all
systemctl reload nginx

# View logs
pm2 logs shopvippremium-backend
tail -f /var/log/nginx/access.log
```