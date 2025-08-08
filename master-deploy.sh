#!/bin/bash

#========================================
# SHOP VIP PREMIUM - MASTER DEPLOYMENT SCRIPT
# One-Click Complete Website Deployment
# Domain: shopvippremium.com
# Author: AI Assistant
# Date: $(date)
#========================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="shopvippremium.com"
PROJECT_DIR="/var/www/shopvippremium"
BACKEND_PORT="8001"
FRONTEND_PORT="3000"
DB_NAME="shopvippremium_db"
ADMIN_EMAIL="admin@shopvippremium.com"  # For SSL certificate

# NOWPayments API Configuration
NOWPAYMENTS_IPN_SECRET="CRKTwqWfAbLGLeWdrsGZ4ZMES0DtTdD3"
NOWPAYMENTS_PRIVATE_KEY="S8QWJ1C-SDZ4WRE-QKZBRSJ-HJ9SQ7C"
NOWPAYMENTS_PUBLIC_KEY="66f018a4-4c91-4fdf-b8a0-275d63bc3d97"

echo_colored() {
    echo -e "${1}${2}${NC}"
}

print_step() {
    echo_colored $BLUE "
🚀 STEP $1: $2
=========================================="
}

print_success() {
    echo_colored $GREEN "✅ $1"
}

print_error() {
    echo_colored $RED "❌ ERROR: $1"
    exit 1
}

print_warning() {
    echo_colored $YELLOW "⚠️  WARNING: $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root. Use: sudo bash master-deploy.sh"
    fi
    print_success "Running as root user"
}

# System Information
print_system_info() {
    print_step "0" "SYSTEM INFORMATION"
    echo "OS: $(lsb_release -d | cut -f2)"
    echo "Kernel: $(uname -r)"
    echo "Architecture: $(uname -m)"
    echo "Memory: $(free -h | grep '^Mem' | awk '{print $2}')"
    echo "Disk Space: $(df -h / | awk 'NR==2{print $4}' 2>/dev/null || echo 'Unknown')"
    echo "Domain: $DOMAIN"
    echo "Project Directory: $PROJECT_DIR"
}

# Update system packages
update_system() {
    print_step "1" "UPDATING SYSTEM PACKAGES"
    
    # Add universe repository
    add-apt-repository universe -y
    
    # Update package lists
    apt update -y
    
    # Upgrade existing packages
    apt upgrade -y
    
    # Install essential packages
    apt install -y wget curl git unzip software-properties-common apt-transport-https ca-certificates lsb-release gnupg2 build-essential
    
    print_success "System packages updated successfully"
}

# Install Node.js
install_nodejs() {
    print_step "2" "INSTALLING NODE.JS 20.x LTS"
    
    # Remove any existing Node.js
    apt remove --purge -y nodejs npm node
    apt autoremove -y
    
    # Install NodeSource repository
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    
    # Install Node.js
    apt install -y nodejs
    
    # Install Yarn globally
    npm install -g yarn pm2
    
    # Verify installations
    node_version=$(node --version)
    npm_version=$(npm --version)
    yarn_version=$(yarn --version)
    pm2_version=$(pm2 --version)
    
    print_success "Node.js $node_version installed"
    print_success "NPM $npm_version installed"
    print_success "Yarn $yarn_version installed"
    print_success "PM2 $pm2_version installed"
}

# Install Python 3.11
install_python() {
    print_step "3" "INSTALLING PYTHON 3.11"
    
    # Add deadsnakes PPA for Python 3.11
    add-apt-repository ppa:deadsnakes/ppa -y
    apt update -y
    
    # Install Python 3.11 and related packages
    apt install -y python3.11 python3.11-venv python3.11-dev python3-pip python3.11-distutils
    
    # Create symbolic links
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
    
    # Install pip for Python 3.11
    curl https://bootstrap.pypa.io/get-pip.py | python3.11
    
    # Verify installation
    python_version=$(python3 --version)
    pip_version=$(pip3 --version)
    
    print_success "Python $python_version installed"
    print_success "Pip $pip_version installed"
}

