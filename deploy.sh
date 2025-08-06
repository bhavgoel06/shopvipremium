#!/bin/bash

# Shop VIP Premium - One-Click Deployment Script
# This script deploys the complete e-commerce application to your VPS

set -e

echo "🚀 Starting Shop VIP Premium Deployment..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run this script as root (use sudo)"
    exit 1
fi

# Get server IP
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')

print_status "Detected Server IP: $SERVER_IP"

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install essential packages
print_status "Installing essential packages..."
apt install -y curl wget gnupg2 software-properties-common apt-transport-https ca-certificates lsb-release

# Install Node.js 20
print_status "Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Yarn
print_status "Installing Yarn..."
npm install -g yarn

# Install Python 3.11 and pip
print_status "Installing Python 3.11..."
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip build-essential

# Install MongoDB 7.0
print_status "Installing MongoDB 7.0..."
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
apt update
apt install -y mongodb-org

# Install Nginx
print_status "Installing Nginx..."
apt install -y nginx

# Install PM2
print_status "Installing PM2..."
npm install -g pm2

# Create application directory
print_status "Creating application directory..."
mkdir -p /var/www/shopvippremium
cd /var/www/shopvippremium

# Create project structure
print_status "Creating project structure..."
mkdir -p backend frontend

print_status "Creating backend files..."

# Create backend requirements.txt
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

# Create backend .env
cat > backend/.env << EOF
MONGO_URL=mongodb://localhost:27017/shopvippremium
DB_NAME=shopvippremium
SECRET_KEY=your-super-secret-key-change-this-in-production
BACKEND_URL=http://$SERVER_IP:8001
FRONTEND_URL=http://$SERVER_IP
NOWPAYMENTS_IPN_SECRET=your_nowpayments_ipn_secret
NOWPAYMENTS_PRIVATE_KEY=your_nowpayments_private_key
NOWPAYMENTS_PUBLIC_KEY=your_nowpayments_public_key
EOF

print_warning "⚠️  IMPORTANT: Please update the Nowpayments API keys in backend/.env before running the application"

# Create Python virtual environment
print_status "Setting up Python virtual environment..."
cd backend
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create backend models.py
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

# Create backend database.py
cat > database.py << 'EOF'
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from models import User, Product, Order, Payment, UserRole, OrderStatus, PaymentStatus
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME", "shopvippremium")
    
    db.client = AsyncIOMotorClient(mongo_url)
    db.database = db.client[db_name]
    
    print(f"Connected to MongoDB at {mongo_url}")

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()

# User operations
async def create_user(user_data: dict) -> str:
    """Create a new user"""
    user_data["hashed_password"] = pwd_context.hash(user_data["password"])
    del user_data["password"]
    
    user = User(**user_data)
    result = await db.database.users.insert_one(user.dict())
    return user.id

async def get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email"""
    return await db.database.users.find_one({"email": email})

async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by ID"""
    return await db.database.users.find_one({"id": user_id})

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

# Product operations
async def create_product(product_data: dict) -> str:
    """Create a new product"""
    product = Product(**product_data)
    await db.database.products.insert_one(product.dict())
    return product.id

