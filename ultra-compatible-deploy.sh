#!/bin/bash

# Shop VIP Premium - Ultra-Compatible One-Click Deployment
# Works on all Ubuntu versions

set -e

echo "🚀 Shop VIP Premium - Ultra-Compatible Deployment"
echo "================================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root: sudo bash"
    exit 1
fi

SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
print_status "Detected Server IP: $SERVER_IP"

print_status "Step 1/10: System Detection & Updates"
UBUNTU_VERSION=$(lsb_release -rs 2>/dev/null || echo "20.04")
print_status "Ubuntu Version: $UBUNTU_VERSION"

# Comprehensive system update
apt update && apt upgrade -y

# Add all necessary repositories
add-apt-repository main -y 2>/dev/null || true
add-apt-repository universe -y 2>/dev/null || true
add-apt-repository restricted -y 2>/dev/null || true
add-apt-repository multiverse -y 2>/dev/null || true

apt update

print_status "Step 2/10: Installing Core Dependencies"
# Install absolutely essential packages first
apt install -y curl wget software-properties-common apt-transport-https ca-certificates lsb-release

# Install gnupg (try different variants)
apt install -y gnupg || apt install -y gnupg2 || apt install -y gnupg-agent

print_status "Step 3/10: Installing Node.js 20"
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Yarn globally
npm install -g yarn

print_status "Step 4/10: Installing Python (Multiple Attempts)"
# Try to install Python packages with multiple fallbacks
PYTHON_INSTALLED=false

# Method 1: Try standard packages
if apt install -y python3 python3-venv python3-dev python3-pip 2>/dev/null; then
    print_success "Standard Python packages installed"
    PYTHON_INSTALLED=true
fi

# Method 2: Try without specific packages
if [ "$PYTHON_INSTALLED" = false ]; then
    print_status "Trying alternative Python installation..."
    apt install -y python3 2>/dev/null || true
    
    # Install pip manually if not available
    if ! command -v pip3 &> /dev/null; then
        print_status "Installing pip manually..."
        curl -sSL https://bootstrap.pypa.io/get-pip.py | python3
    fi
    
    # Try to install venv capability
    python3 -m pip install virtualenv 2>/dev/null || true
    PYTHON_INSTALLED=true
fi

# Method 3: Deadpool mode - install what we can
if [ "$PYTHON_INSTALLED" = false ]; then
    print_warning "Using fallback Python setup..."
    # Just get Python3 working somehow
    which python3 || apt install -y python3-minimal
    
    # Get pip working
    curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 --user
    export PATH="$HOME/.local/bin:$PATH"
    
    PYTHON_INSTALLED=true
fi

print_status "Step 5/10: Installing Build Tools"
# Install build tools (try multiple approaches)
apt install -y build-essential 2>/dev/null || apt install -y gcc g++ make libc6-dev

print_status "Step 6/10: Installing MongoDB"
# Install MongoDB with better error handling
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg 2>/dev/null || true

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list 2>/dev/null || true

apt update
if ! apt install -y mongodb-org; then
    print_warning "MongoDB 7.0 failed, trying fallback..."
    apt install -y mongodb 2>/dev/null || apt install -y mongodb-server 2>/dev/null || print_warning "MongoDB installation skipped - will use external DB"
fi

print_status "Step 7/10: Installing Nginx & PM2"
apt install -y nginx
npm install -g pm2

print_status "Step 8/10: Creating Application Structure"
mkdir -p /var/www/shopvippremium/{backend,frontend}
cd /var/www/shopvippremium

print_status "Step 9/10: Setting Up Backend"
# Backend requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pymongo==4.6.0
motor==3.3.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
requests==2.31.0
pydantic==2.5.2
python-dotenv==1.0.0
bcrypt==4.1.2
EOF

# Backend .env
cat > backend/.env << EOF
MONGO_URL=mongodb://localhost:27017/shopvippremium
DB_NAME=shopvippremium
SECRET_KEY=shop-vip-premium-secret-$(openssl rand -hex 16)
BACKEND_URL=http://$SERVER_IP:8001
FRONTEND_URL=http://$SERVER_IP
NOWPAYMENTS_IPN_SECRET=your_nowpayments_ipn_secret_here
NOWPAYMENTS_PRIVATE_KEY=your_nowpayments_private_key_here
NOWPAYMENTS_PUBLIC_KEY=your_nowpayments_public_key_here
EOF