# Install MongoDB
install_mongodb() {
    print_step "4" "INSTALLING MONGODB 7.0"
    
    # Import MongoDB GPG key
    curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
    
    # Add MongoDB repository
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    
    # Update package lists
    apt update -y
    
    # Install MongoDB
    apt install -y mongodb-org
    
    # Start and enable MongoDB
    systemctl start mongod
    systemctl enable mongod
    
    # Wait for MongoDB to start
    sleep 5
    
    # Verify MongoDB is running
    if systemctl is-active --quiet mongod; then
        print_success "MongoDB installed and running"
    else
        print_error "MongoDB failed to start"
    fi
}

# Install Nginx
install_nginx() {
    print_step "5" "INSTALLING NGINX"
    
    # Install Nginx
    apt install -y nginx
    
    # Start and enable Nginx
    systemctl start nginx
    systemctl enable nginx
    
    # Verify Nginx is running
    if systemctl is-active --quiet nginx; then
        print_success "Nginx installed and running"
    else
        print_error "Nginx failed to start"
    fi
}

# Setup project directory and clone/copy files
setup_project() {
    print_step "6" "SETTING UP PROJECT DIRECTORY"
    
    # Create project directory
    mkdir -p $PROJECT_DIR
    cd $PROJECT_DIR
    
    # If files are in current directory (for GitHub deployment)
    if [ -f "$(dirname "$0")/backend/server.py" ]; then
        echo "Copying files from current directory..."
        cp -r "$(dirname "$0")"/* $PROJECT_DIR/
    fi
    
    # Set proper permissions
    chown -R www-data:www-data $PROJECT_DIR
    chmod -R 755 $PROJECT_DIR
    
    print_success "Project directory setup complete"
}

# Setup backend
setup_backend() {
    print_step "7" "SETTING UP BACKEND (FastAPI)"
    
    cd $PROJECT_DIR/backend
    
    # Create virtual environment
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        print_error "requirements.txt not found"
    fi
    
    # Create .env file with all improvements
    cat > .env << EOF
# Database Configuration
MONGO_URL="mongodb://localhost:27017"
DB_NAME="$DB_NAME"

# JWT Configuration
JWT_SECRET="$(openssl rand -hex 32)"

# Nowpayments API Configuration
NOWPAYMENTS_IPN_SECRET="$NOWPAYMENTS_IPN_SECRET"
NOWPAYMENTS_PRIVATE_KEY="$NOWPAYMENTS_PRIVATE_KEY"
NOWPAYMENTS_PUBLIC_KEY="$NOWPAYMENTS_PUBLIC_KEY"

# Application Configuration
ENVIRONMENT="production"
DEBUG="false"
HOST="0.0.0.0"
PORT="$BACKEND_PORT"

# Currency Configuration
EXCHANGE_RATE="90"

# AI Tech Theme Configuration
THEME="ai-tech"
ENABLE_DUAL_CURRENCY="true"
ENABLE_CRYPTO_USD="true"
EOF
    
    # Set proper permissions for .env
    chmod 600 .env
    chown www-data:www-data .env
    
    print_success "Backend environment configured"
}

# Setup frontend
setup_frontend() {
    print_step "8" "SETTING UP FRONTEND (React)"
    
    cd $PROJECT_DIR/frontend
    
    # Create .env file for production
    cat > .env << EOF
REACT_APP_BACKEND_URL=https://$DOMAIN/api
GENERATE_SOURCEMAP=false
REACT_APP_NOWPAYMENTS_PUBLIC_KEY="$NOWPAYMENTS_PUBLIC_KEY"
FAST_REFRESH=false

# AI Tech Theme Configuration
REACT_APP_THEME="ai-tech"
REACT_APP_CURRENCY_RATE=90

# SEO and Gateway Configuration
REACT_APP_SITE_NAME="Shop VIP Premium"
REACT_APP_BUSINESS_TYPE="Digital Workspace Solutions"
REACT_APP_ENABLE_CRYPTO_USD=true
REACT_APP_ENABLE_DUAL_CURRENCY=true
EOF
    
    # Install dependencies using Yarn
    yarn install --frozen-lockfile
    
    # Build production version
    yarn build
    
    # Set proper permissions
    chown -R www-data:www-data build/
    chmod -R 755 build/
    
    print_success "Frontend built and configured"
}

# Seed database
seed_database() {
    print_step "9" "SEEDING DATABASE WITH PRODUCTS"
    
    cd $PROJECT_DIR/backend
    source venv/bin/activate
    
    # Run database seeder
    if [ -f "mega_product_seeder.py" ]; then
        python mega_product_seeder.py
        print_success "Database seeded with products"
    else
        print_warning "Database seeder not found, skipping..."
    fi
}

# Configure Nginx
configure_nginx() {
    print_step "10" "CONFIGURING NGINX"
    
    # Backup default config
    cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
    
    # Create new site configuration
    cat > /etc/nginx/sites-available/shopvippremium << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Redirect HTTP to HTTPS (will be enabled after SSL setup)
    # return 301 https://\$server_name\$request_uri;

    # Temporary configuration before SSL
    root $PROJECT_DIR/frontend/build;
    index index.html;
    
    # Frontend routes
    location / {
        try_files \$uri \$uri/ /index.html;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
    }
    
    # API routes (backend)
    location /api {
        proxy_pass http://127.0.0.1:$BACKEND_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
    }
    
    # Handle preflight requests
    location ~ ^/api {
        if (\$request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
    
    # Static files caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
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
        application/json;
}
EOF
    
    # Enable the site
    ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
    
    # Remove default site
    rm -f /etc/nginx/sites-enabled/default
    
    # Test Nginx configuration
    nginx -t
    
    # Reload Nginx
    systemctl reload nginx
    
    print_success "Nginx configured successfully"
}

# Setup SSL with Let's Encrypt
setup_ssl() {
    print_step "11" "SETTING UP SSL CERTIFICATE (Let's Encrypt)"
    
    # Install Certbot
    apt install -y certbot python3-certbot-nginx
    
    # Obtain SSL certificate
    echo "Obtaining SSL certificate for $DOMAIN..."
    
    # Run certbot with automatic nginx configuration
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email $ADMIN_EMAIL --redirect
    
    # Test automatic renewal
    certbot renew --dry-run
    
    # Set up automatic renewal cron job
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
    
    print_success "SSL certificate installed and auto-renewal configured"
}

# Setup PM2 for backend
setup_pm2() {
    print_step "12" "CONFIGURING PM2 FOR BACKEND"
    
    cd $PROJECT_DIR/backend
    
    # Create PM2 ecosystem file
    cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'shopvippremium-backend',
    script: 'venv/bin/python',
    args: '-m uvicorn server:app --host 0.0.0.0 --port $BACKEND_PORT --workers 4',
    cwd: '$PROJECT_DIR/backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PYTHONPATH: '$PROJECT_DIR/backend'
    },
    error_file: '/var/log/pm2/shopvippremium-backend-error.log',
    out_file: '/var/log/pm2/shopvippremium-backend-out.log',
    log_file: '/var/log/pm2/shopvippremium-backend.log',
    time: true
  }]
};
EOF
    
    # Create log directory
    mkdir -p /var/log/pm2
    chown -R www-data:www-data /var/log/pm2
    
    # Start application with PM2
    pm2 start ecosystem.config.js
    
    # Save PM2 configuration
    pm2 save
    
    # Setup PM2 to start on boot
    pm2 startup systemd -u root --hp /root
    
    print_success "PM2 configured and backend started"
}

# Configure firewall
configure_firewall() {
    print_step "13" "CONFIGURING FIREWALL"
    
    # Install and configure UFW
    apt install -y ufw
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Set default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH (important!)
    ufw allow ssh
    
    # Allow HTTP and HTTPS
    ufw allow 'Nginx Full'
    
    # Allow specific ports
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
    
    # Enable firewall
    ufw --force enable
    
    print_success "Firewall configured and enabled"
}

# Performance optimizations
optimize_performance() {
    print_step "14" "APPLYING PERFORMANCE OPTIMIZATIONS"
    
    # Optimize MongoDB
    cat >> /etc/mongod.conf << EOF

# Performance optimizations
operationProfiling:
  slowOpThresholdMs: 100

# Connection settings
net:
  maxIncomingConnections: 1000
EOF
    
    # Restart MongoDB
    systemctl restart mongod
    
    # Optimize Nginx
    sed -i 's/worker_connections 768/worker_connections 1024/' /etc/nginx/nginx.conf
    
    # Add performance settings to Nginx
    cat >> /etc/nginx/nginx.conf << EOF

# Performance optimizations
client_max_body_size 50M;
keepalive_timeout 65;
types_hash_max_size 2048;
server_names_hash_bucket_size 64;
EOF
    
    # Reload Nginx
    systemctl reload nginx
    
    print_success "Performance optimizations applied"
}

# Final verification
verify_deployment() {
    print_step "15" "VERIFYING DEPLOYMENT"
    
    echo "🔍 Checking services..."
    
    # Check MongoDB
    if systemctl is-active --quiet mongod; then
        print_success "MongoDB is running"
    else
        print_error "MongoDB is not running"
    fi
    
    # Check Nginx
    if systemctl is-active --quiet nginx; then
        print_success "Nginx is running"
    else
        print_error "Nginx is not running"
    fi
    
    # Check PM2 backend
    if pm2 describe shopvippremium-backend > /dev/null 2>&1; then
        print_success "Backend (PM2) is running"
    else
        print_error "Backend is not running"
    fi
    
    # Check if ports are listening
    if netstat -tln | grep -q ":$BACKEND_PORT "; then
        print_success "Backend is listening on port $BACKEND_PORT"
    else
        print_warning "Backend may not be listening on port $BACKEND_PORT"
    fi
    
    if netstat -tln | grep -q ":80 \|:443 "; then
        print_success "Nginx is listening on HTTP/HTTPS ports"
    else
        print_warning "Nginx may not be listening on HTTP/HTTPS ports"
    fi
    
    # Test database connection
    cd $PROJECT_DIR/backend
    source venv/bin/activate
    python -c "
import pymongo
try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['$DB_NAME']
    print('✅ Database connection successful')
    
    # Check if products exist
    products_count = db.products.count_documents({})
    print(f'✅ Products in database: {products_count}')
    
    if products_count == 0:
        print('⚠️  No products found - you may need to run the seeder manually')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
    
    print_success "Deployment verification completed"
}

# Print final instructions
print_final_instructions() {
    print_step "16" "DEPLOYMENT COMPLETED! 🎉"
    
    echo_colored $GREEN "
╔══════════════════════════════════════════════════════════════╗
║                 🎉 DEPLOYMENT SUCCESSFUL! 🎉                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Your Shop VIP Premium website is now live!                 ║
║                                                              ║
║  🌐 Website URL: https://$DOMAIN                      ║
║  🔐 Admin Panel: https://$DOMAIN/admin                ║
║                                                              ║
║  👤 Admin Login Credentials:                                 ║
║     Username: admin                                          ║
║     Password: VIP@dm1n2025!                                  ║
║                                                              ║
║  📁 Project Directory: $PROJECT_DIR                          ║
║  🗄️  Database: $DB_NAME                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"
    
    echo_colored $YELLOW "
📝 IMPORTANT POST-DEPLOYMENT NOTES:

1. 🔒 SSL Certificate: Automatically configured with Let's Encrypt
2. 🔄 Auto-renewal: SSL certificates will auto-renew via cron job
3. 🛡️  Firewall: UFW enabled with necessary ports open
4. 📈 Performance: MongoDB and Nginx optimized for production
5. 🔧 Process Management: Backend managed by PM2 with auto-restart

🔧 USEFUL COMMANDS:

# Check services status
sudo systemctl status nginx mongod
pm2 status

# View backend logs
pm2 logs shopvippremium-backend

# Restart services
sudo systemctl restart nginx mongod
pm2 restart shopvippremium-backend

# Check SSL certificate
sudo certbot certificates

# Manual SSL renewal (if needed)
sudo certbot renew

# View firewall status
sudo ufw status

📞 SUPPORT:
If you need any assistance, contact support via:
- Telegram: @shopvippremium  
- Email: admin@shopvippremium.com
"
    
    echo_colored $BLUE "
🚀 Your e-commerce platform is ready for business!
   Visit https://$DOMAIN to see your live website!
"
}

# Main deployment function
main() {
    echo_colored $PURPLE "
╔══════════════════════════════════════════════════════════════╗
║           SHOP VIP PREMIUM - MASTER DEPLOYMENT              ║
║                   Starting Deployment...                     ║
╚══════════════════════════════════════════════════════════════╝
"
    
    print_system_info
    check_root
    update_system
    install_nodejs
    install_python
    install_mongodb
    install_nginx
    setup_project
    setup_backend
    setup_frontend
    seed_database
    configure_nginx
    setup_ssl
    setup_pm2
    configure_firewall
    optimize_performance
    verify_deployment
    print_final_instructions
}

# Run main function
main

echo_colored $GREEN "
🎉 DEPLOYMENT COMPLETED SUCCESSFULLY! 🎉
Visit https://$DOMAIN to see your live website!
"