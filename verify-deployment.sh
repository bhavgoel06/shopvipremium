#!/bin/bash

#========================================
# SHOP VIP PREMIUM - DEPLOYMENT VERIFICATION
# Post-deployment health check script
#========================================

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo_colored() {
    echo -e "${1}${2}${NC}"
}

print_success() {
    echo_colored $GREEN "✅ $1"
}

print_error() {
    echo_colored $RED "❌ $1"
}

print_warning() {
    echo_colored $YELLOW "⚠️  $1"
}

print_info() {
    echo_colored $BLUE "ℹ️  $1"
}

DOMAIN="shopvippremium.com"
PROJECT_DIR="/var/www/shopvippremium"
DB_NAME="shopvippremium_db"

echo_colored $BLUE "
╔══════════════════════════════════════════════════════════════╗
║           SHOP VIP PREMIUM - DEPLOYMENT VERIFICATION        ║
╚══════════════════════════════════════════════════════════════╝
"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    print_error "This script should be run as root for complete verification"
    exit 1
fi

echo "🔍 Starting comprehensive deployment verification..."
echo

# 1. Check system services
echo "1. CHECKING SYSTEM SERVICES"
echo "────────────────────────────"

# MongoDB
if systemctl is-active --quiet mongod; then
    print_success "MongoDB is running"
    
    # Check MongoDB connection
    if mongo --eval "db.adminCommand('ismaster')" &>/dev/null; then
        print_success "MongoDB connection successful"
    else
        print_error "MongoDB connection failed"
    fi
else
    print_error "MongoDB is not running"
fi

# Nginx
if systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
    
    # Test Nginx configuration
    if nginx -t &>/dev/null; then
        print_success "Nginx configuration is valid"
    else
        print_error "Nginx configuration has errors"
    fi
else
    print_error "Nginx is not running"
fi

# PM2
if command -v pm2 &>/dev/null; then
    if pm2 describe shopvippremium-backend &>/dev/null; then
        PM2_STATUS=$(pm2 describe shopvippremium-backend | grep -o "status.*online\|status.*stopped")
        if [[ $PM2_STATUS == *"online"* ]]; then
            print_success "Backend (PM2) is running"
        else
            print_error "Backend is not running (PM2 status: stopped)"
        fi
    else
        print_error "Backend process not found in PM2"
    fi
else
    print_error "PM2 is not installed"
fi

echo

# 2. Check network ports
echo "2. CHECKING NETWORK PORTS"
echo "──────────────────────────"

# Backend port
if netstat -tln | grep -q ":8001 "; then
    print_success "Backend is listening on port 8001"
else
    print_warning "Backend may not be listening on port 8001"
fi

# HTTP port
if netstat -tln | grep -q ":80 "; then
    print_success "Nginx is listening on port 80 (HTTP)"
else
    print_warning "HTTP port 80 is not listening"
fi

# HTTPS port
if netstat -tln | grep -q ":443 "; then
    print_success "Nginx is listening on port 443 (HTTPS)"
else
    print_warning "HTTPS port 443 is not listening"
fi

echo

# 3. Check SSL certificates
echo "3. CHECKING SSL CERTIFICATES"
echo "─────────────────────────────"

if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    print_success "SSL certificate directory exists"
    
    # Check certificate validity
    CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
    if [ -f "$CERT_PATH" ]; then
        CERT_EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_PATH" 2>/dev/null | cut -d= -f2)
        if [ ! -z "$CERT_EXPIRY" ]; then
            print_success "SSL certificate is valid until: $CERT_EXPIRY"
        else
            print_warning "Could not read SSL certificate expiry"
        fi
    else
        print_error "SSL certificate file not found"
    fi
else
    print_warning "SSL certificate not found - may need manual setup"
fi

echo

# 4. Check database
echo "4. CHECKING DATABASE"
echo "────────────────────"

cd $PROJECT_DIR/backend
if [ -d "venv" ]; then
    source venv/bin/activate
    
    # Test database connection and count products
    python3 -c "
import pymongo
import sys
try:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['$DB_NAME']
    
    # Check database connection
    client.admin.command('ismaster')
    print('✅ Database connection successful')
    
    # Check collections
    collections = db.list_collection_names()
    print(f'✅ Found {len(collections)} collections: {collections}')
    
    # Check products
    if 'products' in collections:
        products_count = db.products.count_documents({})
        print(f'✅ Products in database: {products_count}')
        if products_count == 0:
            print('⚠️  No products found - database may need seeding')
    else:
        print('⚠️  Products collection not found')
        
    # Check users
    if 'users' in collections:
        users_count = db.users.count_documents({})
        print(f'✅ Users in database: {users_count}')
    
    # Check orders
    if 'orders' in collections:
        orders_count = db.orders.count_documents({})
        print(f'✅ Orders in database: {orders_count}')
        
except Exception as e:
    print(f'❌ Database error: {e}')
    sys.exit(1)
" 2>/dev/null || print_error "Database verification failed"
else
    print_error "Python virtual environment not found"
fi

echo

