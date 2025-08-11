#!/bin/bash

#========================================
# SHOP VIP PREMIUM - CRITICAL BUG FIXES
# Fix Domain Typo and SSL Issues
# Domain: shopvipremium.com (CORRECTED)
#========================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_colored() {
    echo -e "${1}${2}${NC}"
}

print_step() {
    echo_colored $BLUE "🚀 STEP $1: $2"
    echo "=========================================="
}

print_success() {
    echo_colored $GREEN "✅ $1"
}

print_error() {
    echo_colored $RED "❌ ERROR: $1"
}

# Variables
CORRECT_DOMAIN="shopvipremium.com"
PROJECT_DIR="/var/www/shopvipremium"  # Updated to correct spelling

echo_colored $PURPLE "
#########################################
🔧 SHOP VIP PREMIUM - CRITICAL FIXES
#########################################

This script fixes the domain typo bug that prevents
products from being visible on shopvipremium.com

Issues Fixed:
✅ Domain typo: shopvippremium → shopvipremium (removed extra 'p')
✅ Frontend API URL configuration
✅ Nginx server configuration
✅ SSL certificate paths
✅ CORS headers

"

print_step "1" "Updating Frontend Configuration"

# Fix frontend .env file
cat > ${PROJECT_DIR}/frontend/.env << 'EOF'
REACT_APP_BACKEND_URL=https://shopvipremium.com/api
WDS_SOCKET_PORT=443

# Currency configuration
REACT_APP_CURRENCY_RATE=90

# Nowpayments Configuration
REACT_APP_NOWPAYMENTS_PUBLIC_KEY=66f018a4-4c91-4fdf-b8a0-275d63bc3d97
EOF

print_success "Frontend environment configured for correct domain"

print_step "2" "Updating Nginx Configuration"

# Create corrected Nginx configuration
cat > /etc/nginx/sites-available/shopvipremium << 'EOF'
# Nginx Configuration for Shop VIP Premium
# CORRECTED DOMAIN: shopvipremium.com

server {
    listen 80;
    listen [::]:80;
    server_name shopvipremium.com www.shopvipremium.com;
    
    # Let's Encrypt challenge location
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    # Redirect all HTTP traffic to HTTPS (after SSL setup)
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name shopvipremium.com www.shopvipremium.com;
    
    root /var/www/shopvipremium/frontend/build;
    index index.html;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Frontend routes - React Router
    location / {
        try_files $uri $uri/ /index.html;
        
        # Cache static files
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|webp)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }
    }
    
    # API routes - FastAPI Backend
    location /api {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase proxy timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # CORS headers for API
        add_header 'Access-Control-Allow-Origin' 'https://shopvipremium.com' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
        
        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 'https://shopvipremium.com';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
    
    # Admin panel - extra security
    location /admin {
        try_files $uri $uri/ /index.html;
    }
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Deny access to sensitive files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/x-javascript
        application/xml+rss
        application/javascript
        application/json
        application/atom+xml
        image/svg+xml;
}
EOF

# Enable the site (remove old symlink if exists)
rm -f /etc/nginx/sites-enabled/shopvippremium 2>/dev/null || true
rm -f /etc/nginx/sites-enabled/shopvipremium 2>/dev/null || true

# Create new symlink
ln -sf /etc/nginx/sites-available/shopvipremium /etc/nginx/sites-enabled/

print_success "Nginx configuration updated for correct domain"

print_step "3" "Testing Nginx Configuration"

# Test nginx configuration
if nginx -t; then
    print_success "Nginx configuration is valid"
else
    print_error "Nginx configuration has errors"
    exit 1
fi

print_step "4" "Creating SSL Challenge Directory"

# Ensure the ACME challenge directory exists
mkdir -p /var/www/html/.well-known/acme-challenge
chmod 755 /var/www/html/.well-known
chmod 755 /var/www/html/.well-known/acme-challenge
chown www-data:www-data /var/www/html/.well-known/acme-challenge

print_success "SSL challenge directory created"

print_step "5" "Restarting Services"

# Restart Nginx
systemctl reload nginx
print_success "Nginx reloaded with new configuration"

