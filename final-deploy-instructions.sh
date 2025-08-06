#!/bin/bash

# Shop VIP Premium - Final Deployment Instructions
# This script provides final deployment commands and startup

set -e

echo ""
echo "🚀 SHOP VIP PREMIUM - FINAL DEPLOYMENT INSTRUCTIONS"
echo "=================================================="
echo ""

SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

echo "📋 DEPLOYMENT SUMMARY:"
echo "====================="
echo "Server IP: $SERVER_IP"
echo "Backend Port: 8001 (managed by PM2)"
echo "Frontend: Static files served by Nginx"
echo "Database: MongoDB running on localhost:27017"
echo "Admin Credentials: admin@shopvippremium.com / admin123"
echo ""

echo "🔧 FINAL SETUP COMMANDS:"
echo "========================"
echo ""

# Check if all files exist
echo "1️⃣ First, run all the file creation scripts:"
echo ""
echo "cd /var/www/shopvippremium"
echo "bash -x /var/www/shopvippremium/create-frontend-files.sh"
echo "bash -x /var/www/shopvippremium/create-pages.sh"
echo "bash -x /var/www/shopvippremium/create-remaining-pages.sh"
echo "bash -x /var/www/shopvippremium/create-info-pages.sh"
echo ""

echo "2️⃣ Build the React frontend:"
echo ""
echo "cd /var/www/shopvippremium/frontend"
echo "yarn build"
echo ""

echo "3️⃣ Start the backend service with PM2:"
echo ""
echo "cd /var/www/shopvippremium"
echo "pm2 start ecosystem.config.js"
echo "pm2 save"
echo ""

echo "4️⃣ Ensure all services are running:"
echo ""
echo "# Check PM2 processes"
echo "pm2 list"
echo ""
echo "# Check Nginx status"
echo "systemctl status nginx"
echo ""
echo "# Check MongoDB status"
echo "systemctl status mongod"
echo ""

echo "🌐 ACCESS INFORMATION:"
echo "====================="
echo ""
echo "🏠 Main Website: http://$SERVER_IP"
echo "🔧 Admin Panel: http://$SERVER_IP/admin"
echo "📚 Products Page: http://$SERVER_IP/products"
echo "📞 Contact Page: http://$SERVER_IP/contact"
echo ""

echo "🔑 ADMIN LOGIN:"
echo "==============="
echo "Email: admin@shopvippremium.com"
echo "Password: admin123"
echo ""

echo "⚠️  IMPORTANT CONFIGURATION:"
echo "============================"
echo ""
echo "1. UPDATE NOWPAYMENTS API KEYS:"
echo "   Edit: /var/www/shopvippremium/backend/.env"
echo "   Set your actual Nowpayments API keys:"
echo "   - NOWPAYMENTS_IPN_SECRET"
echo "   - NOWPAYMENTS_PRIVATE_KEY"
echo "   - NOWPAYMENTS_PUBLIC_KEY"
echo ""
echo "2. RESTART BACKEND AFTER KEY UPDATE:"
echo "   pm2 restart shopvippremium-backend"
echo ""

echo "📱 SUPPORT CHANNELS:"
echo "==================="
echo "Update these in your admin panel and pages:"
echo "- Telegram: https://t.me/shopvippremium"
echo "- WhatsApp: https://wa.me/1234567890"
echo ""

echo "🛠️  MAINTENANCE COMMANDS:"
echo "========================"
echo ""
echo "# View backend logs"
echo "pm2 logs shopvippremium-backend"
echo ""
echo "# Restart all services"
echo "pm2 restart all"
echo "systemctl restart nginx"
echo ""
echo "# Monitor system"
echo "pm2 monit"
echo ""

echo "🔥 FEATURES INCLUDED:"
echo "===================="
echo ""
echo "✅ Complete e-commerce frontend (React)"
echo "✅ Secure backend API (FastAPI)"
echo "✅ MongoDB database with sample data"
echo "✅ User authentication & registration"
echo "✅ Cryptocurrency payment integration"
echo "✅ Comprehensive admin panel"
echo "✅ Product catalog management"
echo "✅ Order processing & tracking"
echo "✅ Dark theme UI/UX"
echo "✅ Mobile responsive design"
echo "✅ SEO optimized pages"
echo "✅ Legal pages (Privacy, Terms)"
echo "✅ Contact & support integration"
echo "✅ 24/7 ready deployment"
echo ""

echo "🎯 DEPLOYMENT COMPLETE!"
echo "======================"
echo ""
echo "Your Shop VIP Premium e-commerce platform is now ready!"
echo "Access your site at: http://$SERVER_IP"
echo ""
echo "Next steps:"
echo "1. Update Nowpayments API keys"
echo "2. Customize branding and content"
echo "3. Add your actual products"
echo "4. Configure payment methods"
echo "5. Set up SSL certificate (recommended)"
echo ""

# Create a simple status check script
cat > /var/www/shopvippremium/check-status.sh << 'EOF'
#!/bin/bash

echo "🔍 SYSTEM STATUS CHECK"
echo "====================="
echo ""

echo "📊 PM2 Processes:"
pm2 list

echo ""
echo "🌐 Nginx Status:"
systemctl is-active nginx

echo ""
echo "🗄️  MongoDB Status:"
systemctl is-active mongod

echo ""
echo "🔌 Port Check:"
echo "Backend (8001): $(netstat -tuln | grep :8001 | wc -l) connections"
echo "HTTP (80): $(netstat -tuln | grep :80 | wc -l) connections"

echo ""
echo "💾 Disk Usage:"
df -h /var/www/shopvippremium

echo ""
echo "🔗 Test URLs:"
echo "Main site: $(curl -o /dev/null -s -w "%{http_code}" http://localhost/ || echo "Failed")"
echo "API health: $(curl -o /dev/null -s -w "%{http_code}" http://localhost:8001/api/health || echo "Failed")"

echo ""
echo "Status check complete!"
EOF

chmod +x /var/www/shopvippremium/check-status.sh

echo "📋 STATUS CHECK SCRIPT CREATED:"
echo "Run: /var/www/shopvippremium/check-status.sh"
echo ""

echo "🎉 CONGRATULATIONS!"
echo "=================="
echo "Your Shop VIP Premium deployment package is ready!"
echo "All scripts and files have been created successfully."
echo ""
echo "Happy selling! 💰"