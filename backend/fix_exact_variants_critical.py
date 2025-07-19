#!/usr/bin/env python3
"""
CRITICAL FIX: Update ALL products with EXACT variants and descriptions from shopallpremium.com
This fixes the wrong generic variants I mistakenly added
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

# Database connection
client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'premium_shop')]

# EXACT PRODUCT DATA FROM SHOPALLPREMIUM.COM
EXACT_PRODUCT_DATA = {
    "YouTube Premium (WorldWide)": {
        "description": """YouTube Premium (WorldWide)

Works Worldwide.

This Youtube Premium will work in Every Country.

We will send you login credentials in your email.

With YouTube Premium, you can watch millions of videos without interruptions by ads before and during a video, including video overlay ads. You will also not see third-party banner ads and search ads.

Features
• YouTube Premium
• Watch videos without ads
• Download videos to watch offline
• Personal Account
• Background play and Picture-in-picture
• Access to YouTube Music Premium
• YouTube Originals
• All Device Supported [Smart Phone, Tablet iOS, Mac, Windows, TV, PlayStation, FireStick, etc.]

Usage
Just log in and use the YouTube & YouTube Music App.

Indian Users
Go to this link for purchase: Click Here

International User (Outside India)
Just Login the credentials in the Youtube App / Website.

Please change the password and add a recovery email in Google Account Settings.

FAQ (Frequently Asked Queries)

Q. How many devices can I use for this YouTube Premium?
I would say unlimited. I mean as much as you can log in to your Gmail account on multiple devices like PC, SmartPhone, TV, iOs, etc.

Q. Can I get this Subscription in my existing account (Gmail)?
Yes, you can activate these 6 Months and 1 Year to your existing account. First, contact our WhatsApp Support Team.

Our WhatsApp Team will guide you for activation.

Q. Can I renew my 6 Months and 1 Year after expiry?
Yes, of course, we can renew your plan after your plan expiry. Just place an order and contact our WhatsApp Team.

Q. Can I change my password and email?
If we are providing you with Gmail Credentials, you can change your password. Also, we recommend you change the password only.

Replacement & Warranty
You can claim your warranty if your account is not working within the warranty period.

Contact WhatsApp Team to claim your replacement warranty

Please Read the Above Details Before Purchasing.

TYPE: Our Email Password
VALIDITY: 1 Year | 6 Months""",
        "short_description": "YouTube Premium (WorldWide) - Works Worldwide. Ad-free videos, downloads, background play, YouTube Music Premium included.",
        "features": [
            "YouTube Premium",
            "Watch videos without ads",
            "Download videos to watch offline", 
            "Personal Account",
            "Background play and Picture-in-picture",
            "Access to YouTube Music Premium",
            "YouTube Originals",
            "All Device Supported"
        ],
        "duration_options": ["Comes with 12 Month Plan (Private)", "6 Months Plan"],
        "category": "ott"
    },
    
    "HMA VPN": {
        "description": """HMA VPN

Works in (Android / Windows)

HMA VPN (HideMyAss VPN) is a popular virtual private network service that offers secure and private internet access by masking your IP address and encrypting your data. It provides a user-friendly interface, servers in numerous countries, and supports multiple devices for enhanced online privacy and bypassing geo-restrictions.

*Important Terms*
• Do Not try to change the E-Mail

TYPE: License Key – 1 Year
VALIDITY: 1 Year
Warranty: 10 Months
Personal Account

Please Read the Above Details Before Purchase.

HMA VPN Features:
• 20 Gbps server speeds
• 90+ countries
• Browse the web from a different region
• Stay safe on Wi-Fi
• Protect and secure your information when connected to public Wi-Fi
• Hide your IP address to enjoy anonymous browsing
• Stop hackers from stealing your identity and data snoopers
• Works on all of your devices including Android TV or game console
• Connect up to 5 devices at the same time
• Round-the-clock customer support via email and live chat
• Encrypt your connection when using unsecured public Wi-Fi hotspots""",
        "short_description": "HMA VPN - Secure VPN service with servers in 90+ countries. License Key for 1 Year.",
        "features": [
            "20 Gbps server speeds",
            "90+ countries",
            "Works on Android / Windows",
            "License Key – 1 Year",
            "10 Months Warranty",
            "Personal Account",
            "Connect up to 5 devices",
            "24/7 customer support"
        ],
        "duration_options": ["License Key - 1 Year"],
        "category": "vpn"
    },
    
    "Coursera Plus": {
        "description": """Coursera Plus gives you unlimited access to thousands of courses from top universities and companies.

Features:
• Unlimited access to thousands of courses
• Certificates from top universities
• Hands-on projects and assignments
• Mobile and desktop access
• Download courses for offline learning
• No ads interruptions
• Access to specializations and professional certificates

*Important Terms*
• TYPE: Account (Email & Password)
• VALIDITY: As per selected plan
• Personal use only