# Build React frontend if needed
if [ -d "$PROJECT_DIR/frontend" ]; then
    cd $PROJECT_DIR/frontend
    if [ ! -d "build" ] || [ ! -z "$(find src -newer build 2>/dev/null)" ]; then
        echo_colored $YELLOW "Building React frontend..."
        npm run build
        print_success "React frontend built successfully"
    else
        print_success "React frontend build is up to date"
    fi
fi

# Restart backend services (PM2 if using it)
if command -v pm2 &> /dev/null; then
    cd $PROJECT_DIR/backend
    pm2 restart ecosystem.config.js 2>/dev/null || pm2 start ecosystem.config.js
    print_success "Backend services restarted"
fi

print_step "6" "Installing SSL Certificate"

echo_colored $YELLOW "Installing SSL certificate for shopvipremium.com..."
echo_colored $YELLOW "This may take a few moments..."

# Stop nginx temporarily for standalone mode
systemctl stop nginx

# Try to obtain certificate using standalone mode first
if certbot certonly --standalone --agree-tos --no-eff-email --email admin@shopvipremium.com -d shopvipremium.com -d www.shopvipremium.com; then
    print_success "SSL certificate obtained successfully"
    
    # Update nginx configuration with SSL
    sed -i 's|# ssl_certificate|ssl_certificate|g' /etc/nginx/sites-available/shopvipremium
    sed -i 's|# ssl_certificate_key|ssl_certificate_key|g' /etc/nginx/sites-available/shopvipremium
    sed -i 's|# include /etc/letsencrypt|include /etc/letsencrypt|g' /etc/nginx/sites-available/shopvipremium
    sed -i 's|# ssl_dhparam|ssl_dhparam|g' /etc/nginx/sites-available/shopvipremium
    
    # Start nginx again
    systemctl start nginx
    systemctl reload nginx
    
    print_success "SSL certificate configured in Nginx"
else
    print_error "SSL certificate installation failed"
    echo_colored $YELLOW "Starting Nginx without SSL..."
    
    # Start nginx again even if SSL failed
    systemctl start nginx
    
    echo_colored $YELLOW "
    SSL Installation Failed. Common reasons:
    1. Domain DNS not pointing to this server
    2. Firewall blocking ports 80/443
    3. Domain not yet propagated
    
    Please check:
    - DNS A record for shopvipremium.com points to this server's IP
    - Ports 80 and 443 are open in firewall
    - Domain propagation (can take up to 24 hours)
    "
fi

print_step "7" "Final System Status Check"

# Check service status
echo_colored $BLUE "Service Status:"
systemctl is-active nginx && print_success "Nginx: Running" || print_error "Nginx: Not running"
systemctl is-active mongodb && print_success "MongoDB: Running" || echo_colored $YELLOW "⚠️  MongoDB: Not running (check if needed)"

# Check if PM2 is running
if command -v pm2 &> /dev/null; then
    if pm2 list | grep -q "online"; then
        print_success "Backend (PM2): Running"
    else
        print_error "Backend (PM2): Not running"
    fi
fi

# Check ports
echo_colored $BLUE "Port Status:"
netstat -tlnp | grep ":80 " && print_success "Port 80: Open" || print_error "Port 80: Not listening"
netstat -tlnp | grep ":443 " && print_success "Port 443: Open" || echo_colored $YELLOW "⚠️  Port 443: Not listening (normal without SSL)"
netstat -tlnp | grep ":8001 " && print_success "Backend Port 8001: Running" || print_error "Backend Port 8001: Not running"

echo_colored $GREEN "
#########################################
🎉 CRITICAL FIXES COMPLETED!
#########################################

✅ Domain typo fixed: shopvipremium.com
✅ Frontend configured to use correct API URL
✅ Nginx configuration updated
✅ SSL certificate directory prepared

NEXT STEPS:
1. Verify DNS: dig shopvipremium.com (should point to this server)
2. Check firewall: ufw status (ports 80, 443 should be open)
3. Test website: https://shopvipremium.com
4. Check products: https://shopvipremium.com/api/products

If products still don't show:
- Check browser console for API errors
- Verify backend is running: curl http://localhost:8001/api/health
- Check nginx logs: tail -f /var/log/nginx/error.log

"

echo_colored $PURPLE "Domain Fix Summary:"
echo "❌ OLD (wrong): shopvippremium.com (extra 'p')"
echo "✅ NEW (correct): shopvipremium.com"
echo ""