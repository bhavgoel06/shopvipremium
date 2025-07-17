#!/usr/bin/env python3
"""
Script to fix product variants and descriptions to match shopallpremium.com exactly
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import json
from datetime import datetime

# Database connection
client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'premium_shop')]

# Product variants and descriptions matching shopallpremium.com
PRODUCT_UPDATES = {
    "OnlyFans Accounts": {
        "duration_options": ["$100 Balance", "$200 Balance"],
        "description": """Get Onlyfans Accounts with Loaded Balance

Use your Balance –
• Subscribe to models and see full Videos
• Unlock chats and Video calls with them
• Tip models for Exclusive content for you
• Transfer Funds for Personalized Requests

*Important Terms*
• Warranty: 6 - 8 hours Only
• All Device Supported

TYPE: Account ( Email & Password)

Please Read the Above Details Before purchasing.""",
        "short_description": "Get Onlyfans Accounts with Loaded Balance",
        "features": [
            "Subscribe to models and see full Videos",
            "Unlock chats and Video calls with them",
            "Tip models for Exclusive content for you",
            "Transfer Funds for Personalized Requests",
            "Warranty: 6 - 8 hours Only",
            "All Device Supported",
            "Account (Email & Password)"
        ]
    },
    
    "Netflix 1 Screen": {
        "duration_options": ["28 Days"],
        "description": """Netflix is one of the world's leading entertainment services, with 221 million paid memberships in over 190 countries, enjoying TV series, documentaries, feature films, and mobile games across various genres and languages.

VPN : Not Required

Comes with 28 Days Subscription UHD Plan

★ 1 SCREEN ONLY
★ UHD PLAN (799₹)

*Important Terms*
• Do Not try to change the Email
• CLEAR DATA OF NETFLIX APP BEFORE LOGIN

TYPE: Account (Email & Password)
VALIDITY: 28 Days""",
        "short_description": "Netflix 1 Screen UHD Plan - 28 Days Subscription",
        "features": [
            "1 Screen Only",
            "UHD Plan (799₹)",
            "28 Days Subscription",
            "VPN Not Required",
            "Account (Email & Password)",
            "Do Not change Email"
        ]
    },

    "Netflix Premium 4K UHD": {
        "duration_options": ["1 Screen", "2 Screens", "4 Screens (4K)", "Mobile Only"],
        "description": """Netflix is one of the world's leading entertainment services with 221 million paid memberships in over 190 countries enjoying TV series, documentaries and feature films across a wide variety of genres and languages.

Premium 4K UHD plan allows streaming on up to 4 screens simultaneously in Ultra High Definition quality.

*Important Terms*
• Do Not try to change the E-Mail or Password
• TYPE: Account (EMAIL & Password)
• VALIDITY: 1 Month
• Cracked Account""",
        "short_description": "Netflix Premium 4K UHD with multiple screen options",
        "features": [
            "Ultra HD (4K) streaming quality",
            "Stream on up to 4 screens simultaneously",
            "Download content for offline viewing",
            "No ads interruptions",
            "Access to Netflix Originals",
            "Compatible with all devices",
            "1 month validity",
            "Instant delivery"
        ]
    },

    "Spotify Premium – Individual": {
        "duration_options": ["1 Month", "3 Months", "6 Months", "1 Year"],
        "description": """Spotify Premium is a digital music, podcast, and video service that gives you access to millions of songs and other content from creators all over the world

• Password Changeable
• Personal Account

Key Features:
• Ad-free music listening
• Works in all countries
• Enjoy uninterrupted music
• Offline playback
• Save your data by listening offline
• Play everywhere
• Listen to your speakers, TV, and other favorite devices
• Password Changeable
• Personal Account
• All Device Supported [Smart Phone, Tablet iOS, Mac, Windows, TV, PlayStation, FireStick, etc.]

VALIDITY: 1 Month | 3 Months | 4 Months | 6 Months | 1 Year
Personal Account

Please Read the Above Details Before Purchasing.""",
        "short_description": "Spotify Premium Individual - Ad-free music streaming",
        "features": [
            "Ad-free music listening",
            "Works in all countries",
            "Offline playback",
            "Password Changeable",
            "Personal Account",
            "All Device Supported",
            "High-quality streaming at 320 Kbps",
            "Unlimited skips"
        ]
    },

    "LeetCode Premium": {
        "duration_options": ["1 Month", "1 Year"],
        "description": """LeetCode is a popular online platform for coding practice, technical interview preparation, and skill development for software developers. It provides a wide range of coding problems and tools to help users enhance their programming and problem-solving skills.

Plan: Premium

Benefits:
• Access to Premium Content
• Video Solutions
• Interview Preparation Tools
• Insights and Analytics
• Enhanced Contest Features
• Priority Support
• Learning and Practice Resources
• Works on every platform [Smart Phone, Tablet iOS, Mac, Windows, TV, etc.]

*Important Terms*
• It will be Activated on Your Email

TYPE: Account (Email & Password)
VALIDITY: 1 Month | 1 Year
Personal Account

Please Read the Above Details Before Purchase.""",
        "short_description": "LeetCode Premium - Coding practice and interview preparation",
        "features": [
            "Access to Premium Content",
            "Video Solutions",
            "Interview Preparation Tools",
            "Insights and Analytics",
            "Enhanced Contest Features",
            "Priority Support",
            "Learning and Practice Resources",
            "Works on every platform"
        ]
    },

    "YouTube Premium (WorldWide)": {
        "duration_options": ["1 Month", "3 Months", "6 Months", "1 Year"],
        "description": """YouTube Premium (WorldWide) gives you access to ad-free videos, background play, offline downloads, and YouTube Music Premium.