Please Read the Above Details Before Purchasing.""",
        "short_description": "Coursera Plus - Unlimited access to thousands of courses from top universities",
        "features": [
            "Unlimited access to thousands of courses",
            "Certificates from top universities", 
            "Hands-on projects and assignments",
            "Mobile and desktop access",
            "Download courses for offline learning",
            "No ads interruptions",
            "Access to specializations",
            "Professional certificates"
        ],
        "duration_options": ["Individual Plan", "Plus Plan", "Team Plan"],
        "category": "education"
    },
    
    "Spotify Premium – Individual": {
        "description": """Spotify Premium is a digital music, podcast, and video service that gives you access to millions of songs and other content from creators all over the world

• Password Changeable
• Personal Account

Key Features
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
        "short_description": "Spotify Premium Individual - Ad-free music streaming with offline playback",
        "features": [
            "Ad-free music listening",
            "Works in all countries",
            "Enjoy uninterrupted music",
            "Offline playback", 
            "Save your data by listening offline",
            "Play everywhere",
            "Password Changeable",
            "Personal Account",
            "All Device Supported",
            "High-quality streaming at 320 Kbps"
        ],
        "duration_options": ["1 Month Plan", "3 Months Plan", "6 Months Plan", "1 Year Plan"],
        "category": "membership"
    },
    
    "Netflix Premium 4K UHD": {
        "description": """Netflix is one of the world's leading entertainment services with 221 million paid memberships in over 190 countries enjoying TV series, documentaries and feature films across a wide variety of genres and languages.

Features
• 4 SCREEN
• ULTRA HD PLAN  
• Personal Account
• Password Changeable
• All Device Supported
  [Smart Phone, Tablet iOS, Mac, Windows, TV, PlayStation, FireStick, etc.]

★ VPN = Not Required

FAQ (FREQUENTLY ASKED QUERIES)

Q. What does 4 Screen mean and 4K UHD mean?
Four people can simultaneously log in to one single account and watch anything they want. UHD means Ultra HD Quality of video streaming which is used mostly in TVs.

Q. Can I change my password and email?
Also, we recommend you change the password only. Email change is not allowed; otherwise, the warranty will be void.

*Important Terms*
TYPE: Account (Email & Password)
VALIDITY: 28 Days

Please Read the Above Details Before Purchase.""",
        "short_description": "Netflix Premium 4K UHD - 4 Screen Ultra HD Plan with 28 Days validity",
        "features": [
            "4 SCREEN",
            "ULTRA HD PLAN",
            "Personal Account",
            "Password Changeable", 
            "All Device Supported",
            "VPN Not Required",
            "28 Days Validity",
            "Account (Email & Password)"
        ],
        "duration_options": ["4 Screens Ultra HD - 28 Days"],
        "category": "ott"
    },
    
    "LeetCode Premium": {
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
        "short_description": "LeetCode Premium - Coding practice and interview preparation platform",
        "features": [
            "Access to Premium Content",
            "Video Solutions",
            "Interview Preparation Tools",
            "Insights and Analytics",
            "Enhanced Contest Features", 
            "Priority Support",
            "Learning and Practice Resources",
            "Works on every platform",
            "Activated on Your Email"
        ],
        "duration_options": ["Premium Plan - 1 Month", "Premium Plan - 1 Year"],
        "category": "education"
    }
}

# For other products, remove generic variants and set proper ones based on category
CATEGORY_SPECIFIC_VARIANTS = {
    "software": ["License Key", "Product Key", "Activation Key", "Full Version"],
    "vpn": ["License Key - 1 Year", "License Key - 6 Months", "Personal License"],
    "ott": ["Personal Account", "Family Account", "Premium Plan"],
    "education": ["Individual Plan", "Student Plan", "Premium Access"],
    "membership": ["Individual Plan", "Premium Plan", "Plus Plan"],
    "professional": ["Business License", "Professional Plan", "Enterprise Access"],
    "gaming": ["Game License", "DLC Access", "Season Pass", "Premium Edition"],
    "health": ["Personal Plan", "Premium Features", "Pro Access"],
    "financial": ["Basic Plan", "Premium Features", "Professional Tools"],
    "social_media": ["Premium Features", "Pro Account", "Business Plan"],
    "adult": ["Premium Access", "VIP Account", "Exclusive Content"]
}

