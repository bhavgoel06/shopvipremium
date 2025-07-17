import asyncio
import requests
from bs4 import BeautifulSoup
from database import db
from models import SearchFilters
import time
import re

# Manual mapping of correct descriptions and features from shopallpremium.com
CORRECT_PRODUCT_DATA = {
    "Codecademy PRO": {
        "description": """Codecademy PRO helps you review and practice what you learn on the web, anywhere, anytime. Learn to code the easy way.

"Taking a few minutes a day to reinforce the underlying concepts has been an easy way to remember them, even on days when I'm not coding." — Chance N., Codecademy Go Learner

"Comparing it to all of the other coding apps I have tried this one is best at bringing together learning, practicing, and practicality via articles into one place." — Sean M., Codecademy Go Learner

Comes with 6 Months | 1 Year Subscription Plan. Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 6 Months | 1 Year. Cracked Account.""",
        "features": [
            "Discover a new way to practice coding syntax",
            "Remember more with daily flashcards that you can quickly skim",
            "Review whenever, wherever. Leave the desktop",
            "Learn how to apply your skills in your day-to-day with advice from industry leaders",
            "Maintain streaks and track your progress",
            "Learn Web Development, Data Science, Computer Science",
            "HTML & CSS, Python, JavaScript, SQL support",
            "6 Months | 1 Year subscription options"
        ]
    },
    "OnlyFans Accounts": {
        "description": """Get Onlyfans Accounts with Loaded Balance

Use your Balance →Subscribe to models and see full Videos, Send Messages, and much more.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 12 Months. Cracked Account.""",
        "features": [
            "Premium account with loaded balance",
            "Subscribe to exclusive content from creators",
            "Send direct messages to models",
            "Access high-quality photos and videos",
            "12 months validity",
            "Instant delivery within 24 hours",
            "Compatible with all devices",
            "24/7 customer support"
        ]
    },
    "Netflix Premium 4K UHD": {
        "description": """Netflix is one of the world's leading entertainment services with 221 million paid memberships in over 190 countries enjoying TV series, documentaries and feature films across a wide variety of genres and languages.

Premium 4K UHD plan allows streaming on up to 4 screens simultaneously in Ultra High Definition quality.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Month. Cracked Account.""",
        "features": [
            "Ultra HD (4K) streaming quality",
            "Stream on up to 4 screens simultaneously",
            "Download content for offline viewing",
            "No ads interruptions",
            "Access to Netflix Originals",
            "Compatible with all devices",
            "1 month validity",
            "Instant delivery within 24 hours"
        ]
    },
    "Spotify Premium – Individual": {
        "description": """Spotify Premium gives you ad-free music streaming with unlimited skips and the ability to download music for offline listening.

Individual plan is perfect for one person with all premium features included.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Month. Cracked Account.""",
        "features": [
            "Ad-free music streaming",
            "Unlimited skips",
            "Download up to 10,000 songs for offline listening",
            "High-quality audio streaming",
            "Access to millions of songs and podcasts",
            "Individual plan for one user",
            "1 month validity",
            "Instant delivery within 24 hours"
        ]
    },
    "ChatGPT Plus": {
        "description": """ChatGPT Plus gives you faster response speeds, priority access during peak times, and access to GPT-4 and other advanced features.

Perfect for users who need reliable access to ChatGPT's most advanced capabilities.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Month. Cracked Account.""",
        "features": [
            "Access to GPT-4 model",
            "Faster response times",
            "Priority access during peak hours",
            "Advanced conversation capabilities",
            "Plugin support and integrations",
            "1 month validity",
            "Instant delivery within 24 hours",
            "24/7 customer support"
        ]
    },
    "Coursera Plus": {
        "description": """Coursera Plus is a subscription plan that gives you unlimited access to over 90% of the learning programs on Coursera, including courses, Specializations, and Professional Certificates.

Perfect for learners who want to explore multiple subjects and advance their skills.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Year. Cracked Account.""",
        "features": [
            "Unlimited access to 90% of Coursera content",
            "Courses from top universities and companies",
            "Professional Certificates included",
            "Specializations and guided projects",
            "Mobile app access for learning on-the-go",
            "1 year validity",
            "Instant delivery within 24 hours",
            "24/7 customer support"
        ]
    },
    "Canva PRO": {
        "description": """Canva Pro gives you access to premium templates, stock photos, and advanced design tools to create professional-quality graphics.

Perfect for designers, marketers, and content creators who need advanced features.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Year. Cracked Account.""",
        "features": [
            "Access to premium templates and designs",
            "100GB cloud storage",
            "Background remover tool",
            "Magic resize for different platforms",
            "Brand kit and team collaboration",
            "Premium stock photos and videos",
            "1 year validity",
            "Instant delivery within 24 hours"
        ]
    },
    "Amazon Prime Video": {
        "description": """Amazon Prime Video offers unlimited streaming of movies, TV shows, and Amazon Original content.

Includes access to a vast library of entertainment content with high-quality streaming.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 1 Month. Cracked Account.""",
        "features": [
            "Unlimited streaming of movies and TV shows",
            "Access to Amazon Original content",
            "Download content for offline viewing",
            "Multiple device support",
            "HD streaming quality",
            "1 month validity",
            "Instant delivery within 24 hours",
            "24/7 customer support"
        ]
    }
}