async def get_products(skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[dict]:
    """Get products with pagination and filtering"""
    query = {}
    if category:
        query["category"] = category
    
    cursor = db.database.products.find(query).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def get_product_by_id(product_id: str) -> Optional[dict]:
    """Get product by ID"""
    return await db.database.products.find_one({"id": product_id})

async def update_product(product_id: str, update_data: dict) -> bool:
    """Update product"""
    result = await db.database.products.update_one(
        {"id": product_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

async def delete_product(product_id: str) -> bool:
    """Delete product"""
    result = await db.database.products.delete_one({"id": product_id})
    return result.deleted_count > 0

async def get_featured_products() -> List[dict]:
    """Get featured products"""
    cursor = db.database.products.find({"is_featured": True})
    return await cursor.to_list(length=None)

async def get_bestseller_products() -> List[dict]:
    """Get bestseller products"""
    cursor = db.database.products.find({"is_bestseller": True})
    return await cursor.to_list(length=None)

# Order operations
async def create_order(order_data: dict) -> str:
    """Create a new order"""
    order = Order(**order_data)
    await db.database.orders.insert_one(order.dict())
    return order.id

async def get_order_by_id(order_id: str) -> Optional[dict]:
    """Get order by ID"""
    return await db.database.orders.find_one({"id": order_id})

async def update_order_status(order_id: str, status: OrderStatus) -> bool:
    """Update order status"""
    result = await db.database.orders.update_one(
        {"id": order_id},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

async def get_user_orders(user_id: str) -> List[dict]:
    """Get orders for a user"""
    cursor = db.database.orders.find({"user_id": user_id}).sort("created_at", -1)
    return await cursor.to_list(length=None)

# Payment operations
async def create_payment(payment_data: dict) -> str:
    """Create a new payment"""
    payment = Payment(**payment_data)
    await db.database.payments.insert_one(payment.dict())
    return payment.id

async def get_payment_by_order_id(order_id: str) -> Optional[dict]:
    """Get payment by order ID"""
    return await db.database.payments.find_one({"order_id": order_id})

async def update_payment_status(payment_id: str, status: PaymentStatus, payment_id_external: Optional[str] = None) -> bool:
    """Update payment status"""
    update_data = {"status": status, "updated_at": datetime.utcnow()}
    if payment_id_external:
        update_data["payment_id"] = payment_id_external
    
    result = await db.database.payments.update_one(
        {"id": payment_id},
        {"$set": update_data}
    )
    return result.modified_count > 0

# Admin operations
async def get_dashboard_stats() -> dict:
    """Get admin dashboard statistics"""
    total_users = await db.database.users.count_documents({})
    total_products = await db.database.products.count_documents({})
    total_orders = await db.database.orders.count_documents({})
    
    # Calculate revenue from completed orders
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
    """Get all orders for admin"""
    cursor = db.database.orders.find({}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

async def get_users(skip: int = 0, limit: int = 50) -> List[dict]:
    """Get all users for admin"""
    cursor = db.database.users.find({}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
EOF

# Create backend nowpayments_service.py
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
        """Get list of available cryptocurrencies"""
        try:
            response = requests.get(f"{self.base_url}/currencies")
            response.raise_for_status()
            return response.json().get("currencies", [])
        except Exception as e:
            print(f"Error fetching currencies: {e}")
            return []
    
    def get_estimate(self, amount: float, currency_from: str = "usd", currency_to: str = "btc") -> Optional[Dict]:
        """Get estimated amount for crypto payment"""
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
        """Create a new payment"""
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
        """Get payment status"""
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
        """Verify IPN signature"""
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

# Create backend server.py (Part 1)
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

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Shop VIP Premium API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
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

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Authentication endpoints
@app.post("/api/auth/register")
async def register(user_data: dict):
    # Check if user already exists
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

# Product endpoints
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

# Order endpoints
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
    
    # Check if user owns the order or is admin
    if order["user_id"] != current_user["id"] and current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return order

@app.get("/api/orders")
async def get_user_orders_endpoint(current_user: dict = Depends(get_current_user)):
    orders = await get_user_orders(current_user["id"])
    return {"orders": orders}

# Payment endpoints
@app.post("/api/payments/crypto")
async def create_crypto_payment(payment_data: dict, current_user: dict = Depends(get_current_user)):
    order = await get_order_by_id(payment_data["order_id"])
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create payment in Nowpayments
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
    
    # Save payment to database
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
        # Update order and payment status
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

# Admin endpoints
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

# Move to frontend directory
cd ../frontend

print_status "Creating frontend files..."

# Create package.json
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
    "extends": [
      "react-app",
      "react-app/jest"
    ]
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
  },
  "devDependencies": {
    "tailwindcss": "^3.3.6",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10"
  },
  "proxy": "http://localhost:8001"
}
EOF

# Create frontend .env
cat > .env << EOF
REACT_APP_BACKEND_URL=http://$SERVER_IP:8001
GENERATE_SOURCEMAP=false
EOF

# Install frontend dependencies
print_status "Installing frontend dependencies..."
yarn install

# Create Tailwind CSS config
yarn add -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        dark: {
          800: '#1f2937',
          900: '#111827',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
EOF

# Create public directory and files
mkdir -p public src/components src/pages src/context

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
  <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
  <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
  <title>Shop VIP Premium - Digital Workspace Toolkit</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Store",
    "name": "Shop VIP Premium",
    "description": "Premium Digital Workspace Toolkit",
    "url": "https://shopvippremium.com"
  }
  </script>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
EOF

# Create basic source files (this will be generated by a separate command to avoid size limits)
print_status "Frontend directory structure created. Application files will be created next..."

# Create MongoDB service file
print_status "Configuring MongoDB..."
systemctl start mongod
systemctl enable mongod

# Create database seeding script
cat > /tmp/seed_database.py << 'EOF'
import asyncio
import os
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
    print("Admin user created: admin@shopvippremium.com / admin123")
    
    # Create sample products
    products = [
        {
            "name": "Premium Productivity Suite",
            "description": "Complete digital workspace toolkit with advanced productivity tools, project management software, and collaboration utilities designed for professionals and freelancers.",
            "price_usd": 29.99,
            "price_inr": 2499.00,
            "category": "Productivity",
            "image_url": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=500",
            "is_featured": True,
            "is_bestseller": True
        },
        {
            "name": "Business Analytics Toolkit",
            "description": "Professional business intelligence and analytics software bundle for data-driven decision making and performance optimization.",
            "price_usd": 39.99,
            "price_inr": 3299.00,
            "category": "Business",
            "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500",
            "is_featured": True
        },
        {
            "name": "Creative Design Pack",
            "description": "Comprehensive creative software bundle including graphic design tools, video editing software, and digital art applications.",
            "price_usd": 49.99,
            "price_inr": 4199.00,
            "category": "Creative",
            "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500",
            "is_bestseller": True
        },
        {
            "name": "Developer Tools Collection",
            "description": "Essential development tools and utilities for software developers, including code editors, debugging tools, and development frameworks.",
            "price_usd": 34.99,
            "price_inr": 2899.00,
            "category": "Development",
            "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=500"
        },
        {
            "name": "Marketing Automation Suite",
            "description": "Complete digital marketing toolkit with automation tools, analytics platforms, and campaign management utilities.",
            "price_usd": 44.99,
            "price_inr": 3799.00,
            "category": "Marketing",
            "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500",
            "is_featured": True
        }
    ]
    
    for product in products:
        await create_product(product)
    
    print(f"Created {len(products)} sample products")
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_database())
EOF

# Run database seeding
print_status "Seeding database with initial data..."
cd /var/www/shopvippremium/backend
source venv/bin/activate
python3 /tmp/seed_database.py

# Create Nginx configuration
print_status "Configuring Nginx..."
cat > /etc/nginx/sites-available/shopvippremium << EOF
server {
    listen 80;
    server_name $SERVER_IP;
    
    # Frontend
    location / {
        root /var/www/shopvippremium/frontend/build;
        try_files \$uri \$uri/ /index.html;
        index index.html;
    }
    
    # Backend API
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
    
    # Static files
    location /static {
        root /var/www/shopvippremium/frontend/build;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable Nginx site
ln -sf /etc/nginx/sites-available/shopvippremium /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# Create PM2 ecosystem file
print_status "Configuring PM2..."
cat > /var/www/shopvippremium/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'shopvippremium-backend',
    cwd: '/var/www/shopvippremium/backend',
    script: '/var/www/shopvippremium/backend/venv/bin/python',
    args: '-m uvicorn server:app --host 0.0.0.0 --port 8001 --reload',
    env: {
      PYTHONPATH: '/var/www/shopvippremium/backend'
    },
    error_file: '/var/log/pm2/shopvippremium-backend.err.log',
    out_file: '/var/log/pm2/shopvippremium-backend.out.log',
    log_file: '/var/log/pm2/shopvippremium-backend.log'
  }]
};
EOF

mkdir -p /var/log/pm2

# Set up firewall
print_status "Configuring firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

print_success "Base deployment completed!"
print_warning "Next steps:"
echo "1. Run: cd /var/www/shopvippremium && curl -sSL https://raw.githubusercontent.com/shopvippremium/deploy/main/create-frontend-files.sh | bash"
echo "2. Update Nowpayments API keys in /var/www/shopvippremium/backend/.env"
echo "3. Start services with: cd /var/www/shopvippremium && pm2 start ecosystem.config.js"
echo ""
echo "🌐 Your site will be available at: http://$SERVER_IP"
echo "🔑 Admin login: admin@shopvippremium.com / admin123"
echo ""
print_success "Deployment script completed successfully!"
EOF
    </file>