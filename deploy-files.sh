#!/bin/bash

# Complete deployment script for Shop VIP Premium
# This will create all necessary files on your VPS

echo "🚀 Creating Shop VIP Premium deployment files..."

# Create directory structure
mkdir -p /var/www/shopvippremium/{backend,frontend/src,frontend/public}
cd /var/www/shopvippremium

# Create backend requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
motor==3.3.2
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
requests==2.31.0
python-dotenv==1.0.0
pymongo==4.6.0
bcrypt==4.1.2
PyJWT==2.8.0
aiofiles==23.2.1
EOF

echo "✅ Backend requirements created"

# Create frontend package.json
cat > frontend/package.json << 'EOF'
{
  "name": "shopvippremium-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "react-helmet": "^6.1.0",
    "react-toastify": "^9.1.1",
    "@heroicons/react": "^2.0.16",
    "framer-motion": "^10.8.5"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "devDependencies": {
    "react-scripts": "^5.0.1",
    "tailwindcss": "^3.2.7",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.21",
    "@craco/craco": "^7.1.0"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
EOF

echo "✅ Frontend package.json created"
echo "📁 Directory structure ready at /var/www/shopvippremium"
echo ""
echo "🔄 Next: Run the application setup script"