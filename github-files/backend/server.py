from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import uuid
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="ShopVIPremium API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
client = None
db = None

async def get_db():
    global client, db
    if client is None:
        client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
        db = client[os.getenv("DB_NAME")]
    return db

# Sample products - 81 products
PRODUCTS = []

def generate_products():
    categories = ["ott", "software", "vpn", "education", "social_media", "gaming", "membership"]
    names = ["Netflix Premium", "Spotify Premium", "ChatGPT Plus", "Adobe Creative", "Microsoft Office", "VPN Premium", "Gaming Plus"]
    
    for i in range(1, 82):
        category = categories[i % len(categories)]
        name = f"{names[i % len(names)]} {i}"
        
        product = {
            "id": str(uuid.uuid4()),
            "name": name,
            "slug": name.lower().replace(" ", "-").replace("+", "-plus"),
            "description": f"{name} - Premium digital access with instant delivery and 24/7 support.",
            "short_description": f"{name} - Premium access",
            "category": category,
            "original_price": float(999 + (i * 100)),
            "discounted_price": float(499 + (i * 50)),
            "discount_percentage": int(50 + (i % 30)),
            "image_url": f"https://via.placeholder.com/300x200?text={name.replace(' ', '+')}",
            "is_featured": i <= 8,
            "is_bestseller": i <= 12 and i > 4,
            "stock_quantity": 100,
            "status": "active",
            "rating": 4.0 + (i % 10) / 10,
            "total_reviews": i * 10,
            "created_at": datetime.now().isoformat()
        }
        PRODUCTS.append(product)

generate_products()

@app.on_event("startup")
async def startup():
    db = await get_db()
    # Seed products if database is empty
    count = await db.products.count_documents({})
    if count == 0:
        await db.products.insert_many(PRODUCTS)

@app.get("/api/health")
async def health():
    return {"status": "healthy", "products": len(PRODUCTS)}

@app.get("/api/products")
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    category: Optional[str] = None,
    search: Optional[str] = None
):
    db = await get_db()
    
    # Build filter
    filter_dict = {"status": "active"}
    if category:
        filter_dict["category"] = category
    if search:
        filter_dict["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get products from database
    skip = (page - 1) * per_page
    cursor = db.products.find(filter_dict).skip(skip).limit(per_page)
    products = await cursor.to_list(length=per_page)
    
    total = await db.products.count_documents(filter_dict)
    
    return {
        "success": True,
        "data": products,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

@app.get("/api/products/featured")
async def get_featured():
    db = await get_db()
    cursor = db.products.find({"is_featured": True, "status": "active"}).limit(8)
    products = await cursor.to_list(length=8)
    return {"success": True, "data": products}

@app.get("/api/products/bestsellers") 
async def get_bestsellers():
    db = await get_db()
    cursor = db.products.find({"is_bestseller": True, "status": "active"}).limit(8)
    products = await cursor.to_list(length=8)
    return {"success": True, "data": products}

@app.get("/api/products/search")
async def search_products(q: str = Query(...)):
    db = await get_db()
    filter_dict = {
        "status": "active",
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"category": {"$regex": q, "$options": "i"}}
        ]
    }
    cursor = db.products.find(filter_dict).limit(20)
    products = await cursor.to_list(length=20)
    return {"success": True, "data": products}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)