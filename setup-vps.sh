#!/bin/bash

# Shop VIP Premium - VPS Setup Script
# Run this on your VPS as root

set -e

echo "🚀 Setting up Shop VIP Premium on VPS..."

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install essential packages
echo "🔧 Installing essential packages..."
apt install -y curl wget git nginx software-properties-common

# Install Node.js 18
echo "📱 Installing Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Install Python 3.11 and pip
echo "🐍 Installing Python 3.11..."
apt install -y python3.11 python3.11-venv python3-pip

# Install MongoDB
echo "🗄️ Installing MongoDB..."
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org

# Start and enable services
echo "🔄 Starting services..."
systemctl start mongod
systemctl enable mongod
systemctl start nginx
systemctl enable nginx

# Install PM2 globally
echo "⚙️ Installing PM2..."
npm install -g pm2

# Create app directory
echo "📁 Creating application directory..."
mkdir -p /var/www/shopvippremium
cd /var/www/shopvippremium

echo "✅ VPS setup complete!"
echo "📋 Next steps:"
echo "1. Upload your deployment files to /var/www/shopvippremium/"
echo "2. Run the application setup script"