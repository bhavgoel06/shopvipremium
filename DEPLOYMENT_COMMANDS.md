# VPS Deployment Commands - Copy & Paste

## 1. Connect to VPS
```bash
ssh root@31.97.65.193
# Password: @FlashRocks23xshop
```

## 2. System Setup
```bash
# Update system
apt update && apt upgrade -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Install Python 3.11
apt install -y python3.11 python3.11-venv python3-pip

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org nginx

# Start services
systemctl start mongod nginx
systemctl enable mongod nginx

# Install PM2
npm install -g pm2

# Create directory
mkdir -p /var/www/shopvippremium
cd /var/www/shopvippremium
```

## 3. Upload Files
**Option A: Use SCP from your local machine**
```bash
# From LOCAL machine (where the app is)
scp /app/shopvippremium-deploy.tar.gz root@31.97.65.193:/var/www/shopvippremium/
```

**Option B: Create files directly on VPS (I'll guide you through this)**

## 4. Setup Application
```bash
# Extract files (if using Option A)
cd /var/www/shopvippremium
tar -xzf shopvippremium-deploy.tar.gz

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create backend .env
cat > .env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="shopvippremium_prod"
NOWPAYMENTS_IPN_SECRET="CRKTwqWfAbLGLeWdrsGZ4ZMES0DtTdD3"
NOWPAYMENTS_PRIVATE_KEY="S8QWJ1C-SDZ4WRE-QKZBRSJ-HJ9SQ7C"
NOWPAYMENTS_PUBLIC_KEY="66f018a4-4c91-4fdf-b8a0-275d63bc3d97"
BACKEND_URL="http://31.97.65.193:8001"
FRONTEND_URL="http://31.97.65.193:3000"
EOF

# Frontend setup
cd ../frontend
npm install

# Create frontend .env
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://31.97.65.193:8001
EOF

# Build frontend
npm run build
```

## 5. Configure Nginx
```bash
# Create Nginx config
cat > /etc/nginx/sites-available/shopvippremium << 'EOF'
server {
    listen 80;
    server_name 31.97.65.193;
    
    location / {
        root /var/www/shopvippremium/frontend/build;
        try_files $uri $uri/ /index.html;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
    }
    
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
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        root /var/www/shopvippremium/frontend/build;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

## 6. Start with PM2
```bash
cd /var/www/shopvippremium

# Create PM2 config
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'shopvippremium-backend',
      script: 'venv/bin/python',
      args: '-m uvicorn server:app --host 0.0.0.0 --port 8001 --workers 2',
      cwd: '/var/www/shopvippremium/backend',
      env: { NODE_ENV: 'production' },
      instances: 1,
      exec_mode: 'fork',
      watch: false,
      autorestart: true,
      max_memory_restart: '1G'
    }
  ]
};
EOF

# Start app
mkdir -p /var/log/pm2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 7. Security
```bash
# Basic firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable
```

## 8. Test
```bash
# Check services
systemctl status nginx mongod
pm2 status

# Test endpoints
curl http://31.97.65.193
curl http://31.97.65.193/api/health
```

## 9. Access Your Site
- **Website**: http://31.97.65.193
- **Admin**: http://31.97.65.193/admin
- **Credentials**: admin / VIP@dm1n2025!

## Maintenance
```bash
# View logs
pm2 logs
tail -f /var/log/nginx/error.log

# Restart
pm2 restart all
systemctl reload nginx

# Update code (future updates)
cd /var/www/shopvippremium
# Upload new files
pm2 restart all
```