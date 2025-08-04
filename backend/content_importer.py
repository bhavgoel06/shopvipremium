#!/usr/bin/env python3
"""
Content importer and admin content management system
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add the backend directory to Python path
sys.path.append('/app/backend')

from database import db
from models import Product

async def import_scraped_products():
    """Import scraped/sample products into database"""
    print("Starting product import...")
    
    # Sample products based on shopallpremium.com structure
    sample_products = [
        {
            "id": "netflix-premium-4k-1month",
            "name": "Netflix Premium 4K UHD (1 Month)",
            "short_description": "Netflix Premium with 4K streaming and multiple screens",
            "description": "Get Netflix Premium subscription with stunning 4K Ultra HD quality, watch on up to 4 screens simultaneously, download content for offline viewing, and enjoy completely ad-free experience. Perfect for families and movie enthusiasts who want the ultimate Netflix experience.",
            "category": "ott",
            "original_price": 649,
            "discounted_price": 199,
            "currency": "INR",
            "duration_options": ["1 month", "3 months", "6 months", "1 year"],
            "features": [
                "4K Ultra HD streaming quality",
                "Watch on 4 screens at the same time", 
                "Download & watch offline on mobile",
                "No advertisements",
                "Premium Netflix Originals",
                "Instant account delivery",
                "24/7 customer support"
            ],
            "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 100,
            "is_featured": True,
            "is_bestseller": True,
            "average_rating": 4.8,
            "review_count": 1250,
            "seo_title": "Netflix Premium 4K UHD Subscription - 1 Month at ₹199",
            "seo_description": "Get Netflix Premium 4K subscription for just ₹199/month. Watch on 4 screens, offline downloads, no ads. Instant delivery with 24/7 support.",
            "seo_keywords": ["netflix premium", "4k subscription", "netflix 4 screens", "netflix premium india"]
        },
        {
            "id": "spotify-premium-3months",
            "name": "Spotify Premium Individual (3 Months)",
            "short_description": "Ad-free music streaming with offline downloads",
            "description": "Enjoy unlimited music streaming without any advertisements. Download your favorite songs and playlists for offline listening, get unlimited skips, and experience high-quality audio streaming. Perfect for music lovers who want uninterrupted listening experience.",
            "category": "music",
            "original_price": 399,
            "discounted_price": 299,
            "currency": "INR", 
            "duration_options": ["1 month", "3 months", "6 months", "1 year"],
            "features": [
                "Ad-free music streaming",
                "Download music for offline listening",
                "Unlimited song skips",
                "High-quality audio (320kbps)",
                "Access to podcasts",
                "Play any song, anytime",
                "Cross-device listening"
            ],
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 100,
            "is_featured": True,
            "is_bestseller": True,
            "average_rating": 4.7,
            "review_count": 980,
            "seo_title": "Spotify Premium 3 Months Subscription - Music Without Ads",
            "seo_description": "Get Spotify Premium for 3 months at discounted price. No ads, offline downloads, unlimited skips. Premium music streaming experience.",
            "seo_keywords": ["spotify premium", "music streaming", "offline music", "spotify india"]
        },
        {
            "id": "disney-hotstar-super-1year",
            "name": "Disney+ Hotstar Super (1 Year)",
            "short_description": "Complete entertainment with Disney+ and live sports",
            "description": "Access the complete Disney+ Hotstar Super experience with premium Disney content, Marvel movies, live sports including IPL and cricket, latest Bollywood and Hollywood movies, and exclusive Indian shows. Stream on multiple devices with full HD quality.",
            "category": "ott",
            "original_price": 1499,
            "discounted_price": 799,
            "currency": "INR",
            "duration_options": ["3 months", "6 months", "1 year"],
            "features": [
                "Disney+ Premium Originals",
                "Live Sports (IPL, Cricket, Football)",
                "Latest movies in HD",
                "Indian premium content",
                "Marvel & Star Wars content", 
                "Watch on 2 devices simultaneously",
                "Ad-free Disney+ content"
            ],
            "image_url": "https://images.unsplash.com/photo-1489599314773-1b98e69cced3?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 100,
            "is_featured": True,
            "is_bestseller": True,
            "average_rating": 4.6,
            "review_count": 750,
            "seo_title": "Disney+ Hotstar Super 1 Year Subscription - Premium Entertainment",
            "seo_description": "Disney+ Hotstar Super yearly plan with live sports, Disney+ content, movies. Watch IPL, Marvel, Bollywood at discounted price.",
            "seo_keywords": ["disney hotstar", "hotstar premium", "ipl streaming", "disney plus india"]
        },
        {
            "id": "amazon-prime-video-1year",
            "name": "Amazon Prime Video (1 Year)",
            "short_description": "Prime Video with exclusive shows and faster delivery",
            "description": "Get Amazon Prime membership with access to Prime Video's exclusive shows and movies, faster delivery on Amazon orders, Prime Music access, and exclusive deals during sales. Complete entertainment and shopping benefits in one subscription.",
            "category": "ott",
            "original_price": 1499,
            "discounted_price": 899,
            "currency": "INR",
            "duration_options": ["3 months", "6 months", "1 year"],
            "features": [
                "Prime Video Originals & Movies",
                "Free & faster delivery on Amazon",
                "Prime Music access",
                "Early access to deals & sales",
                "Prime Reading books",
                "Ad-free streaming",
                "Download for offline viewing"
            ],
            "image_url": "https://images.unsplash.com/photo-1560472355-536de3962603?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 100,
            "is_featured": True,
            "is_bestseller": False,
            "average_rating": 4.5,
            "review_count": 920,
            "seo_title": "Amazon Prime Video 1 Year Subscription - Streaming + Shopping Benefits",
            "seo_description": "Get Amazon Prime for full year with Prime Video, free delivery, exclusive deals. Complete entertainment and shopping package.",
            "seo_keywords": ["amazon prime", "prime video", "prime membership", "amazon prime india"]
        },
        {
            "id": "nordvpn-2year-plan",
            "name": "NordVPN 2-Year Plan",
            "short_description": "Secure VPN with 5400+ servers worldwide",
            "description": "Protect your online privacy with NordVPN's premium 2-year plan. Get access to 5400+ servers in 60+ countries, military-grade encryption, no-logs policy, kill switch protection, and secure up to 6 devices simultaneously. Perfect for privacy-conscious users.",
            "category": "vpn",
            "original_price": 11600,
            "discounted_price": 6999,
            "currency": "INR",
            "duration_options": ["6 months", "1 year", "2 years", "3 years"],
            "features": [
                "5400+ servers in 60+ countries",
                "Military-grade encryption",
                "Strict no-logs policy",
                "Kill switch protection",
                "Secure up to 6 devices",
                "24/7 customer support",
                "30-day money-back guarantee"
            ],
            "image_url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 100,
            "is_featured": True,
            "is_bestseller": False,
            "average_rating": 4.4,
            "review_count": 650,
            "seo_title": "NordVPN 2-Year Plan - Premium VPN Security at Discounted Price",
            "seo_description": "Get NordVPN 2-year subscription with 40% discount. 5400+ servers, no-logs policy, 6 devices. Secure your online privacy now.",
            "seo_keywords": ["nordvpn", "vpn service", "online privacy", "secure vpn india"]
        },
        {
            "id": "adobe-creative-cloud-1year",
            "name": "Adobe Creative Cloud All Apps (1 Year)",
            "short_description": "Complete Adobe Creative Suite for professionals",
            "description": "Get the complete Adobe Creative Cloud suite including Photoshop, Illustrator, Premiere Pro, After Effects, InDesign, and 15+ more professional apps. Includes 100GB cloud storage, premium fonts, and regular updates. Perfect for designers, photographers, and content creators.",
            "category": "software",
            "original_price": 52999,
            "discounted_price": 24999,
            "currency": "INR",
            "duration_options": ["6 months", "1 year", "2 years"],
            "features": [
                "20+ premium Adobe apps",
                "100GB cloud storage",
                "Adobe Fonts premium library",
                "Regular app updates",
                "Mobile apps included",
                "Advanced collaboration tools",
                "Premium tutorials & resources"
            ],
            "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 50,
            "is_featured": True,
            "is_bestseller": False,
            "average_rating": 4.9,
            "review_count": 420,
            "seo_title": "Adobe Creative Cloud All Apps 1 Year - Professional Design Suite",
            "seo_description": "Adobe Creative Cloud yearly subscription at 53% discount. Photoshop, Illustrator, Premiere Pro + 17 more apps. For professionals.",
            "seo_keywords": ["adobe creative cloud", "photoshop subscription", "adobe illustrator", "creative suite india"]
        },
        {
            "id": "chatgpt-plus-1month",
            "name": "ChatGPT Plus (1 Month)",
            "short_description": "Advanced AI assistant with GPT-4 access",
            "description": "Unlock the full potential of ChatGPT with Plus subscription. Get priority access to GPT-4, faster response times, plugin access, and advanced AI capabilities. Perfect for professionals, students, and anyone who wants the best AI assistance available.",
            "category": "software",
            "original_price": 2000,
            "discounted_price": 589,
            "currency": "INR",
            "duration_options": ["1 month", "3 months", "6 months"],
            "features": [
                "Access to GPT-4 model",
                "Priority access during high traffic",
                "Faster response times",
                "Plugin access (when available)",
                "Advanced reasoning capabilities",
                "Image analysis with GPT-4V",
                "Priority customer support"
            ],
            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 200,
            "is_featured": True,
            "is_bestseller": True,
            "average_rating": 4.8,
            "review_count": 1100,
            "seo_title": "ChatGPT Plus 1 Month - Advanced AI Assistant with GPT-4",
            "seo_description": "ChatGPT Plus subscription with GPT-4 access for just ₹589. Priority access, faster responses, advanced AI features.",
            "seo_keywords": ["chatgpt plus", "gpt-4 access", "ai assistant", "chatgpt subscription"]
        },
        {
            "id": "youtube-premium-6months",
            "name": "YouTube Premium (6 Months)",
            "short_description": "Ad-free YouTube with background play and downloads",
            "description": "Enjoy YouTube without interruptions with YouTube Premium. Watch ad-free videos, play videos in background, download for offline viewing, and get access to YouTube Music Premium. Perfect for heavy YouTube users and music lovers.",
            "category": "ott",
            "original_price": 779,
            "discounted_price": 499,
            "currency": "INR",
            "duration_options": ["1 month", "3 months", "6 months", "1 year"],
            "features": [
                "Ad-free YouTube videos",
                "Background play on mobile",
                "Download videos for offline",
                "YouTube Music Premium included",
                "YouTube Originals access",
                "Play with screen locked",
                "No interruptions while watching"
            ],
            "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=500&h=300&fit=crop&auto=format&q=80",
            "stock_quantity": 150,
            "is_featured": False,
            "is_bestseller": True,
            "average_rating": 4.6,
            "review_count": 890,
            "seo_title": "YouTube Premium 6 Months - Ad-Free YouTube Experience",
            "seo_description": "YouTube Premium 6-month subscription at discounted price. No ads, background play, offline downloads, YouTube Music included.",
            "seo_keywords": ["youtube premium", "ad-free youtube", "youtube music", "youtube subscription"]
        }
    ]
    
    imported_count = 0
    updated_count = 0
    
    for product_data in sample_products:
        try:
            # Check if product exists
            existing_product = await db.get_product_by_id(product_data["id"])
            
            # Calculate discount percentage
            original = product_data["original_price"]
            discounted = product_data["discounted_price"]
            discount_percentage = round(((original - discounted) / original) * 100)
            product_data["discount_percentage"] = discount_percentage
            
            # Add timestamps
            now = datetime.utcnow()
            if not existing_product:
                product_data["created_at"] = now
                product_data["updated_at"] = now
                # Insert new product
                await db.add_product(product_data)
                imported_count += 1
                print(f"✅ Imported: {product_data['name']}")
            else:
                product_data["updated_at"] = now
                product_data["created_at"] = existing_product.get("created_at", now)
                # Update existing product
                await db.update_product(product_data["id"], product_data)
                updated_count += 1
                print(f"🔄 Updated: {product_data['name']}")
                
        except Exception as e:
            print(f"❌ Error importing {product_data.get('name', 'Unknown')}: {e}")
    
    print(f"\n🎉 Import completed!")
    print(f"📦 New products imported: {imported_count}")
    print(f"🔄 Existing products updated: {updated_count}")
    
    return imported_count, updated_count

async def create_content_management_data():
    """Create sample content for admin management"""
    print("\nCreating content management data...")
    
    # This would be stored in a separate content collection
    content_data = {
        "hero_section": {
            "title": "WELCOME TO PREMIUM SHOP",
            "subtitle": "World's #1 Premium Account Shop",
            "description": "Don't miss out on special items at extraordinary sale prices!",
            "cta_primary": "Shop Now",
            "cta_secondary": "Learn More",
            "background_image": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=1200&h=600&fit=crop"
        },
        "promo_banner": {
            "enabled": True,
            "title": "⚡ ChatGPT Plus Offer!",
            "description": "Now on Shop For Premium. Only ₹589 or $12/month",
            "countdown_hours": 1,
            "cta_text": "SHOP NOW!",
            "cta_link": "/products?search=chatgpt",
            "background_color": "#dc2626"
        },
        "trust_section": {
            "enabled": True,
            "main_title": "Why 8,500+ Customers Trust Us",
            "subtitle": "We've been the most trusted premium service provider since 2017",
            "stats": [
                {"label": "Happy Customers", "value": "8,500+", "icon": "😊"},
                {"label": "Orders Delivered", "value": "12,000+", "icon": "📦"},
                {"label": "Countries Served", "value": "25+", "icon": "🌍"},
                {"label": "Success Rate", "value": "99.8%", "icon": "🎯"}
            ]
        },
        "testimonials": [
            {
                "name": "Akshay Vankariant",
                "rating": 5,
                "text": "Absolutely legit and super fast. Got Netflix 4 screen for ₹200. Delivery was super quick. Payment method was UPI so secure. 100% recommended!",
                "verified": True,
                "platform": "Netflix Premium"
            },
            {
                "name": "Chirag Taparia",
                "rating": 5,
                "text": "This was my first purchase and it was a good experience got the account within promised time. Account details working absolutely fine. Will definitely do business again.",
                "verified": True,
                "platform": "Disney+ Hotstar"
            }
        ],
        "site_settings": {
            "site_title": "Shop VIP Premium - Premium Account Shop",
            "site_description": "World's Best VIP Subscriptions at unbeatable prices",
            "contact_email": "support@shopvippremium.com",
            "whatsapp_number": "+91-9876543210",
            "telegram_handle": "@shopvippremium",
            "support_hours": "24/7 Available"
        }
    }
    
    try:
        # Save to database (you would create a content collection)
        await db.save_content_data(content_data)
        print("✅ Content management data created successfully")
    except Exception as e:
        print(f"❌ Error creating content data: {e}")
        # Save to file as fallback
        with open('/app/backend/content_data.json', 'w') as f:
            json.dump(content_data, f, indent=2, default=str)
        print("💾 Content data saved to file as fallback")

async def main():
    print("🚀 Starting content import and management setup...")
    
    try:
        # Import products
        imported, updated = await import_scraped_products()
        
        # Create content management data
        await create_content_management_data()
        
        print(f"\n✨ Setup completed successfully!")
        print(f"📊 Database now has real shopallpremium.com-inspired products")
        print(f"🎛️ Admin can now manage all content through dashboard")
        
    except Exception as e:
        print(f"💥 Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())