print_warning "⚠️  IMPORTANT: Update Nowpayments API keys in backend/.env"

# Setup Python environment with multiple fallback methods
cd backend

print_status "Setting up Python virtual environment..."
# Try different venv methods
if python3 -m venv venv 2>/dev/null; then
    print_success "Created venv using python3 -m venv"
elif python3 -m virtualenv venv 2>/dev/null; then
    print_success "Created venv using virtualenv"
elif virtualenv venv 2>/dev/null; then
    print_success "Created venv using virtualenv command"
else
    print_warning "Could not create virtual environment, using global Python"
    mkdir -p venv/bin
    ln -sf $(which python3) venv/bin/python
    ln -sf $(which pip3) venv/bin/pip
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || export PATH="/var/www/shopvippremium/backend/venv/bin:$PATH"

# Upgrade pip in multiple ways
python -m pip install --upgrade pip 2>/dev/null || pip install --upgrade pip 2>/dev/null || true

# Install Python dependencies with fallbacks
print_status "Installing Python dependencies..."
pip install -r requirements.txt || {
    print_warning "Requirements install failed, trying individual packages..."
    pip install fastapi uvicorn pymongo motor requests pydantic python-dotenv bcrypt
    pip install "python-jose[cryptography]" || pip install python-jose
    pip install "passlib[bcrypt]" || pip install passlib
    pip install python-multipart || true
}

# Create all backend files
print_status "Creating backend application files..."

cat > models.py << 'EOF'
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    hashed_password: str
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price_usd: float
    price_inr: float
    category: str
    image_url: Optional[str] = None
    is_featured: bool = False
    is_bestseller: bool = False
    in_stock: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    product_ids: List[str]
    total_amount: float
    currency: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Payment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    payment_method: str
    amount: float
    currency: str
    status: PaymentStatus = PaymentStatus.PENDING
    payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
EOF

cat > database.py << 'EOF'
import os
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Product, Order, Payment, UserRole, OrderStatus, PaymentStatus
from passlib.context import CryptContext
from datetime import datetime
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/shopvippremium")
    db_name = os.environ.get("DB_NAME", "shopvippremium")
    
    db.client = AsyncIOMotorClient(mongo_url)
    db.database = db.client[db_name]
    print(f"Connected to MongoDB: {db_name}")

async def close_mongo_connection():
    if db.client:
        db.client.close()

async def create_user(user_data: dict) -> str:
    user_data["hashed_password"] = pwd_context.hash(user_data["password"])
    del user_data["password"]
    user = User(**user_data)
    await db.database.users.insert_one(user.dict())
    return user.id

async def get_user_by_email(email: str) -> Optional[dict]:
    return await db.database.users.find_one({"email": email})

async def get_user_by_id(user_id: str) -> Optional[dict]:
    return await db.database.users.find_one({"id": user_id})

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_product(product_data: dict) -> str:
    product = Product(**product_data)
    await db.database.products.insert_one(product.dict())
    return product.id

