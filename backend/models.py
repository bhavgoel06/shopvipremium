from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

class CategoryType(str, Enum):
    OTT = "ott"
    SOFTWARE = "software"
    VPN = "vpn"
    GAMING = "gaming"
    PROFESSIONAL = "professional"
    SOCIAL_MEDIA = "social_media"
    ADULT = "adult"
    EDUCATION = "education"

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

# Product Models
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    description: str
    short_description: str
    category: CategoryType
    subcategory: Optional[str] = None
    original_price: float
    discounted_price: float
    discount_percentage: int
    duration_options: List[str]  # ["1 month", "3 months", "6 months", "1 year"]
    features: List[str]
    image_url: str
    gallery_images: List[str] = []
    is_featured: bool = False
    is_bestseller: bool = False
    stock_quantity: int = 0
    status: ProductStatus = ProductStatus.ACTIVE
    seo_title: str
    seo_description: str
    seo_keywords: List[str] = []
    rating: float = 0.0
    total_reviews: int = 0
    total_sales: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    description: str
    short_description: str
    category: CategoryType
    subcategory: Optional[str] = None
    original_price: float
    discounted_price: float
    duration_options: List[str]
    features: List[str]
    image_url: str
    gallery_images: List[str] = []
    is_featured: bool = False
    is_bestseller: bool = False
    stock_quantity: int = 0
    seo_title: str
    seo_description: str
    seo_keywords: List[str] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    category: Optional[CategoryType] = None
    subcategory: Optional[str] = None
    original_price: Optional[float] = None
    discounted_price: Optional[float] = None
    duration_options: Optional[List[str]] = None
    features: Optional[List[str]] = None
    image_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None
    is_featured: Optional[bool] = None
    is_bestseller: Optional[bool] = None
    stock_quantity: Optional[int] = None
    status: Optional[ProductStatus] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    seo_keywords: Optional[List[str]] = None

# User Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime

class AuthData(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class AuthResponse(BaseModel):
    success: bool
    message: str
    data: AuthData

# Order Models
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    duration: str
    quantity: int
    unit_price: float
    total_price: float

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_email: str
    user_name: str
    user_phone: Optional[str] = None
    items: List[OrderItem]
    total_amount: float
    discount_amount: float = 0.0
    final_amount: float
    status: OrderStatus = OrderStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_method: str
    delivery_details: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    user_id: str
    user_email: str
    user_name: str
    user_phone: Optional[str] = None
    items: List[OrderItem]
    total_amount: float
    discount_amount: float = 0.0
    payment_method: str
    notes: Optional[str] = None

# Review Models
class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_id: str
    user_id: str
    user_name: str
    rating: int = Field(ge=1, le=5)
    title: str
    content: str
    is_verified: bool = False
    is_approved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewCreate(BaseModel):
    product_id: str
    user_id: str
    user_name: str
    rating: int = Field(ge=1, le=5)
    title: str
    content: str

# Blog Models
class BlogPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    content: str
    excerpt: str
    author: str
    featured_image: str
    category: str
    tags: List[str] = []
    is_published: bool = False
    is_featured: bool = False
    seo_title: str
    seo_description: str
    seo_keywords: List[str] = []
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BlogPostCreate(BaseModel):
    title: str
    content: str
    excerpt: str
    author: str
    featured_image: str
    category: str
    tags: List[str] = []
    is_published: bool = False
    is_featured: bool = False
    seo_title: str
    seo_description: str
    seo_keywords: List[str] = []

# Category Models
class Category(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    description: str
    icon: str
    image_url: str
    parent_id: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0
    seo_title: str
    seo_description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CategoryCreate(BaseModel):
    name: str
    description: str
    icon: str
    image_url: str
    parent_id: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0
    seo_title: str
    seo_description: str

# Newsletter Models
class Newsletter(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    is_active: bool = True
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)

class NewsletterCreate(BaseModel):
    email: EmailStr

# Contact Models
class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str
    is_replied: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

# Analytics Models
class Analytics(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    page_path: str
    user_id: Optional[str] = None
    ip_address: str
    user_agent: str
    referrer: Optional[str] = None
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AnalyticsCreate(BaseModel):
    page_path: str
    user_id: Optional[str] = None
    ip_address: str
    user_agent: str
    referrer: Optional[str] = None
    session_id: str

# Response Models
class ProductResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: List[Any]
    total: int
    page: int
    per_page: int
    total_pages: int

class SearchFilters(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rating: Optional[int] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: int = 1
    per_page: int = 12