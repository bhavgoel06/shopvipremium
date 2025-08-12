#!/bin/bash
# ShopVIPremium.com - One-Click Deployment

set -e
DOMAIN="shopvipremium.com"
APP_DIR="/var/www/shopvipremium"

echo "🚀 Installing ShopVIPremium.com..."

# Install system packages
export DEBIAN_FRONTEND=noninteractive
apt update -qq && apt install -y nginx nodejs npm python3 python3-pip python3-venv mongodb curl certbot python3-certbot-nginx ufw
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - >/dev/null 2>&1
apt install -y nodejs
npm install -g pm2 --silent

# Setup firewall
ufw --force enable && ufw allow ssh && ufw allow 80 && ufw allow 443

# Create app directory
rm -rf $APP_DIR && mkdir -p $APP_DIR && cd $APP_DIR

# Download app from GitHub (replace with your repo)
git clone https://github.com/YOURUSERNAME/shopvipremium.git .

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt >/dev/null 2>&1

# Setup frontend  
cd ../frontend
npm install --silent
npm run build

# Configure nginx
cp nginx.conf /etc/nginx/sites-available/shopvipremium
ln -sf /etc/nginx/sites-available/shopvipremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
chown -R www-data:www-data $APP_DIR

# Test and start services
nginx -t
systemctl start mongodb nginx
systemctl enable mongodb nginx

# Start backend
cd $APP_DIR/backend
pm2 start ecosystem.config.js
pm2 save >/dev/null 2>&1
pm2 startup | grep -E '^sudo' | bash || true

# Install SSL
sleep 5
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo "⚠️ SSL failed - run manually"

echo "✅ Done! Visit https://$DOMAIN"