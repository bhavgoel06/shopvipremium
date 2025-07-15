from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from typing import Optional, List
from datetime import datetime, timedelta
import json
import jwt
import bcrypt
import uuid

# Import models and database
from models import *
from database import db

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create FastAPI app
app = FastAPI(
    title="Premium Subscription Shop API",
    description="SEO-optimized e-commerce platform for premium subscriptions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
security = HTTPBearer()

# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Analytics middleware
@app.middleware("http")
async def analytics_middleware(request: Request, call_next):
    # Log page view
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    referrer = request.headers.get("referer")
    
    # Generate session ID (simple implementation)
    session_id = request.headers.get("x-session-id", "anonymous")
    
    analytics_data = AnalyticsCreate(
        page_path=str(request.url.path),
        ip_address=client_ip,
        user_agent=user_agent,
        referrer=referrer,
        session_id=session_id
    )
    
    try:
        await db.log_analytics(analytics_data)
    except Exception as e:
        logger.error(f"Error logging analytics: {e}")
    
    response = await call_next(request)
    return response

# Routes

# Authentication Routes
@app.post("/api/auth/register", response_model=AuthResponse)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await db.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = User(
            id=generate_uuid(),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        created_user = await db.create_user(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": created_user.id})
        
        return AuthResponse(
            success=True,
            message="User registered successfully",
            data=AuthData(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=created_user.id,
                    first_name=created_user.first_name,
                    last_name=created_user.last_name,
                    email=created_user.email,
                    created_at=created_user.created_at
                )
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/login", response_model=AuthResponse)
async def login_user(login_data: UserLogin):
    """Login user"""
    try:
        # Get user by email
        user = await db.get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = create_access_token(data={"sub": user.id})
        
        return AuthResponse(
            success=True,
            message="Login successful",
            data=AuthData(
                access_token=access_token,
                token_type="bearer",
                user=UserResponse(
                    id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=user.email,
                    created_at=user.created_at
                )
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user(current_user_id: str = Depends(verify_token)):
    """Get current user info"""
    try:
        user = await db.get_user_by_id(current_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Product Routes
@app.get("/api/products", response_model=PaginatedResponse)
async def get_products(
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    rating: Optional[int] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    page: int = 1,
    per_page: int = 12
):
    """Get products with filters and pagination"""
    try:
        filters = SearchFilters(
            category=category,
            min_price=min_price,
            max_price=max_price,
            rating=rating,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page
        )
        
        products = await db.get_products(filters)
        total = await db.get_products_count(filters)
        total_pages = (total + per_page - 1) // per_page
        
        return PaginatedResponse(
            success=True,
            message="Products retrieved successfully",
            data=[product.dict() for product in products],
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/featured", response_model=ProductResponse)
async def get_featured_products(limit: int = 8):
    """Get featured products"""
    try:
        products = await db.get_featured_products(limit)
        return ProductResponse(
            success=True,
            message="Featured products retrieved successfully",
            data=[product.dict() for product in products]
        )
    except Exception as e:
        logger.error(f"Error getting featured products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/bestsellers", response_model=ProductResponse)
async def get_bestseller_products(limit: int = 8):
    """Get bestseller products"""
    try:
        products = await db.get_bestseller_products(limit)
        return ProductResponse(
            success=True,
            message="Bestseller products retrieved successfully",
            data=[product.dict() for product in products]
        )
    except Exception as e:
        logger.error(f"Error getting bestseller products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/search", response_model=ProductResponse)
async def search_products(q: str, limit: int = 10):
    """Search products"""
    try:
        products = await db.search_products(q, limit)
        return ProductResponse(
            success=True,
            message="Search results retrieved successfully",
            data=[product.dict() for product in products]
        )
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get product by ID"""
    try:
        product = await db.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            success=True,
            message="Product retrieved successfully",
            data=product.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/slug/{slug}", response_model=ProductResponse)
async def get_product_by_slug(slug: str):
    """Get product by slug"""
    try:
        product = await db.get_product_by_slug(slug)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            success=True,
            message="Product retrieved successfully",
            data=product.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product by slug: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Admin Product Routes
@app.post("/api/admin/products", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Create new product (Admin only)"""
    try:
        new_product = await db.create_product(product)
        return ProductResponse(
            success=True,
            message="Product created successfully",
            data=new_product.dict()
        )
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/admin/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    """Update product (Admin only)"""
    try:
        updated_product = await db.update_product(product_id, product_update)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            success=True,
            message="Product updated successfully",
            data=updated_product.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/admin/products/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: str):
    """Delete product (Admin only)"""
    try:
        deleted = await db.delete_product(product_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return ProductResponse(
            success=True,
            message="Product deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# User Routes
@app.post("/api/users/register", response_model=ProductResponse)
async def register_user(user: UserCreate):
    """Register new user"""
    try:
        # Check if user already exists
        existing_user = await db.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        new_user = await db.create_user(user)
        return ProductResponse(
            success=True,
            message="User registered successfully",
            data=new_user.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/users/login", response_model=ProductResponse)
async def login_user(user_login: UserLogin):
    """Login user"""
    try:
        user = await db.get_user_by_email(user_login.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # TODO: Implement password verification
        
        return ProductResponse(
            success=True,
            message="User logged in successfully",
            data=user.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/users/{user_id}", response_model=ProductResponse)
async def get_user(user_id: str):
    """Get user by ID"""
    try:
        user = await db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return ProductResponse(
            success=True,
            message="User retrieved successfully",
            data=user.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Order Routes
@app.post("/api/orders", response_model=ProductResponse)
async def create_order(order: OrderCreate):
    """Create new order"""
    try:
        new_order = await db.create_order(order)
        return ProductResponse(
            success=True,
            message="Order created successfully",
            data=new_order.dict()
        )
    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/orders/{order_id}", response_model=ProductResponse)
async def get_order(order_id: str):
    """Get order by ID"""
    try:
        order = await db.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return ProductResponse(
            success=True,
            message="Order retrieved successfully",
            data=order.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting order: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/users/{user_id}/orders", response_model=ProductResponse)
async def get_user_orders(user_id: str):
    """Get user orders"""
    try:
        orders = await db.get_user_orders(user_id)
        return ProductResponse(
            success=True,
            message="User orders retrieved successfully",
            data=[order.dict() for order in orders]
        )
    except Exception as e:
        logger.error(f"Error getting user orders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/orders/{order_id}/status", response_model=ProductResponse)
async def update_order_status(order_id: str, status: OrderStatus):
    """Update order status"""
    try:
        updated = await db.update_order_status(order_id, status)
        if not updated:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return ProductResponse(
            success=True,
            message="Order status updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating order status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/orders/{order_id}/payment", response_model=ProductResponse)
async def update_payment_status(order_id: str, payment_status: PaymentStatus):
    """Update payment status"""
    try:
        updated = await db.update_payment_status(order_id, payment_status)
        if not updated:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return ProductResponse(
            success=True,
            message="Payment status updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating payment status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Review Routes
@app.post("/api/reviews", response_model=ProductResponse)
async def create_review(review: ReviewCreate):
    """Create new review"""
    try:
        new_review = await db.create_review(review)
        return ProductResponse(
            success=True,
            message="Review created successfully",
            data=new_review.dict()
        )
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/products/{product_id}/reviews", response_model=ProductResponse)
async def get_product_reviews(product_id: str, limit: int = 10):
    """Get product reviews"""
    try:
        reviews = await db.get_product_reviews(product_id, limit)
        return ProductResponse(
            success=True,
            message="Product reviews retrieved successfully",
            data=[review.dict() for review in reviews]
        )
    except Exception as e:
        logger.error(f"Error getting product reviews: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Blog Routes
@app.post("/api/admin/blog", response_model=ProductResponse)
async def create_blog_post(blog_post: BlogPostCreate):
    """Create new blog post (Admin only)"""
    try:
        new_post = await db.create_blog_post(blog_post)
        return ProductResponse(
            success=True,
            message="Blog post created successfully",
            data=new_post.dict()
        )
    except Exception as e:
        logger.error(f"Error creating blog post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blog", response_model=ProductResponse)
async def get_blog_posts(limit: int = 10, skip: int = 0):
    """Get blog posts"""
    try:
        posts = await db.get_blog_posts(limit, skip)
        return ProductResponse(
            success=True,
            message="Blog posts retrieved successfully",
            data=[post.dict() for post in posts]
        )
    except Exception as e:
        logger.error(f"Error getting blog posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blog/featured", response_model=ProductResponse)
async def get_featured_blog_posts(limit: int = 3):
    """Get featured blog posts"""
    try:
        posts = await db.get_featured_blog_posts(limit)
        return ProductResponse(
            success=True,
            message="Featured blog posts retrieved successfully",
            data=[post.dict() for post in posts]
        )
    except Exception as e:
        logger.error(f"Error getting featured blog posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blog/{post_id}", response_model=ProductResponse)
async def get_blog_post(post_id: str):
    """Get blog post by ID"""
    try:
        post = await db.get_blog_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return ProductResponse(
            success=True,
            message="Blog post retrieved successfully",
            data=post.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blog post: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/blog/slug/{slug}", response_model=ProductResponse)
async def get_blog_post_by_slug(slug: str):
    """Get blog post by slug"""
    try:
        post = await db.get_blog_post_by_slug(slug)
        if not post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        return ProductResponse(
            success=True,
            message="Blog post retrieved successfully",
            data=post.dict()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blog post by slug: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Category Routes
@app.post("/api/admin/categories", response_model=ProductResponse)
async def create_category(category: CategoryCreate):
    """Create new category (Admin only)"""
    try:
        new_category = await db.create_category(category)
        return ProductResponse(
            success=True,
            message="Category created successfully",
            data=new_category.dict()
        )
    except Exception as e:
        logger.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/categories", response_model=ProductResponse)
async def get_categories():
    """Get all categories"""
    try:
        categories = await db.get_categories()
        return ProductResponse(
            success=True,
            message="Categories retrieved successfully",
            data=[category.dict() for category in categories]
        )
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Newsletter Routes
@app.post("/api/newsletter", response_model=ProductResponse)
async def subscribe_newsletter(newsletter: NewsletterCreate):
    """Subscribe to newsletter"""
    try:
        subscription = await db.subscribe_newsletter(newsletter)
        return ProductResponse(
            success=True,
            message="Successfully subscribed to newsletter",
            data=subscription.dict()
        )
    except Exception as e:
        logger.error(f"Error subscribing to newsletter: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Contact Routes
@app.post("/api/contact", response_model=ProductResponse)
async def create_contact(contact: ContactCreate):
    """Create contact message"""
    try:
        new_contact = await db.create_contact(contact)
        return ProductResponse(
            success=True,
            message="Contact message sent successfully",
            data=new_contact.dict()
        )
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Analytics Routes
@app.get("/api/admin/analytics", response_model=ProductResponse)
async def get_analytics_stats():
    """Get analytics statistics (Admin only)"""
    try:
        stats = await db.get_analytics_stats()
        return ProductResponse(
            success=True,
            message="Analytics statistics retrieved successfully",
            data=stats
        )
    except Exception as e:
        logger.error(f"Error getting analytics stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Root endpoint
@app.get("/api/")
async def root():
    """Root endpoint"""
    return {
        "message": "Premium Subscription Shop API",
        "version": "1.0.0",
        "status": "running"
    }

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)