async def fix_exact_products():
    """Fix specific products with exact data from shopallpremium.com"""
    
    print("🔧 FIXING EXACT PRODUCTS WITH SHOPALLPREMIUM.COM DATA...")
    
    fixed_count = 0
    
    for product_name, exact_data in EXACT_PRODUCT_DATA.items():
        try:
            # Find product by name (flexible matching)
            product = await db.products.find_one({
                "name": {"$regex": product_name.replace("(", "\\(").replace(")", "\\)"), "$options": "i"}
            })
            
            if not product:
                # Try partial matching
                name_parts = product_name.split()
                for part in name_parts[:2]:  # Try first 2 words
                    if len(part) > 3:
                        product = await db.products.find_one({
                            "name": {"$regex": part, "$options": "i"}
                        })
                        if product:
                            break
            
            if product:
                # Remove MongoDB _id
                product.pop('_id', None)
                
                # Update with exact data
                update_data = {
                    "description": exact_data["description"],
                    "short_description": exact_data["short_description"], 
                    "features": exact_data["features"],
                    "duration_options": exact_data["duration_options"],
                    "category": exact_data["category"],
                    "updated_at": datetime.utcnow(),
                    "data_source": "shopallpremium.com_exact"
                }
                
                result = await db.products.update_one(
                    {"id": product["id"]},
                    {"$set": update_data}
                )
                
                if result.modified_count > 0:
                    fixed_count += 1
                    print(f"✅ FIXED: {product_name}")
                    print(f"   Variants: {exact_data['duration_options']}")
                    print("---")
                else:
                    print(f"⚠️  No changes: {product_name}")
            else:
                print(f"❌ Not found: {product_name}")
                
        except Exception as e:
            print(f"❌ Error fixing {product_name}: {e}")
    
    print(f"\n📊 Fixed {fixed_count}/{len(EXACT_PRODUCT_DATA)} exact products")
    return fixed_count

async def fix_remaining_generic_variants():
    """Fix remaining products that have generic variants"""
    
    print("\n🔧 FIXING REMAINING PRODUCTS WITH GENERIC VARIANTS...")
    
    # Find products with generic time-based variants
    generic_patterns = ["1 month", "3 months", "6 months", "1 year", "2 years"]
    
    cursor = db.products.find({
        "duration_options": {"$in": generic_patterns},
        "data_source": {"$ne": "shopallpremium.com_exact"}  # Skip already fixed products
    })
    
    fixed_count = 0
    
    async for product in cursor:
        try:
            product.pop('_id', None)
            
            category = product.get("category", "ott")
            product_name = product.get("name", "")
            
            # Get appropriate variants for this category
            new_variants = CATEGORY_SPECIFIC_VARIANTS.get(category, ["Personal Plan", "Premium Access"])
            
            # Special handling for specific product types
            if "key" in product_name.lower() or "license" in product_name.lower():
                new_variants = ["License Key", "Product Key"]
            elif "vpn" in product_name.lower():
                new_variants = ["License Key - 1 Year"]
            elif "premium" in product_name.lower() and category == "ott":
                new_variants = ["Premium Account"]
            
            # Update the product
            result = await db.products.update_one(
                {"id": product["id"]},
                {"$set": {
                    "duration_options": new_variants,
                    "updated_at": datetime.utcnow(),
                    "data_source": "category_appropriate"
                }}
            )
            
            if result.modified_count > 0:
                fixed_count += 1
                print(f"✅ Fixed generic variants: {product_name}")
                print(f"   Category: {category}")
                print(f"   New variants: {new_variants}")
                print("---")
                
        except Exception as e:
            print(f"❌ Error fixing generic variants for {product.get('name', 'Unknown')}: {e}")
    
    print(f"\n📊 Fixed generic variants for {fixed_count} products")
    return fixed_count

async def verify_fixes():
    """Verify that fixes were applied correctly"""
    
    print("\n🔍 VERIFYING FIXES...")
    
    # Check for remaining generic variants
    generic_patterns = ["1 month", "3 months", "6 months", "1 year", "2 years"]
    generic_count = await db.products.count_documents({
        "duration_options": {"$in": generic_patterns}
    })
    
    print(f"📊 Verification Results:")
    print(f"   - Products with generic variants remaining: {generic_count}")
    
    # Show sample of fixed products
    fixed_products = await db.products.find({
        "data_source": "shopallpremium.com_exact"
    }).limit(3).to_list(length=3)
    
    print(f"   - Sample of exact fixes:")
    for product in fixed_products:
        print(f"     • {product['name']}: {product['duration_options']}")
    
    if generic_count == 0:
        print("🎉 SUCCESS: No generic variants remaining!")
    else:
        print(f"⚠️  {generic_count} products still have generic variants")

async def main():
    """Main function to run all fixes"""
    
    print("🚨 CRITICAL FIX: REMOVING WRONG GENERIC VARIANTS")
    print("=" * 80)
    print("Fixing products with EXACT variants from shopallpremium.com")
    print("Removing generic '1 month, 6 months, 1 year' variants I mistakenly added")
    print("=" * 80)
    
    try:
        # Step 1: Fix specific products with exact data
        exact_count = await fix_exact_products()
        
        # Step 2: Fix remaining generic variants
        generic_count = await fix_remaining_generic_variants()
        
        # Step 3: Verify fixes
        await verify_fixes()
        
        print("\n" + "=" * 80)
        print("✅ CRITICAL FIXES COMPLETED!")
        print(f"📊 Total fixes: {exact_count + generic_count}")
        print("🎯 Products now have correct variants from shopallpremium.com")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())