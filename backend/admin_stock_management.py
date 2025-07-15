#!/usr/bin/env python3
"""
Admin Stock Management System
Provides one-click stock management for all products
"""

import asyncio
import sys
from datetime import datetime
from typing import Optional, List
from models import Product, ProductStatus
from database import db

class StockManager:
    def __init__(self):
        self.db = db
    
    async def set_all_out_of_stock(self):
        """Set all products to out of stock"""
        try:
            result = await self.db.db.products.update_many(
                {},
                {
                    "$set": {
                        "stock_quantity": 0,
                        "status": ProductStatus.OUT_OF_STOCK.value,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count
        except Exception as e:
            print(f"Error setting all products out of stock: {e}")
            return 0
    
    async def set_all_in_stock(self, default_stock: int = 100):
        """Set all products to in stock with default quantity"""
        try:
            result = await self.db.db.products.update_many(
                {},
                {
                    "$set": {
                        "stock_quantity": default_stock,
                        "status": ProductStatus.ACTIVE.value,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count
        except Exception as e:
            print(f"Error setting all products in stock: {e}")
            return 0
    
    async def set_product_stock(self, product_id: str, stock_quantity: int):
        """Set stock for a specific product"""
        try:
            status = ProductStatus.ACTIVE if stock_quantity > 0 else ProductStatus.OUT_OF_STOCK
            result = await self.db.db.products.update_one(
                {"id": product_id},
                {
                    "$set": {
                        "stock_quantity": stock_quantity,
                        "status": status.value,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error setting product stock: {e}")
            return False
    
    async def get_stock_overview(self):
        """Get stock overview for all products"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": None,
                        "total_products": {"$sum": 1},
                        "in_stock": {
                            "$sum": {
                                "$cond": [{"$gt": ["$stock_quantity", 0]}, 1, 0]
                            }
                        },
                        "out_of_stock": {
                            "$sum": {
                                "$cond": [{"$eq": ["$stock_quantity", 0]}, 1, 0]
                            }
                        },
                        "total_stock_units": {"$sum": "$stock_quantity"}
                    }
                }
            ]
            
            result = await self.db.db.products.aggregate(pipeline).to_list(length=1)
            if result:
                return result[0]
            return {
                "total_products": 0,
                "in_stock": 0,
                "out_of_stock": 0,
                "total_stock_units": 0
            }
        except Exception as e:
            print(f"Error getting stock overview: {e}")
            return None
    
    async def get_low_stock_products(self, threshold: int = 10):
        """Get products with low stock"""
        try:
            cursor = self.db.db.products.find(
                {"stock_quantity": {"$lte": threshold, "$gt": 0}},
                {"id": 1, "name": 1, "stock_quantity": 1, "category": 1}
            )
            products = await cursor.to_list(length=100)
            return products
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    async def get_all_products_stock(self):
        """Get all products with their stock information"""
        try:
            cursor = self.db.db.products.find(
                {},
                {
                    "id": 1,
                    "name": 1,
                    "category": 1,
                    "stock_quantity": 1,
                    "status": 1,
                    "discounted_price": 1,
                    "is_featured": 1,
                    "is_bestseller": 1
                }
            )
            products = await cursor.to_list(length=1000)
            return products
        except Exception as e:
            print(f"Error getting all products stock: {e}")
            return []

async def main():
    """Main function for command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python admin_stock_management.py <command> [options]")
        print("Commands:")
        print("  overview              - Show stock overview")
        print("  set-all-out-of-stock  - Set all products to out of stock")
        print("  set-all-in-stock      - Set all products to in stock")
        print("  low-stock             - Show products with low stock")
        print("  list-all              - List all products with stock info")
        print("  set-stock <product_id> <quantity> - Set stock for specific product")
        return
    
    stock_manager = StockManager()
    command = sys.argv[1]
    
    if command == "overview":
        overview = await stock_manager.get_stock_overview()
        if overview:
            print("📊 STOCK OVERVIEW")
            print("=" * 50)
            print(f"Total Products: {overview['total_products']}")
            print(f"In Stock: {overview['in_stock']}")
            print(f"Out of Stock: {overview['out_of_stock']}")
            print(f"Total Stock Units: {overview['total_stock_units']}")
            print()
            
            # Show percentage
            if overview['total_products'] > 0:
                in_stock_pct = (overview['in_stock'] / overview['total_products']) * 100
                print(f"Stock Availability: {in_stock_pct:.1f}%")
    
    elif command == "set-all-out-of-stock":
        print("⚠️  Setting all products to OUT OF STOCK...")
        count = await stock_manager.set_all_out_of_stock()
        print(f"✅ Successfully updated {count} products to out of stock")
    
    elif command == "set-all-in-stock":
        default_stock = 100
        if len(sys.argv) > 2:
            default_stock = int(sys.argv[2])
        
        print(f"📦 Setting all products to IN STOCK with {default_stock} units...")
        count = await stock_manager.set_all_in_stock(default_stock)
        print(f"✅ Successfully updated {count} products to in stock")
    
    elif command == "low-stock":
        threshold = 10
        if len(sys.argv) > 2:
            threshold = int(sys.argv[2])
        
        print(f"⚠️  LOW STOCK PRODUCTS (≤ {threshold} units)")
        print("=" * 50)
        products = await stock_manager.get_low_stock_products(threshold)
        
        if products:
            for product in products:
                print(f"📦 {product['name']}")
                print(f"   Stock: {product['stock_quantity']} units")
                print(f"   Category: {product['category']}")
                print(f"   ID: {product['id']}")
                print()
        else:
            print("✅ No products with low stock found")
    
    elif command == "list-all":
        print("📋 ALL PRODUCTS STOCK STATUS")
        print("=" * 80)
        products = await stock_manager.get_all_products_stock()
        
        for product in products:
            status_emoji = "✅" if product['stock_quantity'] > 0 else "❌"
            featured_emoji = "⭐" if product.get('is_featured', False) else ""
            bestseller_emoji = "🔥" if product.get('is_bestseller', False) else ""
            
            print(f"{status_emoji} {product['name']} {featured_emoji} {bestseller_emoji}")
            print(f"   Stock: {product['stock_quantity']} units")
            print(f"   Category: {product['category']}")
            print(f"   Price: ₹{product['discounted_price']}")
            print(f"   Status: {product['status']}")
            print()
    
    elif command == "set-stock":
        if len(sys.argv) < 4:
            print("Usage: python admin_stock_management.py set-stock <product_id> <quantity>")
            return
        
        product_id = sys.argv[2]
        quantity = int(sys.argv[3])
        
        success = await stock_manager.set_product_stock(product_id, quantity)
        if success:
            print(f"✅ Successfully set stock for product {product_id} to {quantity} units")
        else:
            print(f"❌ Failed to set stock for product {product_id}")
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python admin_stock_management.py' without arguments to see available commands")

if __name__ == "__main__":
    asyncio.run(main())