async def update_all_products_with_correct_data():
    """Update all products with correct descriptions and features"""
    
    # Get all products
    products = await db.get_products(SearchFilters(page=1, per_page=200))
    print(f"Updating {len(products)} products with correct data...")
    
    updated_count = 0
    
    for product in products:
        try:
            # Check if we have manual data for this product
            correct_data = None
            
            # Direct match
            if product.name in CORRECT_PRODUCT_DATA:
                correct_data = CORRECT_PRODUCT_DATA[product.name]
            else:
                # Partial match
                for key, data in CORRECT_PRODUCT_DATA.items():
                    if key.lower() in product.name.lower() or product.name.lower() in key.lower():
                        correct_data = data
                        break
            
            if correct_data:
                # Update with correct data
                await db.db.products.update_one(
                    {'id': product.id},
                    {'$set': {
                        'description': correct_data['description'],
                        'features': correct_data['features'],
                        'short_description': correct_data['description'][:200] + "..."
                    }}
                )
                updated_count += 1
                print(f"✓ Updated {updated_count}: {product.name}")
            else:
                # Set generic but proper description
                generic_description = f"""Get premium access to {product.name} with full features and instant delivery.

This premium subscription includes all advanced features and benefits at a discounted price.

Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: As per selected plan. Cracked Account."""
                
                generic_features = [
                    "Premium account with full access",
                    "All advanced features included",
                    "Instant delivery within 24 hours",
                    "30-day warranty included",
                    "24/7 customer support",
                    "Compatible with all devices",
                    "Multiple duration options",
                    "100% genuine accounts"
                ]
                
                await db.db.products.update_one(
                    {'id': product.id},
                    {'$set': {
                        'description': generic_description,
                        'features': generic_features,
                        'short_description': f"Get premium access to {product.name} with full features and instant delivery."
                    }}
                )
                updated_count += 1
                print(f"✓ Updated {updated_count}: {product.name} (generic)")
                
        except Exception as e:
            print(f"✗ Error updating {product.name}: {e}")
            continue
    
    print(f"\n🎉 Successfully updated {updated_count} products!")
    
    # Show samples
    print("\n📝 Sample updated products:")
    for product_name in ["Codecademy PRO", "OnlyFans Accounts", "Netflix Premium 4K UHD"]:
        products = await db.get_products(SearchFilters(search=product_name.split()[0].lower(), limit=1))
        if products:
            product = products[0]
            print(f"\n- {product.name}")
            print(f"  Description: {product.description[:100]}...")
            print(f"  Features: {len(product.features)} features")

if __name__ == "__main__":
    asyncio.run(update_all_products_with_correct_data())