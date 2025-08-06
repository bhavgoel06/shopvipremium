#!/bin/bash

# Shop VIP Premium - Application Setup Script
# Run this AFTER uploading files to /var/www/shopvippremium/

set -e

echo "🚀 Setting up Shop VIP Premium application..."

cd /var/www/shopvippremium

# Extract files if tar exists
if [ -f "shopvippremium-deploy.tar.gz" ]; then
    echo "📦 Extracting deployment files..."
    tar -xzf shopvippremium-deploy.tar.gz
fi

# Backend Setup
echo "🐍 Setting up backend..."
cd /var/www/shopvippremium/backend

# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create production .env file
echo "📝 Creating backend .env file..."
cat > .env << 'EOF'
MONGO_URL="mongodb://localhost:27017"
DB_NAME="shopvippremium_prod"

# Nowpayments API Configuration
NOWPAYMENTS_IPN_SECRET="CRKTwqWfAbLGLeWdrsGZ4ZMES0DtTdD3"
NOWPAYMENTS_PRIVATE_KEY="S8QWJ1C-SDZ4WRE-QKZBRSJ-HJ9SQ7C"
NOWPAYMENTS_PUBLIC_KEY="66f018a4-4c91-4fdf-b8a0-275d63bc3d97"

# Production URLs
BACKEND_URL="http://31.97.65.193:8001"
FRONTEND_URL="http://31.97.65.193:3000"
EOF

# Frontend Setup
echo "⚛️ Setting up frontend..."
cd /var/www/shopvippremium/frontend

# Install dependencies
npm install

# Create production .env
echo "📝 Creating frontend .env file..."
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=http://31.97.65.193:8001
EOF

# Build for production
echo "🏗️ Building frontend for production..."
npm run build

# Nginx Configuration
echo "🌐 Configuring Nginx..."
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
ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx

# PM2 Configuration
echo "⚙️ Setting up PM2..."
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
echo "🚀 Starting application..."
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Setup basic firewall
echo "🔒 Setting up firewall..."
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

echo "✅ Shop VIP Premium deployment complete!"
echo ""
echo "🌐 Your site is now available at: http://31.97.65.193"
echo "🔐 Admin panel: http://31.97.65.193/admin"
echo "👤 Admin credentials: admin / VIP@dm1n2025!"
echo ""
echo "📊 Useful commands:"
echo "  - Check status: pm2 status"
echo "  - View logs: pm2 logs"
echo "  - Restart: pm2 restart all"