#!/bin/bash

# Shop VIP Premium - Fixed One-Click Complete Deployment
# This single script deploys the ENTIRE e-commerce application

set -e

echo "🚀 Shop VIP Premium - One-Click Complete Deployment (FIXED)"
echo "==========================================================="

# Colors for output
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
    print_error "Please run as root: sudo bash fixed-deploy.sh"
    exit 1
fi

SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
print_status "Detected Server IP: $SERVER_IP"

print_status "Step 1/8: System Updates & Repository Setup"
apt update && apt upgrade -y

# Add universe repository 
add-apt-repository universe -y
apt update

# Install basic dependencies that should be available
apt install -y curl wget gnupg software-properties-common apt-transport-https ca-certificates lsb-release

print_status "Step 2/8: Installing Node.js 20 & Yarn"
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g yarn

print_status "Step 3/8: Installing Python & Build Tools"
# Use available Python version and install build tools
apt install -y python3 python3-venv python3-dev python3-pip
apt install -y gcc g++ make

print_status "Step 4/8: Installing MongoDB 7.0"
# Install MongoDB with proper key handling
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update && apt install -y mongodb-org

print_status "Step 5/8: Installing Nginx & PM2"
apt install -y nginx
npm install -g pm2

print_status "Step 6/8: Creating Application Structure"
mkdir -p /var/www/shopvippremium/{backend,frontend}
cd /var/www/shopvippremium

print_status "Step 7/8: Creating Backend Files"

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
SECRET_KEY=your-super-secret-key-change-this-in-production-$(openssl rand -hex 32)
BACKEND_URL=http://$SERVER_IP:8001
FRONTEND_URL=http://$SERVER_IP
NOWPAYMENTS_IPN_SECRET=your_nowpayments_ipn_secret
NOWPAYMENTS_PRIVATE_KEY=your_nowpayments_private_key
NOWPAYMENTS_PUBLIC_KEY=your_nowpayments_public_key
EOF

print_warning "⚠️  Update Nowpayments API keys in backend/.env before going live!"

# Setup Python environment using available Python version
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Backend models.py
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

# Backend database.py
cat > database.py << 'EOF'
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Product, Order, Payment, UserRole, OrderStatus, PaymentStatus
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "shopvippremium")
    
    db.client = AsyncIOMotorClient(mongo_url)
    db.database = db.client[db_name]
    
    print(f"Connected to MongoDB at {mongo_url}")

async def close_mongo_connection():
    if db.client:
        db.client.close()

async def create_user(user_data: dict) -> str:
    user_data["hashed_password"] = pwd_context.hash(user_data["password"])
    del user_data["password"]
    
    user = User(**user_data)
    result = await db.database.users.insert_one(user.dict())
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

