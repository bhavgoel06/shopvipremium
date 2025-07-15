#!/usr/bin/env python3
"""
BUSINESS DASHBOARD
Simple dashboard to monitor your e-commerce business
"""

import asyncio
import sys
import os
import json
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import *

class BusinessDashboard:
    def __init__(self):
        self.db = db
    
    async def daily_report(self):
        """Generate daily business report"""
        print("\n📈 DAILY BUSINESS REPORT")
        print("=" * 50)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Get basic stats
        stats = await self.db.get_analytics_stats()
        
        print(f"📦 Total Products: {stats['total_products']}")
        print(f"👥 Total Customers: {stats['total_users']}")
        print(f"🛒 Total Orders: {stats['total_orders']}")
        print(f"👀 Today's Visitors: {stats['today_visitors']}")
        
        # Get top products
        filters = SearchFilters(sort_by="total_sales", sort_order="desc", per_page=5)
        top_products = await self.db.get_products(filters)
        
        print(f"\n🏆 TOP SELLING PRODUCTS:")
        for i, product in enumerate(top_products, 1):
            print(f"{i}. {product.name}")
            print(f"   Price: ₹{product.discounted_price} | Sales: {product.total_sales}")
        
        # Category breakdown
        categories = ["ott", "software", "vpn", "professional", "gaming"]
        print(f"\n📊 PRODUCTS BY CATEGORY:")
        for category in categories:
            cat_filters = SearchFilters(category=category, per_page=100)
            cat_products = await self.db.get_products(cat_filters)
            print(f"   {category.upper()}: {len(cat_products)} products")
        
        print("\n" + "=" * 50)
        print("💡 RECOMMENDATIONS:")
        
        if stats['total_products'] < 20:
            print("• Add more products to increase selection")
        if stats['total_orders'] < 10:
            print("• Focus on marketing to increase orders")
        if stats['today_visitors'] < 100:
            print("• Improve SEO to get more visitors")
        
        print("=" * 50)
    
    async def weekly_summary(self):
        """Generate weekly business summary"""
        print("\n📊 WEEKLY BUSINESS SUMMARY")
        print("=" * 50)
        
        # This is a simplified version - in production, you'd track actual weekly data
        stats = await self.db.get_analytics_stats()
        
        print(f"Week ending: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"📈 Estimated weekly revenue: ₹{stats['total_orders'] * 500}")
        print(f"🎯 Products added this week: {stats['total_products']}")
        print(f"👥 New customers: {stats['total_users']}")
        
        print(f"\n🚀 GROWTH OPPORTUNITIES:")
        print("• Add blog posts for SEO")
        print("• Partner with influencers")
        print("• Launch email marketing")
        print("• Optimize popular products")
    
    async def product_performance(self):
        """Show product performance metrics"""
        print("\n📊 PRODUCT PERFORMANCE")
        print("=" * 50)
        
        # Top performers
        filters = SearchFilters(sort_by="total_sales", sort_order="desc", per_page=10)
        products = await self.db.get_products(filters)
        
        print("🏆 TOP PERFORMERS:")
        for i, product in enumerate(products[:5], 1):
            profit_margin = ((product.original_price - product.discounted_price) / product.original_price) * 100
            print(f"{i}. {product.name[:30]}...")
            print(f"   Sales: {product.total_sales} | Rating: {product.rating}/5")
            print(f"   Profit Margin: {profit_margin:.1f}%")
            print()
        
        # Low stock alerts
        low_stock = [p for p in products if p.stock_quantity < 10]
        if low_stock:
            print("⚠️ LOW STOCK ALERTS:")
            for product in low_stock:
                print(f"• {product.name}: {product.stock_quantity} remaining")
        
        print("=" * 50)

async def main():
    dashboard = BusinessDashboard()
    
    if len(sys.argv) < 2:
        print("""
📊 BUSINESS DASHBOARD
====================

Usage: python dashboard.py <command>

Commands:
  daily      - Daily business report
  weekly     - Weekly business summary  
  products   - Product performance analysis
  
Examples:
  python dashboard.py daily
  python dashboard.py weekly
  python dashboard.py products
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "daily":
        await dashboard.daily_report()
    elif command == "weekly":
        await dashboard.weekly_summary()
    elif command == "products":
        await dashboard.product_performance()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    asyncio.run(main())