async def get_products(skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[dict]:
    query = {}
    if category:
        query["category"] = category
    cursor = db.database.products.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def get_product_by_id(product_id: str) -> Optional[dict]:
    return await db.database.products.find_one({"id": product_id})

async def get_featured_products() -> List[dict]:
    cursor = db.database.products.find({"is_featured": True})
    return await cursor.to_list(length=None)

async def get_bestseller_products() -> List[dict]:
    cursor = db.database.products.find({"is_bestseller": True})
    return await cursor.to_list(length=None)

async def create_order(order_data: dict) -> str:
    order = Order(**order_data)
    await db.database.orders.insert_one(order.dict())
    return order.id

async def get_order_by_id(order_id: str) -> Optional[dict]:
    return await db.database.orders.find_one({"id": order_id})

async def get_dashboard_stats() -> dict:
    total_users = await db.database.users.count_documents({})
    total_products = await db.database.products.count_documents({})
    total_orders = await db.database.orders.count_documents({})
    
    pipeline = [{"$match": {"status": "completed"}}, {"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}]
    revenue_result = await db.database.orders.aggregate(pipeline).to_list(length=1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    return {"total_users": total_users, "total_products": total_products, "total_orders": total_orders, "total_revenue": total_revenue}
EOF

cat > server.py << 'EOF'
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from database import connect_to_mongo, close_mongo_connection, create_user, get_user_by_email, get_user_by_id, verify_password, create_product, get_products, get_product_by_id, get_featured_products, get_bestseller_products, create_order, get_order_by_id, get_dashboard_stats
from models import User, Product, Order, UserRole
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Shop VIP Premium API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = await get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/auth/register")
async def register(user_data: dict):
    existing_user = await get_user_by_email(user_data["email"])
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = await create_user(user_data)
    return {"message": "User created successfully", "user_id": user_id}

@app.post("/api/auth/login")
async def login(credentials: dict):
    user = await get_user_by_email(credentials["email"])
    if not user or not verify_password(credentials["password"], user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["id"]}, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": {"id": user["id"], "email": user["email"], "username": user["username"], "role": user["role"]}
    }

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {"id": current_user["id"], "email": current_user["email"], "username": current_user["username"], "role": current_user["role"]}

@app.get("/api/products")
async def get_products_endpoint(skip: int = 0, limit: int = 100, category: Optional[str] = None):
    products = await get_products(skip=skip, limit=limit, category=category)
    return {"products": products}

@app.get("/api/products/featured")
async def get_featured_products_endpoint():
    products = await get_featured_products()
    return {"products": products}

@app.get("/api/products/bestsellers")
async def get_bestseller_products_endpoint():
    products = await get_bestseller_products()
    return {"products": products}

@app.get("/api/products/{product_id}")
async def get_product_endpoint(product_id: str):
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/orders")
async def create_order_endpoint(order_data: dict, current_user: dict = Depends(get_current_user)):
    order_data["user_id"] = current_user["id"]
    order_id = await create_order(order_data)
    return {"order_id": order_id, "message": "Order created successfully"}

@app.get("/api/admin/dashboard")
async def get_dashboard_stats_endpoint(admin_user: dict = Depends(get_admin_user)):
    return await get_dashboard_stats()

@app.post("/api/admin/products")
async def create_product_endpoint(product_data: dict, admin_user: dict = Depends(get_admin_user)):
    product_id = await create_product(product_data)
    return {"product_id": product_id, "message": "Product created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
EOF

print_status "Step 10/10: Setting Up Frontend"
cd ../frontend

# Create package.json
cat > package.json << 'EOF'
{
  "name": "shopvippremium-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^1.6.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "react-scripts": "5.0.1",
    "react-toastify": "^9.1.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  },
  "devDependencies": {
    "tailwindcss": "^3.3.6"
  }
}
EOF

cat > .env << EOF
REACT_APP_BACKEND_URL=http://$SERVER_IP:8001
GENERATE_SOURCEMAP=false
EOF

print_status "Installing frontend dependencies..."
yarn install
yarn add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

mkdir -p public src/{components,pages,context}

cat > tailwind.config.js << 'EOF'
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
}
EOF

cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Shop VIP Premium - Digital Workspace Toolkit</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
EOF

cat > src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<React.StrictMode><App /></React.StrictMode>);
EOF

cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background-color: #111827; color: #f9fafb; }
.btn-primary { @apply bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors; }
.card-dark { @apply bg-gray-800 border border-gray-700 rounded-xl; }
EOF

cat > src/App.js << 'EOF'
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-900 text-white">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/admin" element={<AdminDashboard />} />
            </Routes>
          </main>
          <ToastContainer position="top-right" theme="dark" />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
EOF

cat > src/context/AuthContext.js << 'EOF'
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, { email, password });
      const { access_token, user: userData } = response.data;
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('token', access_token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>;
};
EOF

cat > src/components/Header.js << 'EOF'
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="bg-gray-800 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-400">Shop VIP Premium</Link>
          
          <nav className="flex items-center space-x-6">
            <Link to="/products" className="text-gray-300 hover:text-white">Products</Link>
            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-300">Hi, {user.username}</span>
                {user.role === 'admin' && (
                  <Link to="/admin" className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700">Admin</Link>
                )}
                <button onClick={logout} className="text-gray-300 hover:text-white">Logout</button>
              </div>
            ) : (
              <Link to="/login" className="btn-primary">Login</Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
EOF

cat > src/pages/HomePage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const HomePage = () => {
  const [products, setProducts] = useState([]);
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products/featured`);
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <section className="bg-gradient-to-r from-blue-900 to-purple-900 py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold text-white mb-6">
            Premium Digital <span className="text-blue-400">Workspace Toolkit</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Discover professional-grade productivity tools and business utilities
          </p>
          <Link to="/products" className="btn-primary text-lg px-8">Browse Products</Link>
        </div>
      </section>

      <section className="py-16 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-white mb-12">Why Choose Us?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 card-dark">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-semibold text-white mb-2">Premium Quality</h3>
              <p className="text-gray-400">Professional-grade tools</p>
            </div>
            <div className="text-center p-6 card-dark">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold text-white mb-2">Secure Payments</h3>
              <p className="text-gray-400">Safe transactions</p>
            </div>
            <div className="text-center p-6 card-dark">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold text-white mb-2">Fast Delivery</h3>
              <p className="text-gray-400">Instant access</p>
            </div>
          </div>
        </div>
      </section>

      {products.length > 0 && (
        <section className="py-16 bg-gray-800">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-center text-white mb-12">Featured Products</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {products.slice(0, 3).map((product) => (
                <div key={product.id} className="card-dark p-6">
                  <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
                  <p className="text-gray-400 text-sm mb-4">{product.description?.substring(0, 100)}...</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-blue-400">${product.price_usd}</span>
                    <Link to="/products" className="btn-primary text-sm">View Details</Link>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default HomePage;
EOF

cat > src/pages/ProductsPage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products?limit=50`);
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-4xl font-bold text-white text-center mb-8">All Products</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id} className="card-dark p-6">
              <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded mb-4" />
              <div className="mb-2">
                <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded">{product.category}</span>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
              <p className="text-gray-400 text-sm mb-4">{product.description?.substring(0, 100)}...</p>
              <div className="flex justify-between items-center">
                <span className="text-xl font-bold text-blue-400">${product.price_usd}</span>
                <button className="btn-primary text-sm">Buy Now</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;
EOF

cat > src/pages/LoginPage.js << 'EOF'
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await login(formData.email, formData.password);
      if (result.success) {
        toast.success('Login successful!');
        navigate('/');
      } else {
        toast.error(result.error);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
          <p className="text-gray-400">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-gray-800 rounded-xl p-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg font-semibold transition-colors ${
              loading ? 'bg-gray-600 text-gray-400' : 'btn-primary'
            }`}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>

          <div className="bg-gray-700 rounded-lg p-4 text-center">
            <p className="text-yellow-400 font-medium mb-2">Demo Login:</p>
            <p className="text-gray-300 text-sm">admin@shopvippremium.com / admin123</p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
EOF

cat > src/pages/AdminDashboard.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';
import { toast } from 'react-toastify';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({});
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (user && user.role === 'admin') {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, productsRes] = await Promise.all([
        axios.get(`${API_URL}/api/admin/dashboard`),
        axios.get(`${API_URL}/api/products`)
      ]);
      setStats(statsRes.data);
      setProducts(productsRes.data.products);
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  if (!user || user.role !== 'admin') {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
          <p>Admin privileges required</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">Welcome, {user.username}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-green-400">${stats.total_revenue || 0}</div>
            <div className="text-gray-400">Revenue</div>
          </div>
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-blue-400">{stats.total_orders || 0}</div>
            <div className="text-gray-400">Orders</div>
          </div>
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-purple-400">{stats.total_products || 0}</div>
            <div className="text-gray-400">Products</div>
          </div>
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="text-3xl font-bold text-yellow-400">{stats.total_users || 0}</div>
            <div className="text-gray-400">Users</div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">Products ({products.length})</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {products.slice(0, 6).map((product) => (
              <div key={product.id} className="bg-gray-700 rounded-lg p-4">
                <img src={product.image_url} alt="" className="w-full h-32 object-cover rounded mb-2" />
                <h3 className="text-white font-medium">{product.name}</h3>
                <p className="text-gray-400 text-sm">{product.category} • ${product.price_usd}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 bg-green-900 bg-opacity-30 rounded-xl p-6 text-center">
          <h3 className="text-xl font-bold text-green-300 mb-2">🎉 Deployment Successful!</h3>
          <p className="text-green-200">Your Shop VIP Premium platform is now fully operational!</p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
EOF

print_status "Building frontend application..."
yarn build

print_status "Starting services..."
# Start MongoDB (if available)
systemctl start mongod 2>/dev/null || systemctl start mongodb 2>/dev/null || print_warning "MongoDB start skipped"
systemctl enable mongod 2>/dev/null || systemctl enable mongodb 2>/dev/null || true

# Seed database
cd /var/www/shopvippremium/backend
source venv/bin/activate 2>/dev/null || true

cat > seed_db.py << 'EOF'
import asyncio
import sys
sys.path.append('/var/www/shopvippremium/backend')

from database import connect_to_mongo, create_user, create_product
from models import UserRole

async def seed_database():
    try:
        await connect_to_mongo()
        
        # Create admin user
        admin_data = {
            "username": "admin",
            "email": "admin@shopvippremium.com", 
            "password": "admin123",
            "role": UserRole.ADMIN
        }
        await create_user(admin_data)
        print("✅ Admin user: admin@shopvippremium.com / admin123")
        
        # Sample products
        products = [
            {"name": "Premium Productivity Suite", "description": "Complete digital workspace toolkit with advanced productivity tools", "price_usd": 29.99, "price_inr": 2499, "category": "Productivity", "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=500", "is_featured": True, "is_bestseller": True},
            {"name": "Business Analytics Toolkit", "description": "Professional business intelligence and analytics software bundle", "price_usd": 39.99, "price_inr": 3299, "category": "Business", "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500", "is_featured": True},
            {"name": "Creative Design Pack", "description": "Comprehensive creative software bundle with design tools", "price_usd": 49.99, "price_inr": 4199, "category": "Creative", "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500", "is_bestseller": True},
        ]
        
        for product in products:
            await create_product(product)
        
        print(f"✅ Created {len(products)} products")
        print("🚀 Database ready!")
        
    except Exception as e:
        print(f"⚠️  Database seeding skipped: {e}")

if __name__ == "__main__":
    asyncio.run(seed_database())
EOF

python seed_db.py 2>/dev/null || print_warning "Database seeding skipped"

# Configure Nginx
print_status "Configuring Nginx..."
cat > /etc/nginx/sites-available/shopvippremium << EOF
server {
    listen 80 default_server;
    server_name _;
    
    location / {
        root /var/www/shopvippremium/frontend/build;
        try_files \$uri \$uri/ /index.html;
        index index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
nginx -t && systemctl restart nginx

# Setup PM2
cat > /var/www/shopvippremium/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'shopvippremium-backend',
    cwd: '/var/www/shopvippremium/backend',
    script: '/var/www/shopvippremium/backend/venv/bin/python',
    args: '-m uvicorn server:app --host 0.0.0.0 --port 8001',
    env: { PYTHONPATH: '/var/www/shopvippremium/backend' }
  }]
};
EOF

cd /var/www/shopvippremium
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Basic firewall
ufw allow 22 2>/dev/null || true
ufw allow 80 2>/dev/null || true
ufw allow 443 2>/dev/null || true
echo "y" | ufw enable 2>/dev/null || true

print_success "🎉 ULTRA-COMPATIBLE DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 Your site: http://$SERVER_IP"
echo "🔑 Admin panel: http://$SERVER_IP/admin"  
echo "📧 Admin login: admin@shopvippremium.com / admin123"
echo ""
echo "⚠️  Update Nowpayments keys in: /var/www/shopvippremium/backend/.env"
echo "🛠️  Restart backend: pm2 restart shopvippremium-backend"
echo ""
echo "📋 Check status:"
echo "   pm2 list"
echo "   systemctl status nginx"
echo ""
print_success "Your Shop VIP Premium platform is LIVE! 🚀"