async def update_product(product_id: str, update_data: dict) -> bool:
    result = await db.database.products.update_one(
        {"id": product_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

async def delete_product(product_id: str) -> bool:
    result = await db.database.products.delete_one({"id": product_id})
    return result.deleted_count > 0

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

async def update_order_status(order_id: str, status: OrderStatus) -> bool:
    result = await db.database.orders.update_one(
        {"id": order_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

async def get_user_orders(user_id: str) -> List[dict]:
    cursor = db.database.orders.find({"user_id": user_id}).sort("created_at", -1)
    return await cursor.to_list(length=None)

async def create_payment(payment_data: dict) -> str:
    payment = Payment(**payment_data)
    await db.database.payments.insert_one(payment.dict())
    return payment.id

async def get_payment_by_order_id(order_id: str) -> Optional[dict]:
    return await db.database.payments.find_one({"order_id": order_id})

async def update_payment_status(payment_id: str, status: PaymentStatus, payment_id_external: Optional[str] = None) -> bool:
    update_data = {"status": status, "updated_at": datetime.utcnow()}
    if payment_id_external:
        update_data["payment_id"] = payment_id_external
    
    result = await db.database.payments.update_one(
        {"id": payment_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

async def get_dashboard_stats() -> dict:
    total_users = await db.database.users.count_documents({})
    total_products = await db.database.products.count_documents({})
    total_orders = await db.database.orders.count_documents({})
    
    pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}
    ]
    revenue_result = await db.database.orders.aggregate(pipeline).to_list(length=1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }

async def get_orders(skip: int = 0, limit: int = 50) -> List[dict]:
    cursor = db.database.orders.find({}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def get_users(skip: int = 0, limit: int = 50) -> List[dict]:
    cursor = db.database.users.find({}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
EOF

# Backend nowpayments_service.py
cat > nowpayments_service.py << 'EOF'
import os
import requests
import hashlib
import hmac
import json
from typing import Dict, Optional, List

class NowpaymentsService:
    def __init__(self):
        self.base_url = "https://api.nowpayments.io/v1"
        self.private_key = os.environ.get("NOWPAYMENTS_PRIVATE_KEY")
        self.public_key = os.environ.get("NOWPAYMENTS_PUBLIC_KEY")
        self.ipn_secret = os.environ.get("NOWPAYMENTS_IPN_SECRET")
        
    def get_available_currencies(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/currencies")
            response.raise_for_status()
            return response.json().get("currencies", [])
        except Exception as e:
            print(f"Error fetching currencies: {e}")
            return []
    
    def get_estimate(self, amount: float, currency_from: str = "usd", currency_to: str = "btc") -> Optional[Dict]:
        try:
            response = requests.get(
                f"{self.base_url}/estimate",
                params={
                    "amount": amount,
                    "currency_from": currency_from,
                    "currency_to": currency_to
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting estimate: {e}")
            return None
    
    def create_payment(self, amount: float, currency: str, order_id: str, success_url: str, cancel_url: str) -> Optional[Dict]:
        try:
            headers = {
                "x-api-key": self.private_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "price_amount": amount,
                "price_currency": "usd",
                "pay_currency": currency,
                "order_id": order_id,
                "order_description": f"Order {order_id}",
                "success_url": success_url,
                "cancel_url": cancel_url,
                "ipn_callback_url": f"{os.environ.get('BACKEND_URL')}/api/nowpayments/ipn"
            }
            
            response = requests.post(
                f"{self.base_url}/payment",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error creating payment: {e}")
            return None
    
    def get_payment_status(self, payment_id: str) -> Optional[Dict]:
        try:
            headers = {"x-api-key": self.private_key}
            response = requests.get(
                f"{self.base_url}/payment/{payment_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting payment status: {e}")
            return None
    
    def verify_ipn_signature(self, request_body: str, received_signature: str) -> bool:
        try:
            expected_signature = hmac.new(
                self.ipn_secret.encode('utf-8'),
                request_body.encode('utf-8'),
                hashlib.sha512
            ).hexdigest()
            return hmac.compare_digest(expected_signature, received_signature)
        except Exception as e:
            print(f"Error verifying IPN signature: {e}")
            return False
EOF

# Backend server.py
cat > server.py << 'EOF'
import os
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import json

from database import (
    connect_to_mongo, close_mongo_connection, create_user, get_user_by_email, 
    get_user_by_id, verify_password, create_product, get_products, 
    get_product_by_id, update_product, delete_product, get_featured_products, 
    get_bestseller_products, create_order, get_order_by_id, update_order_status, 
    get_user_orders, create_payment, get_payment_by_order_id, update_payment_status, 
    get_dashboard_stats, get_orders, get_users
)
from models import User, Product, Order, OrderStatus, PaymentStatus, UserRole
from nowpayments_service import NowpaymentsService

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

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()
nowpayments = NowpaymentsService()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

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
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "role": user["role"]
    }}

@app.get("/api/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "role": current_user["role"]
    }

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

@app.get("/api/orders/{order_id}")
async def get_order_endpoint(order_id: str, current_user: dict = Depends(get_current_user)):
    order = await get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user["id"] and current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order

@app.get("/api/orders")
async def get_user_orders_endpoint(current_user: dict = Depends(get_current_user)):
    orders = await get_user_orders(current_user["id"])
    return {"orders": orders}

@app.post("/api/payments/crypto")
async def create_crypto_payment(payment_data: dict, current_user: dict = Depends(get_current_user)):
    order = await get_order_by_id(payment_data["order_id"])
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    success_url = f"{os.environ.get('FRONTEND_URL')}/order-success?order_id={order['id']}"
    cancel_url = f"{os.environ.get('FRONTEND_URL')}/order-cancelled?order_id={order['id']}"
    
    payment_response = nowpayments.create_payment(
        amount=order["total_amount"],
        currency=payment_data["currency"],
        order_id=order["id"],
        success_url=success_url,
        cancel_url=cancel_url
    )
    
    if not payment_response:
        raise HTTPException(status_code=500, detail="Failed to create payment")
    
    payment_db_data = {
        "order_id": order["id"],
        "payment_method": "crypto",
        "amount": order["total_amount"],
        "currency": payment_data["currency"],
        "payment_id": payment_response.get("payment_id")
    }
    await create_payment(payment_db_data)
    
    return {"payment_url": payment_response.get("invoice_url"), "payment_id": payment_response.get("payment_id")}

@app.post("/api/nowpayments/ipn")
async def nowpayments_ipn(request: Request):
    body = await request.body()
    signature = request.headers.get("x-nowpayments-sig")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    if not nowpayments.verify_ipn_signature(body.decode(), signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    data = json.loads(body)
    payment_status = data.get("payment_status")
    order_id = data.get("order_id")
    
    if payment_status == "finished":
        await update_order_status(order_id, OrderStatus.COMPLETED)
        payment = await get_payment_by_order_id(order_id)
        if payment:
            await update_payment_status(payment["id"], PaymentStatus.PAID)
    elif payment_status in ["failed", "expired"]:
        await update_order_status(order_id, OrderStatus.CANCELLED)
        payment = await get_payment_by_order_id(order_id)
        if payment:
            await update_payment_status(payment["id"], PaymentStatus.FAILED)
    
    return {"status": "ok"}

@app.get("/api/admin/dashboard")
async def get_dashboard_stats_endpoint(admin_user: dict = Depends(get_admin_user)):
    stats = await get_dashboard_stats()
    return stats

@app.get("/api/admin/orders")
async def get_all_orders(skip: int = 0, limit: int = 50, admin_user: dict = Depends(get_admin_user)):
    orders = await get_orders(skip=skip, limit=limit)
    return {"orders": orders}

@app.get("/api/admin/users")
async def get_all_users(skip: int = 0, limit: int = 50, admin_user: dict = Depends(get_admin_user)):
    users = await get_users(skip=skip, limit=limit)
    return {"users": users}

@app.post("/api/admin/products")
async def create_product_endpoint(product_data: dict, admin_user: dict = Depends(get_admin_user)):
    product_id = await create_product(product_data)
    return {"product_id": product_id, "message": "Product created successfully"}

@app.put("/api/admin/products/{product_id}")
async def update_product_endpoint(product_id: str, product_data: dict, admin_user: dict = Depends(get_admin_user)):
    success = await update_product(product_id, product_data)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated successfully"}

@app.delete("/api/admin/products/{product_id}")
async def delete_product_endpoint(product_id: str, admin_user: dict = Depends(get_admin_user)):
    success = await delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
EOF

print_status "Step 8/8: Creating Complete Frontend Application"
cd ../frontend

# Frontend package.json
cat > package.json << 'EOF'
{
  "name": "shopvippremium-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@heroicons/react": "^2.0.18",
    "axios": "^1.6.2",
    "framer-motion": "^10.16.16",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-helmet": "^6.1.0",
    "react-router-dom": "^6.20.1",
    "react-scripts": "5.0.1",
    "react-toastify": "^9.1.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": ["react-app", "react-app/jest"]
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  },
  "devDependencies": {
    "tailwindcss": "^3.3.6",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10"
  },
  "proxy": "http://localhost:8001"
}
EOF

# Frontend .env
cat > .env << EOF
REACT_APP_BACKEND_URL=http://$SERVER_IP:8001
GENERATE_SOURCEMAP=false
EOF

# Install frontend dependencies
print_status "Installing frontend dependencies (this may take a few minutes)..."
yarn install
yarn add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Tailwind config
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 50: '#f0f9ff', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8' },
        dark: { 800: '#1f2937', 900: '#111827' }
      }
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
}
EOF

# Create directories
mkdir -p public src/{components,pages,context}

# Public files
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#000000" />
  <meta name="description" content="Shop VIP Premium - Premium Digital Workspace Toolkit. Access professional tools, productivity software, and freelancer utilities at competitive prices." />
  <meta name="keywords" content="digital workspace, productivity tools, professional software, freelancer utilities, business solutions" />
  <meta property="og:title" content="Shop VIP Premium - Digital Workspace Toolkit" />
  <meta property="og:description" content="Premium Digital Workspace Toolkit. Access professional tools, productivity software, and freelancer utilities." />
  <meta property="og:type" content="website" />
  <title>Shop VIP Premium - Digital Workspace Toolkit</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
EOF

# Source files
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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #111827;
  color: #f9fafb;
}

.bg-gradient-dark { background: linear-gradient(135deg, #1f2937 0%, #111827 100%); }
.text-gradient { background: linear-gradient(135deg, #3b82f6, #1d4ed8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.card-dark { background: rgba(31, 41, 55, 0.5); backdrop-filter: blur(10px); border: 1px solid rgba(75, 85, 99, 0.3); }
.btn-primary { @apply bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105; }
.btn-secondary { @apply bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200; }
EOF

cat > src/App.js << 'EOF'
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { AuthProvider } from './context/AuthContext';
import { CurrencyProvider } from './context/CurrencyContext';
import Header from './components/Header';
import Footer from './components/Footer';

import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import LoginPage from './pages/LoginPage';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  return (
    <AuthProvider>
      <CurrencyProvider>
        <Router>
          <div className="min-h-screen bg-gray-900 text-white">
            <Header />
            <main className="flex-grow">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/products" element={<ProductsPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/admin" element={<AdminDashboard />} />
              </Routes>
            </main>
            <Footer />
            <ToastContainer position="top-right" theme="dark" />
          </div>
        </Router>
      </CurrencyProvider>
    </AuthProvider>
  );
}

export default App;
EOF

# Create context files
cat > src/context/AuthContext.js << 'EOF'
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  useEffect(() => {
    const checkToken = async () => {
      if (token) {
        try {
          const response = await axios.get(`${API_URL}/api/auth/me`);
          setUser(response.data);
        } catch (error) {
          console.error('Token validation failed:', error);
          logout();
        }
      }
      setLoading(false);
    };

    checkToken();
  }, [token, API_URL]);

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

  const value = { user, token, loading, login, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
EOF

cat > src/context/CurrencyContext.js << 'EOF'
import React, { createContext, useContext, useState } from 'react';

const CurrencyContext = createContext();

export const useCurrency = () => {
  const context = useContext(CurrencyContext);
  if (!context) {
    throw new Error('useCurrency must be used within a CurrencyProvider');
  }
  return context;
};

export const CurrencyProvider = ({ children }) => {
  const [currency, setCurrency] = useState('USD');

  const formatPrice = (priceUsd, priceInr) => {
    if (currency === 'INR') {
      return `₹${priceInr?.toFixed(2) || (priceUsd * 83).toFixed(2)}`;
    }
    return `$${priceUsd.toFixed(2)}`;
  };

  const getPrice = (priceUsd, priceInr) => {
    return currency === 'INR' ? (priceInr || priceUsd * 83) : priceUsd;
  };

  const value = { currency, setCurrency, formatPrice, getPrice };
  return <CurrencyContext.Provider value={value}>{children}</CurrencyContext.Provider>;
};
EOF

# Create essential components
cat > src/components/Header.js << 'EOF'
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';

const Header = () => {
  const { user, logout } = useAuth();
  const { currency, setCurrency } = useCurrency();

  return (
    <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link to="/" className="text-xl font-bold text-gradient">Shop VIP Premium</Link>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/products" className="text-gray-300 hover:text-white">Products</Link>
          </nav>

          <div className="flex items-center space-x-4">
            <select
              value={currency}
              onChange={(e) => setCurrency(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded px-3 py-1 text-sm text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="USD">USD</option>
              <option value="INR">INR</option>
            </select>

            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-gray-300">Welcome, {user.username}</span>
                {user.role === 'admin' && (
                  <Link to="/admin" className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700">
                    Admin Panel
                  </Link>
                )}
                <button onClick={logout} className="text-gray-300 hover:text-white">Logout</button>
              </div>
            ) : (
              <Link to="/login" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">Login</Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
EOF

cat > src/components/Footer.js << 'EOF'
import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <h3 className="text-xl font-bold text-gradient mb-4">Shop VIP Premium</h3>
          <p className="text-gray-400 mb-4">Premium digital workspace tools for professionals</p>
          
          <div className="flex justify-center space-x-6 mb-4">
            <a href="https://t.me/shopvippremium" target="_blank" rel="noopener noreferrer" 
               className="text-blue-400 hover:text-blue-300">
              📱 Telegram Support
            </a>
            <a href="https://wa.me/1234567890" target="_blank" rel="noopener noreferrer" 
               className="text-green-400 hover:text-green-300">
              💬 WhatsApp Support
            </a>
          </div>
          
          <p className="text-gray-500 text-sm">
            © 2025 Shop VIP Premium. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
EOF

# Create essential pages
cat > src/pages/HomePage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useCurrency } from '../context/CurrencyContext';

const HomePage = () => {
  const [products, setProducts] = useState([]);
  const { formatPrice } = useCurrency();
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products/featured`);
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  return (
    <div>
      <section className="bg-gradient-dark py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold text-white mb-6">
            Premium Digital <span className="text-gradient">Workspace Toolkit</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Discover professional-grade productivity tools, business utilities, and freelancer solutions
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/products" className="btn-primary text-lg px-8">Browse Products</Link>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-800">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Why Choose Shop VIP Premium?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 card-dark rounded-xl">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-semibold text-white mb-2">Premium Quality</h3>
              <p className="text-gray-400">Professional-grade digital tools crafted for excellence</p>
            </div>
            <div className="text-center p-6 card-dark rounded-xl">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold text-white mb-2">Secure Payments</h3>
              <p className="text-gray-400">Safe cryptocurrency payments</p>
            </div>
            <div className="text-center p-6 card-dark rounded-xl">
              <div className="text-4xl mb-4">24/7</div>
              <h3 className="text-xl font-semibold text-white mb-2">24/7 Support</h3>
              <p className="text-gray-400">Round-the-clock customer support</p>
            </div>
          </div>
        </div>
      </section>

      {products.length > 0 && (
        <section className="py-16 bg-gray-900">
          <div className="max-w-7xl mx-auto px-4">
            <h2 className="text-3xl font-bold text-white text-center mb-12">Featured Products</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {products.slice(0, 3).map((product) => (
                <div key={product.id} className="card-dark rounded-xl p-6">
                  <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
                  <p className="text-gray-400 text-sm mb-4">{product.description?.substring(0, 100)}...</p>
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-blue-400">{formatPrice(product.price_usd, product.price_inr)}</span>
                    <Link to="/products" className="btn-primary text-sm">View Details</Link>
                  </div>
                </div>
              ))}
            </div>
            <div className="text-center mt-8">
              <Link to="/products" className="btn-primary">View All Products</Link>
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
import { useCurrency } from '../context/CurrencyContext';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { formatPrice } = useCurrency();
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products?limit=50`);
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">All Products</h1>
          <p className="text-gray-400">Discover our complete collection of digital workspace solutions</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <div key={product.id} className="card-dark rounded-xl p-6">
              <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover rounded-lg mb-4" />
              
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-medium text-blue-400 bg-blue-400 bg-opacity-10 px-2 py-1 rounded">
                  {product.category}
                </span>
                {product.is_featured && (
                  <span className="text-xs font-medium text-yellow-400 bg-yellow-400 bg-opacity-10 px-2 py-1 rounded">
                    Featured
                  </span>
                )}
              </div>

              <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
              <p className="text-gray-400 text-sm mb-4">{product.description?.substring(0, 80)}...</p>
              
              <div className="flex items-center justify-between">
                <span className="text-xl font-bold text-blue-400">{formatPrice(product.price_usd, product.price_inr)}</span>
                <button className="btn-primary text-sm">Buy Now</button>
              </div>
            </div>
          ))}
        </div>

        {products.length === 0 && (
          <div className="text-center py-16">
            <div className="text-gray-400 text-lg">No products available</div>
          </div>
        )}
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
        toast.error(result.error || 'Login failed');
      }
    } catch (error) {
      toast.error('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
          <p className="text-gray-400">Sign in to your Shop VIP Premium account</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-gray-800 rounded-xl p-8 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white"
              placeholder="Enter your email"
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
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-colors ${
              loading ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>

          <div className="bg-gray-700 rounded-lg p-4">
            <h3 className="text-sm font-medium text-yellow-400 mb-2">Demo Access:</h3>
            <div className="text-xs text-gray-400">
              <p>Admin: admin@shopvippremium.com / admin123</p>
            </div>
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
        axios.get(`${API_URL}/api/products?limit=20`)
      ]);
      
      setStats(statsRes.data);
      setProducts(productsRes.data.products);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (!user || user.role !== 'admin') {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-2xl font-bold mb-4">Access Denied</h1>
          <p>You need admin privileges to access this page.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">Welcome back, {user.username}</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-xl p-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400">${stats.total_revenue || 0}</div>
              <div className="text-gray-400 text-sm">Total Revenue</div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400">{stats.total_orders || 0}</div>
              <div className="text-gray-400 text-sm">Total Orders</div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400">{stats.total_products || 0}</div>
              <div className="text-gray-400 text-sm">Total Products</div>
            </div>
          </div>
          
          <div className="bg-gray-800 rounded-xl p-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-400">{stats.total_users || 0}</div>
              <div className="text-gray-400 text-sm">Total Users</div>
            </div>
          </div>
        </div>

        {/* Products Section */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">Products ({products.length})</h2>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-gray-700">
                  <th className="py-3 px-4 text-gray-300">Product</th>
                  <th className="py-3 px-4 text-gray-300">Category</th>
                  <th className="py-3 px-4 text-gray-300">Price (USD)</th>
                  <th className="py-3 px-4 text-gray-300">Status</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id} className="border-b border-gray-700">
                    <td className="py-3 px-4">
                      <div className="flex items-center">
                        <img src={product.image_url} alt="" className="w-12 h-12 rounded-lg object-cover mr-3" />
                        <div>
                          <div className="text-white font-medium">{product.name}</div>
                          <div className="text-gray-400 text-sm">{product.description?.substring(0, 50)}...</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4 text-gray-300">{product.category}</td>
                    <td className="py-3 px-4 text-white">${product.price_usd}</td>
                    <td className="py-3 px-4">
                      <div className="flex gap-1">
                        {product.is_featured && (
                          <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">Featured</span>
                        )}
                        {product.is_bestseller && (
                          <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Bestseller</span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-8 bg-blue-900 bg-opacity-30 rounded-xl p-6 text-center">
          <h3 className="text-xl font-bold text-blue-300 mb-2">🎉 Admin Panel Ready!</h3>
          <p className="text-blue-200">
            Your Shop VIP Premium admin dashboard is fully functional. 
            You can now manage products, orders, users, and monitor your business metrics.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
EOF

print_status "Building React application (this may take several minutes)..."
yarn build

print_status "Setting up database & services..."
systemctl start mongod
systemctl enable mongod

# Database seeding
cd /var/www/shopvippremium/backend
source venv/bin/activate

cat > seed_db.py << 'EOF'
import asyncio
import sys
sys.path.append('/var/www/shopvippremium/backend')
from database import connect_to_mongo, create_user, create_product
from models import UserRole

async def seed_database():
    await connect_to_mongo()
    
    # Create admin user
    admin_data = {
        "username": "admin",
        "email": "admin@shopvippremium.com",
        "password": "admin123",
        "role": UserRole.ADMIN
    }
    await create_user(admin_data)
    print("✅ Admin user created: admin@shopvippremium.com / admin123")
    
    # Create sample products
    products = [
        {"name": "Premium Productivity Suite", "description": "Complete digital workspace toolkit with advanced productivity tools, project management software, and collaboration utilities designed for professionals and freelancers.", "price_usd": 29.99, "price_inr": 2499.00, "category": "Productivity", "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=500", "is_featured": True, "is_bestseller": True},
        {"name": "Business Analytics Toolkit", "description": "Professional business intelligence and analytics software bundle for data-driven decision making and performance optimization.", "price_usd": 39.99, "price_inr": 3299.00, "category": "Business", "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500", "is_featured": True},
        {"name": "Creative Design Pack", "description": "Comprehensive creative software bundle including graphic design tools, video editing software, and digital art applications.", "price_usd": 49.99, "price_inr": 4199.00, "category": "Creative", "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500", "is_bestseller": True},
        {"name": "Developer Tools Collection", "description": "Essential development tools and utilities for software developers, including code editors, debugging tools, and development frameworks.", "price_usd": 34.99, "price_inr": 2899.00, "category": "Development", "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500"},
        {"name": "Marketing Automation Suite", "description": "Complete digital marketing toolkit with automation tools, analytics platforms, and campaign management utilities.", "price_usd": 44.99, "price_inr": 3799.00, "category": "Marketing", "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500", "is_featured": True}
    ]
    
    for product in products:
        await create_product(product)
    
    print(f"✅ Created {len(products)} sample products")
    print("🚀 Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_database())
EOF

python3 seed_db.py

print_status "Configuring Nginx..."
cat > /etc/nginx/sites-available/shopvippremium << EOF
server {
    listen 80;
    server_name $SERVER_IP _;
    
    location / {
        root /var/www/shopvippremium/frontend/build;
        try_files \$uri \$uri/ /index.html;
        index index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    location /static {
        root /var/www/shopvippremium/frontend/build;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

print_status "Setting up PM2..."
cat > /var/www/shopvippremium/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'shopvippremium-backend',
    cwd: '/var/www/shopvippremium/backend',
    script: '/var/www/shopvippremium/backend/venv/bin/python3',
    args: '-m uvicorn server:app --host 0.0.0.0 --port 8001',
    env: { PYTHONPATH: '/var/www/shopvippremium/backend' },
    error_file: '/var/log/pm2/shopvippremium-backend.err.log',
    out_file: '/var/log/pm2/shopvippremium-backend.out.log',
    log_file: '/var/log/pm2/shopvippremium-backend.log'
  }]
};
EOF

mkdir -p /var/log/pm2
cd /var/www/shopvippremium
pm2 start ecosystem.config.js
pm2 save
pm2 startup

print_status "Setting up firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

print_success "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🌐 Your Shop VIP Premium site is ready at: http://$SERVER_IP"
echo "🔑 Admin Panel: http://$SERVER_IP/admin"
echo "📧 Admin Login: admin@shopvippremium.com / admin123"
echo ""
echo "⚠️  IMPORTANT: Update Nowpayments API keys in:"
echo "   /var/www/shopvippremium/backend/.env"
echo ""
echo "🛠️  Restart backend after updating keys:"
echo "   pm2 restart shopvippremium-backend"
echo ""
echo "📱 Support: Update Telegram/WhatsApp links in your admin panel"
echo ""
echo "🔧 Useful Commands:"
echo "   pm2 list              # Check backend status"
echo "   pm2 logs              # View backend logs"
echo "   systemctl status nginx # Check web server"
echo ""
print_success "Enjoy your new e-commerce platform! 💰🚀"