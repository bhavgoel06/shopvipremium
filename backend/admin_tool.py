#!/usr/bin/env python3
"""
ADMIN MANAGEMENT TOOL
Easy-to-use command-line tool for managing your e-commerce site
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import *

class AdminManager:
    def __init__(self):
        self.db = db
    
    async def add_product(self, product_data):
        """Add a new product to the database"""
        try:
            product = ProductCreate(**product_data)
            new_product = await self.db.create_product(product)
            print(f"✅ Product '{new_product.name}' added successfully!")
            print(f"   ID: {new_product.id}")
            print(f"   Price: ₹{new_product.discounted_price}")
            print(f"   Category: {new_product.category}")
            return new_product
        except Exception as e:
            print(f"❌ Error adding product: {e}")
            return None
    
    async def update_product_price(self, product_id, new_price):
        """Update product price"""
        try:
            update_data = ProductUpdate(discounted_price=new_price)
            updated_product = await self.db.update_product(product_id, update_data)
            if updated_product:
                print(f"✅ Product price updated to ₹{new_price}")
                return updated_product
            else:
                print("❌ Product not found")
                return None
        except Exception as e:
            print(f"❌ Error updating price: {e}")
            return None
    
    async def list_products(self, category=None):
        """List all products or products in a specific category"""
        try:
            filters = SearchFilters(category=category, per_page=100)
            products = await self.db.get_products(filters)
            
            print(f"\n📦 PRODUCTS LIST ({len(products)} products)")
            print("=" * 70)
            
            for product in products:
                print(f"ID: {product.id[:8]}... | {product.name}")
                print(f"   Price: ₹{product.discounted_price} | Category: {product.category}")
                print(f"   Stock: {product.stock_quantity} | Status: {product.status}")
                print("-" * 70)
            
            return products
        except Exception as e:
            print(f"❌ Error listing products: {e}")
            return []
    
    async def delete_product(self, product_id):
        """Delete a product"""
        try:
            deleted = await self.db.delete_product(product_id)
            if deleted:
                print(f"✅ Product deleted successfully!")
                return True
            else:
                print("❌ Product not found")
                return False
        except Exception as e:
            print(f"❌ Error deleting product: {e}")
            return False
    
    async def get_stats(self):
        """Get website statistics"""
        try:
            stats = await self.db.get_analytics_stats()
            
            print("\n📊 WEBSITE STATISTICS")
            print("=" * 40)
            print(f"Total Products: {stats['total_products']}")
            print(f"Total Orders: {stats['total_orders']}")
            print(f"Total Users: {stats['total_users']}")
            print(f"Today's Visitors: {stats['today_visitors']}")
            print("=" * 40)
            
            return stats
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None
    
    async def add_blog_post(self, blog_data):
        """Add a new blog post"""
        try:
            blog_post = BlogPostCreate(**blog_data)
            new_post = await self.db.create_blog_post(blog_post)
            print(f"✅ Blog post '{new_post.title}' added successfully!")
            print(f"   ID: {new_post.id}")
            print(f"   Slug: {new_post.slug}")
            return new_post
        except Exception as e:
            print(f"❌ Error adding blog post: {e}")
            return None

# Command line interface
async def main():
    admin = AdminManager()
    
    if len(sys.argv) < 2:
        print("""
🛠️  ADMIN MANAGEMENT TOOL
========================

Usage: python admin_tool.py <command> [options]

Available commands:
  stats           - Show website statistics
  list            - List all products
  list <category> - List products in specific category
  add-product     - Add a new product (interactive)
  update-price    - Update product price (interactive)
  delete          - Delete a product (interactive)
  add-blog        - Add a new blog post (interactive)

Examples:
  python admin_tool.py stats
  python admin_tool.py list ott
  python admin_tool.py add-product
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "stats":
        await admin.get_stats()
    
    elif command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        await admin.list_products(category)
    
    elif command == "add-product":
        print("\n➕ ADD NEW PRODUCT")
        print("=" * 30)
        
        # Interactive product creation
        product_data = {
            "name": input("Product name: "),
            "description": input("Product description: "),
            "short_description": input("Short description: "),
            "category": input("Category (ott/software/vpn/professional/gaming): "),
            "original_price": float(input("Original price: ")),
            "discounted_price": float(input("Discounted price: ")),
            "duration_options": input("Duration options (comma-separated): ").split(","),
            "features": input("Features (comma-separated): ").split(","),
            "image_url": input("Image URL: "),
            "stock_quantity": int(input("Stock quantity: ")),
            "seo_title": input("SEO title: "),
            "seo_description": input("SEO description: "),
            "seo_keywords": input("SEO keywords (comma-separated): ").split(",")
        }
        
        await admin.add_product(product_data)
    
    elif command == "update-price":
        print("\n💰 UPDATE PRODUCT PRICE")
        print("=" * 30)
        
        product_id = input("Product ID: ")
        new_price = float(input("New price: "))
        
        await admin.update_product_price(product_id, new_price)
    
    elif command == "delete":
        print("\n🗑️  DELETE PRODUCT")
        print("=" * 30)
        
        product_id = input("Product ID: ")
        confirm = input("Are you sure? (yes/no): ")
        
        if confirm.lower() == "yes":
            await admin.delete_product(product_id)
        else:
            print("❌ Operation cancelled")
    
    elif command == "add-blog":
        print("\n📝 ADD NEW BLOG POST")
        print("=" * 30)
        
        blog_data = {
            "title": input("Blog title: "),
            "content": input("Blog content: "),
            "excerpt": input("Excerpt: "),
            "author": input("Author name: "),
            "featured_image": input("Featured image URL: "),
            "category": input("Category: "),
            "tags": input("Tags (comma-separated): ").split(","),
            "is_published": input("Publish now? (yes/no): ").lower() == "yes",
            "seo_title": input("SEO title: "),
            "seo_description": input("SEO description: "),
            "seo_keywords": input("SEO keywords (comma-separated): ").split(",")
        }
        
        await admin.add_blog_post(blog_data)
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    asyncio.run(main())