Features:
• Ad-free videos across YouTube
• Background play (keep videos playing when you switch apps)
• Offline downloads for mobile
• YouTube Music Premium included
• Works worldwide
• All devices supported

*Important Terms*
• TYPE: Account (Email & Password)
• VALIDITY: As per selected plan
• Works worldwide

Please Read the Above Details Before Purchasing.""",
        "short_description": "YouTube Premium WorldWide - Ad-free videos and music",
        "features": [
            "Ad-free videos",
            "Background play",
            "Offline downloads",
            "YouTube Music Premium",
            "Works worldwide",
            "All devices supported",
            "No interruptions",
            "High-quality streaming"
        ]
    },

    "Amazon Prime Video": {
        "duration_options": ["1 Month", "3 Months", "6 Months", "1 Year"],
        "description": """Amazon Prime Video offers unlimited streaming of movies and TV episodes for Amazon Prime members.

Features:
• Unlimited streaming of movies and TV shows
• Amazon Prime Originals
• Download content for offline viewing
• Multiple device streaming
• High-quality video playback
• Family-friendly content controls

*Important Terms*
• TYPE: Account (Email & Password)
• VALIDITY: As per selected plan
• Works internationally

Please Read the Above Details Before Purchasing.""",
        "short_description": "Amazon Prime Video - Unlimited streaming of movies and TV shows",
        "features": [
            "Unlimited streaming",
            "Amazon Prime Originals",
            "Offline downloads",
            "Multiple devices",
            "High-quality video",
            "Family controls",
            "International access",
            "Instant delivery"
        ]
    }
}

async def update_product_variants_and_descriptions():
    """Update products with correct variants and descriptions"""
    
    print("🔄 Starting product variants and descriptions update...")
    
    updated_count = 0
    total_products = len(PRODUCT_UPDATES)
    
    for product_name, updates in PRODUCT_UPDATES.items():
        try:
            # Find product by name (case-insensitive)
            product = await db.products.find_one({
                "name": {"$regex": f"^{product_name}$", "$options": "i"}
            })
            
            if not product:
                print(f"⚠️  Product not found: {product_name}")
                continue
            
            # Prepare update data
            update_data = {
                "duration_options": updates["duration_options"],
                "description": updates["description"],
                "short_description": updates["short_description"],
                "features": updates["features"],
                "updated_at": datetime.utcnow()
            }
            
            # Update the product
            result = await db.products.update_one(
                {"id": product["id"]},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ Updated: {product_name}")
                print(f"   - Duration options: {updates['duration_options']}")
                print(f"   - Features: {len(updates['features'])} features")
            else:
                print(f"⚠️  No changes needed for: {product_name}")
                
        except Exception as e:
            print(f"❌ Error updating {product_name}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   - Products to update: {total_products}")
    print(f"   - Successfully updated: {updated_count}")
    print(f"   - Update completion: {(updated_count/total_products)*100:.1f}%")
    
    return updated_count

async def fix_generic_variants():
    """Fix products that still have generic time-based variants"""
    
    print("\n🔄 Fixing generic time-based variants...")
    
    # Find products with generic variants
    generic_variants = ["1 month", "3 months", "6 months", "1 year"]
    
    cursor = db.products.find({
        "duration_options": {"$in": generic_variants},
        "category": {"$ne": "adult"}  # Skip adult products
    })
    
    fixed_count = 0
    
    async for product in cursor:
        try:
            product_name = product["name"]
            category = product["category"]
            
            # Define category-specific variants
            if category == "software":
                new_variants = ["Basic Plan", "Pro Plan", "Enterprise Plan", "Lifetime"]
            elif category == "education":
                new_variants = ["Personal Plan", "Plus Plan", "Pro Plan", "Team Plan"]
            elif category == "vpn":
                new_variants = ["1 Month", "6 Months", "1 Year", "2 Years"]
            elif category == "ott":
                new_variants = ["Basic Plan", "Standard Plan", "Premium Plan", "Family Plan"]
            elif category == "membership":
                new_variants = ["Monthly", "Quarterly", "Half-yearly", "Yearly"]
            elif category == "social_media":
                new_variants = ["Basic", "Premium", "Plus", "Gold"]
            elif category == "gaming":
                new_variants = ["Standard", "Deluxe", "Ultimate", "Season Pass"]
            elif category == "health":
                new_variants = ["Basic", "Premium", "Pro", "Family"]
            elif category == "professional":
                new_variants = ["Individual", "Business", "Enterprise", "Team"]
            elif category == "financial":
                new_variants = ["Basic", "Premium", "Pro", "Enterprise"]
            else:
                new_variants = ["Basic", "Standard", "Premium", "Pro"]
            
            # Update the product
            result = await db.products.update_one(
                {"id": product["id"]},
                {"$set": {
                    "duration_options": new_variants,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            if result.modified_count > 0:
                fixed_count += 1
                print(f"✅ Fixed generic variants for: {product_name}")
                print(f"   - Category: {category}")
                print(f"   - New variants: {new_variants}")
                
        except Exception as e:
            print(f"❌ Error fixing variants for {product['name']}: {e}")
    
    print(f"\n📊 Generic variants fix summary:")
    print(f"   - Products fixed: {fixed_count}")
    
    return fixed_count

async def main():
    """Main function to run all updates"""
    
    print("🚀 Starting comprehensive product updates...")
    print("="*60)
    
    # Update specific products with shopallpremium.com data
    updated_count = await update_product_variants_and_descriptions()
    
    # Fix remaining generic variants
    fixed_count = await fix_generic_variants()
    
    print("\n" + "="*60)
    print("✅ ALL UPDATES COMPLETED!")
    print(f"📊 Total products updated: {updated_count + fixed_count}")
    print("="*60)
    
    # Close database connection
    client.close()

if __name__ == "__main__":
    asyncio.run(main())