# 5. Check file permissions
echo "5. CHECKING FILE PERMISSIONS"
echo "─────────────────────────────"

if [ -d "$PROJECT_DIR" ]; then
    print_success "Project directory exists: $PROJECT_DIR"
    
    # Check ownership
    OWNER=$(stat -c '%U:%G' $PROJECT_DIR)
    if [[ $OWNER == *"www-data"* ]]; then
        print_success "Project directory has correct ownership: $OWNER"
    else
        print_warning "Project directory ownership: $OWNER (expected www-data)"
    fi
    
    # Check frontend build
    if [ -d "$PROJECT_DIR/frontend/build" ]; then
        print_success "Frontend build directory exists"
    else
        print_warning "Frontend build directory not found"
    fi
    
    # Check backend virtual environment
    if [ -d "$PROJECT_DIR/backend/venv" ]; then
        print_success "Backend virtual environment exists"
    else
        print_error "Backend virtual environment not found"
    fi
else
    print_error "Project directory not found: $PROJECT_DIR"
fi

echo

# 6. Check firewall
echo "6. CHECKING FIREWALL"
echo "─────────────────────"

if command -v ufw &>/dev/null; then
    UFW_STATUS=$(ufw status | head -1)
    if [[ $UFW_STATUS == *"active"* ]]; then
        print_success "UFW firewall is active"
        
        # Check specific ports
        if ufw status | grep -q "22"; then
            print_success "SSH port 22 is allowed"
        else
            print_warning "SSH port 22 may not be explicitly allowed"
        fi
        
        if ufw status | grep -q "80\|Nginx"; then
            print_success "HTTP port 80 is allowed"
        else
            print_warning "HTTP port 80 may not be allowed"
        fi
        
        if ufw status | grep -q "443\|Nginx"; then
            print_success "HTTPS port 443 is allowed"
        else
            print_warning "HTTPS port 443 may not be allowed"
        fi
    else
        print_warning "UFW firewall is not active"
    fi
else
    print_warning "UFW firewall is not installed"
fi

echo

# 7. Test HTTP endpoints
echo "7. TESTING HTTP ENDPOINTS"
echo "──────────────────────────"

# Test backend health
if curl -s "http://localhost:8001/health" &>/dev/null; then
    print_success "Backend health endpoint responding"
else
    print_warning "Backend health endpoint not responding"
fi

# Test frontend
if curl -s "http://localhost/" | grep -q "Shop VIP Premium\|React\|html" &>/dev/null; then
    print_success "Frontend is serving content"
else
    print_warning "Frontend may not be serving correctly"
fi

# Test HTTPS (if certificate exists)
if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    if curl -s -k "https://localhost/" &>/dev/null; then
        print_success "HTTPS is responding"
    else
        print_warning "HTTPS may not be configured correctly"
    fi
fi

echo

# 8. Check logs for errors
echo "8. CHECKING RECENT LOGS"
echo "───────────────────────"

# Check Nginx error logs
if [ -f "/var/log/nginx/error.log" ]; then
    NGINX_ERRORS=$(tail -10 /var/log/nginx/error.log | grep -i "error\|critical" | wc -l)
    if [ "$NGINX_ERRORS" -eq 0 ]; then
        print_success "No recent Nginx errors"
    else
        print_warning "$NGINX_ERRORS recent Nginx errors found"
    fi
else
    print_warning "Nginx error log not found"
fi

# Check PM2 logs
if pm2 logs shopvippremium-backend --lines 10 --nostream 2>/dev/null | grep -i "error\|exception" &>/dev/null; then
    print_warning "Backend errors found in PM2 logs"
else
    print_success "No recent backend errors in PM2 logs"
fi

echo

# 9. Performance check
echo "9. PERFORMANCE CHECK"
echo "────────────────────"

# Check system resources
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

print_info "Memory usage: ${MEMORY_USAGE}%"
print_info "Disk usage: ${DISK_USAGE}%"

if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    print_warning "High memory usage detected"
else
    print_success "Memory usage is normal"
fi

if [ "$DISK_USAGE" -gt 80 ]; then
    print_warning "High disk usage detected"
else
    print_success "Disk usage is normal"
fi

echo

# 10. Final summary
echo "10. DEPLOYMENT SUMMARY"
echo "──────────────────────"

print_info "Domain: https://$DOMAIN"
print_info "Admin Panel: https://$DOMAIN/admin"
print_info "Admin Username: admin"
print_info "Admin Password: VIP@dm1n2025!"
print_info "Project Directory: $PROJECT_DIR"
print_info "Database: $DB_NAME"

echo_colored $GREEN "
╔══════════════════════════════════════════════════════════════╗
║                    VERIFICATION COMPLETE                     ║
║                                                              ║
║  🌐 Website: https://$DOMAIN                          ║
║  🔐 Admin: https://$DOMAIN/admin                       ║
║                                                              ║
║  If any issues were found above, please review the          ║
║  deployment logs and run the master-deploy.sh script        ║
║  again if necessary.                                         ║
╚══════════════════════════════════════════════════════════════╝
"

print_info "Verification completed at $(date)"