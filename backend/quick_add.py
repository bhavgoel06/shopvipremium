#!/usr/bin/env python3
"""
QUICK PRODUCT ADDER
Easy script to add products quickly
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import *

# Pre-defined product templates for quick adding
PRODUCT_TEMPLATES = {
    "netflix": {
        "name": "Netflix Premium 4K",
        "description": "Enjoy unlimited streaming of movies, TV shows, and documentaries in stunning 4K quality. Share with up to 4 family members. Watch on any device - Smart TV, laptop, phone, or tablet. Access to exclusive Netflix Originals and latest releases.",
        "short_description": "Premium Netflix subscription with 4K streaming and 4 screens",
        "category": "ott",
        "original_price": 649.0,
        "discounted_price": 199.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "4K Ultra HD streaming",
            "4 simultaneous screens",
            "Unlimited downloads",
            "No ads",
            "Access to Netflix Originals"
        ],
        "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
        "stock_quantity": 100,
        "seo_title": "Netflix Premium 4K Subscription - 70% Off",
        "seo_description": "Get Netflix Premium 4K subscription at 70% off. Unlimited streaming, 4 screens, no ads.",
        "seo_keywords": ["netflix premium", "netflix 4k", "netflix subscription"]
    },
    "adobe": {
        "name": "Adobe Creative Cloud All Apps",
        "description": "Complete creative suite with Photoshop, Illustrator, Premiere Pro, After Effects, and 20+ creative apps. Perfect for designers, photographers, and video editors.",
        "short_description": "Complete Adobe Creative Cloud suite with all applications",
        "category": "software",
        "original_price": 4999.0,
        "discounted_price": 1299.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "20+ Creative Apps",
            "Photoshop, Illustrator, Premiere Pro",
            "100GB cloud storage",
            "Premium fonts"
        ],
        "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=500&h=300&fit=crop",
        "stock_quantity": 50,
        "seo_title": "Adobe Creative Cloud All Apps - 74% Off",
        "seo_description": "Adobe Creative Cloud complete suite at 74% discount. Photoshop, Illustrator, Premiere Pro.",
        "seo_keywords": ["adobe creative cloud", "photoshop", "illustrator"]
    }
}

async def quick_add_product(template_name, custom_name=None, custom_price=None):
    """Quickly add a product using a template"""
    
    if template_name not in PRODUCT_TEMPLATES:
        print(f"❌ Template '{template_name}' not found")
        print(f"Available templates: {list(PRODUCT_TEMPLATES.keys())}")
        return None
    
    # Get template data
    product_data = PRODUCT_TEMPLATES[template_name].copy()
    
    # Apply customizations
    if custom_name:
        product_data["name"] = custom_name
    if custom_price:
        product_data["discounted_price"] = custom_price
    
    try:
        product = ProductCreate(**product_data)
        new_product = await db.create_product(product)
        print(f"✅ Product '{new_product.name}' added successfully!")
        print(f"   ID: {new_product.id}")
        print(f"   Price: ₹{new_product.discounted_price}")
        return new_product
    except Exception as e:
        print(f"❌ Error adding product: {e}")
        return None

async def main():
    if len(sys.argv) < 2:
        print("""
🚀 QUICK PRODUCT ADDER
=====================

Usage: python quick_add.py <template> [custom_name] [custom_price]

Available templates:
  netflix - Netflix Premium 4K
  adobe   - Adobe Creative Cloud All Apps

Examples:
  python quick_add.py netflix
  python quick_add.py netflix "Netflix Premium Custom" 299
  python quick_add.py adobe "Adobe Suite Pro" 999
        """)
        return
    
    template_name = sys.argv[1].lower()
    custom_name = sys.argv[2] if len(sys.argv) > 2 else None
    custom_price = float(sys.argv[3]) if len(sys.argv) > 3 else None
    
    await quick_add_product(template_name, custom_name, custom_price)

if __name__ == "__main__":
    asyncio.run(main())