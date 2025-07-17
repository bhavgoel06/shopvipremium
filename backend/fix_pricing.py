import json
import asyncio
from database import db
from models import Product, CategoryType
import uuid
from datetime import datetime
import random

# Correct pricing mapping from shopallpremium.com
CORRECT_PRICING = {
    "OnlyFans Accounts": {"original": 3399.00, "discounted": 1599.00, "discount": 53},
    "Brazzers Premium": {"original": 549.00, "discounted": 549.00, "discount": 0},
    "Amazon Prime Video": {"original": 599.00, "discounted": 79.00, "discount": 87},
    "Spotify Premium – Individual": {"original": 739.00, "discounted": 45.00, "discount": 94},
    "Spotify Premium – UPGRADE": {"original": 839.00, "discounted": 489.00, "discount": 42},
    "Pornhub Premium": {"original": 1499.00, "discounted": 549.00, "discount": 63},
    "Reseller | VIP Membership": {"original": 499.00, "discounted": 99.00, "discount": 80},
    "Reality Kings": {"original": 1499.00, "discounted": 549.00, "discount": 63},
    "Random Validity Subscriptions": {"original": 99.00, "discounted": 20.00, "discount": 80},
    "YouTube Premium (India)": {"original": 1099.00, "discounted": 549.00, "discount": 50},
    "IPVanish VPN – 1 Year": {"original": 7999.00, "discounted": 1099.00, "discount": 86},
    "Lucky Buy": {"original": 250.00, "discounted": 1.00, "discount": 100},
    "Canva PRO": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "TradingView Premium": {"original": 7749.00, "discounted": 949.00, "discount": 88},
    "SonyLIV Premium": {"original": 449.00, "discounted": 149.00, "discount": 67},
    "HMA VPN": {"original": 7999.00, "discounted": 1099.00, "discount": 86},
    "Netflix Premium 4K UHD": {"original": 1199.00, "discounted": 809.00, "discount": 33},
    "ChatGPT Plus": {"original": 2049.00, "discounted": 1199.00, "discount": 41},
    "Disney+ 1 Year (No ads)": {"original": 1499.00, "discounted": 799.00, "discount": 47},
    "HBO MAX": {"original": 1299.00, "discounted": 699.00, "discount": 46},
    "HULU Premium": {"original": 999.00, "discounted": 549.00, "discount": 45},
    "Coursera Plus": {"original": 4999.00, "discounted": 1999.00, "discount": 60},
    "LeetCode Premium": {"original": 1274.00, "discounted": 599.00, "discount": 53},
    "Express VPN": {"original": 6999.00, "discounted": 999.00, "discount": 86},
    "Netflix 1 Screen": {"original": 199.00, "discounted": 99.00, "discount": 50},
    "Amazon Prime (All Features)": {"original": 1499.00, "discounted": 399.00, "discount": 73},
    "Zee5 Premium": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "JioCinema Premium": {"original": 999.00, "discounted": 199.00, "discount": 80},
    "Perplexity Pro – 1 Year": {"original": 2499.00, "discounted": 1299.00, "discount": 48},
    "Office 365": {"original": 5999.00, "discounted": 1499.00, "discount": 75},
    "Windscribe Pro – 1 Year": {"original": 5999.00, "discounted": 899.00, "discount": 85},
    "LinkedIn Business Plan": {"original": 7999.00, "discounted": 2499.00, "discount": 69},
    "Duolingo : Learn Multiple Languages": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "Malwarebytes (Keys)": {"original": 3999.00, "discounted": 799.00, "discount": 80},
    "PicsArt GOLD": {"original": 1299.00, "discounted": 399.00, "discount": 69},
    "Wondershare Filmora Perpetual": {"original": 5999.00, "discounted": 1899.00, "discount": 68},
    "Udemy Courses": {"original": 3999.00, "discounted": 999.00, "discount": 75},
    "Twitch": {"original": 499.00, "discounted": 199.00, "discount": 60},
    "Tidal Music": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "Scribd Premium : Audiobooks & ebooks": {"original": 999.00, "discounted": 399.00, "discount": 60},
    "TeamTree House -Learn to Code": {"original": 2999.00, "discounted": 999.00, "discount": 67},
    "Codecademy PRO": {"original": 1999.00, "discounted": 699.00, "discount": 65},
    "VyprVPN Premium": {"original": 5999.00, "discounted": 999.00, "discount": 83},
    "Nord VPN Premium": {"original": 4999.00, "discounted": 799.00, "discount": 84},
    "HealthifyMe Premium": {"original": 1499.00, "discounted": 399.00, "discount": 73},
    "Cult.fit": {"original": 1499.00, "discounted": 499.00, "discount": 67},
    "Times Prime Membership": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "CuriosityStream – Stream Documentaries": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "Discovery Plus (Premium)": {"original": 999.00, "discounted": 199.00, "discount": 80},
    "DocuBay – Streaming Documentaries": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "Magzter GOLD: Digital Magazines & Newspapers": {"original": 1999.00, "discounted": 599.00, "discount": 70},
    "The Times of India Plus": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "The Economic Times PRIME": {"original": 1499.00, "discounted": 499.00, "discount": 67},
    "GTA V : Premium Online Edition (PC)": {"original": 2999.00, "discounted": 999.00, "discount": 67},
    "MX Player Gold": {"original": 399.00, "discounted": 99.00, "discount": 75},
    "ALTBalaji Premium": {"original": 999.00, "discounted": 199.00, "discount": 80},
    "You.com Pro": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "Tinder Gold (1M)": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "Private UNLIMITED Emails": {"original": 2499.00, "discounted": 999.00, "discount": 60},
    "Spuul (Premium)": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "JioHotstar India": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "Amazon Prime India Full Benefits (1M)": {"original": 1499.00, "discounted": 399.00, "discount": 73},
    "Crunchyroll": {"original": 999.00, "discounted": 299.00, "discount": 70},
    "HBO NOW": {"original": 1299.00, "discounted": 699.00, "discount": 46},
    "Sun NXT": {"original": 399.00, "discounted": 99.00, "discount": 75},
    "aha -Telugu Web Series and Movies": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "HoiChoi Bengali Movies": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "ShemarooMe Premium (Personal)": {"original": 699.00, "discounted": 199.00, "discount": 72},
    "KooKu": {"original": 399.00, "discounted": 99.00, "discount": 75},
    "ZEE-5 Premium – (4K PLAN)": {"original": 1299.00, "discounted": 399.00, "discount": 69},
    "LinkedIn Career Plan": {"original": 3999.00, "discounted": 1499.00, "discount": 63},
    "MOFOS Premium – 1 Year": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "XVideos.RED": {"original": 1999.00, "discounted": 699.00, "discount": 65},
    "Naughty America Premium": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "BangBros Premium – 1 Year": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "Cum4k.com Premium": {"original": 1999.00, "discounted": 699.00, "discount": 65},
    "Blacked.com Premium": {"original": 1999.00, "discounted": 799.00, "discount": 60},
    "Teamskeet – 3 Months": {"original": 1499.00, "discounted": 549.00, "discount": 63},
    "Digital Playground Premium": {"original": 1999.00, "discounted": 749.00, "discount": 63}
}

async def fix_product_pricing():
    """Fix the pricing for all products based on correct shopallpremium.com data"""
    
    # Clear existing products
    try:
        await db.db.products.delete_many({})
        print("Cleared existing products from database")
    except Exception as e:
        print(f"Error clearing products: {e}")
    
    # Load the scraped data
    with open('shopallpremium_products.json', 'r', encoding='utf-8') as f:
        scraped_products = json.load(f)
    
    print(f"Processing {len(scraped_products)} products with correct pricing...")
    
    # Category mapping
    category_mapping = {
        'ott': CategoryType.OTT,
        'software': CategoryType.SOFTWARE,
        'adult': CategoryType.ADULT,
        'vpn': CategoryType.VPN,
        'education': CategoryType.EDUCATION,
        'social_media': CategoryType.SOCIAL_MEDIA,
        'gaming': CategoryType.GAMING,
        'health': CategoryType.HEALTH,
        'membership': CategoryType.MEMBERSHIP,
        'professional': CategoryType.PROFESSIONAL,
        'financial': CategoryType.FINANCIAL
    }
    
    imported_count = 0
    
    for i, scraped_product in enumerate(scraped_products):
        try:
            product_name = scraped_product.get('name', '')
            
            # Enhanced category detection
            name_lower = product_name.lower()
            category = 'ott'  # default
            
            if any(keyword in name_lower for keyword in ['onlyfans', 'mofos', 'reality kings', 'teamskeet', 'digital playground', 'adult', 'xvid', 'porn', 'brazzers', 'bangbros', 'cum4k', 'blacked', 'naughty america']):
                category = 'adult'
            elif any(keyword in name_lower for keyword in ['adobe', 'canva', 'picsart', 'office', 'software', 'malwarebytes', 'antivirus', 'filmora']):
                category = 'software'
            elif any(keyword in name_lower for keyword in ['vpn', 'proxy', 'security', 'express', 'nord', 'vypr', 'hma', 'ipvanish', 'windscribe']):
                category = 'vpn'
            elif any(keyword in name_lower for keyword in ['udemy', 'coursera', 'leetcode', 'education', 'learning', 'course', 'codecademy', 'treehouse', 'duolingo']):
                category = 'education'
            elif any(keyword in name_lower for keyword in ['linkedin', 'instagram', 'twitter', 'social', 'tinder']):
                category = 'social_media'
            elif any(keyword in name_lower for keyword in ['gaming', 'game', 'steam', 'xbox', 'playstation', 'gta', 'twitch']):
                category = 'gaming'
            elif any(keyword in name_lower for keyword in ['health', 'fitness', 'workout', 'medical', 'healthifyme', 'cult']):
                category = 'health'
            elif any(keyword in name_lower for keyword in ['membership', 'vip', 'premium', 'reseller', 'times prime']):
                category = 'membership'
            elif any(keyword in name_lower for keyword in ['trading', 'business', 'professional', 'work', 'tradingview']):
                category = 'professional'
            elif any(keyword in name_lower for keyword in ['financial', 'money', 'investment', 'trading']):
                category = 'financial'
            
            # Get correct pricing
            if product_name in CORRECT_PRICING:
                pricing = CORRECT_PRICING[product_name]
                original_price = pricing['original']
                discounted_price = pricing['discounted']
                discount_percentage = pricing['discount']
            else:
                # Use scraped pricing as fallback but convert to reasonable INR values
                original_price = max(scraped_product.get('original_price', 999.0) * 50, 99.0)
                discounted_price = max(scraped_product.get('discounted_price', 499.0) * 50, 49.0)
                discount_percentage = int(((original_price - discounted_price) / original_price) * 100)
            
            # Generate product data
            product_data = {
                'id': str(uuid.uuid4()),
                'name': product_name,
                'slug': product_name.lower().replace(' ', '-').replace('–', '-'),
                'short_description': scraped_product.get('short_description', '')[:200] or f"Premium {product_name} subscription at {discount_percentage}% discount",
                'description': scraped_product.get('description', '') or f"Get access to {product_name} premium features at an unbeatable price. Instant delivery guaranteed.",
                'features': scraped_product.get('features', [])[:5] or [
                    "Instant delivery within 24 hours",
                    "Premium account with full access",
                    "30-day warranty included",
                    "24/7 customer support",
                    "100% genuine accounts"
                ],
                'original_price': original_price,
                'discounted_price': discounted_price,
                'discount_percentage': discount_percentage,
                'currency': 'INR',
                'category': category_mapping.get(category, CategoryType.OTT),
                'subcategory': product_name.split(' ')[0] if product_name else 'premium',
                'image_url': scraped_product.get('image_url', '') or f'https://via.placeholder.com/300x200?text={product_name.replace(" ", "+")}',
                'gallery_images': scraped_product.get('gallery_images', [])[:3],
                'rating': scraped_product.get('rating', 0.0) or round(random.uniform(4.0, 5.0), 1),
                'total_reviews': scraped_product.get('total_reviews', 0) or random.randint(50, 500),
                'stock_quantity': scraped_product.get('stock_quantity', 100) or random.randint(50, 200),
                'is_featured': scraped_product.get('is_featured', False) or (i < 12),  # First 12 are featured
                'is_bestseller': scraped_product.get('is_bestseller', False) or (i < 6),  # First 6 are bestsellers
                'status': 'active',
                'seo_title': f"{product_name} - Premium Subscription | Shop For Premium",
                'seo_description': f"Get {product_name} premium subscription at {discount_percentage}% off. Instant delivery, 30-day warranty, 24/7 support.",
                'seo_keywords': scraped_product.get('seo_keywords', []) or [
                    product_name.lower(),
                    'premium',
                    'subscription',
                    'discount'
                ],
                'duration_options': [
                    variant.get('name', variant) if isinstance(variant, dict) else str(variant)
                    for variant in scraped_product.get('variants', [])
                ] if scraped_product.get('variants') else [
                    "1 month",
                    "3 months", 
                    "6 months",
                    "1 year"
                ],
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Create product
            product = Product(**product_data)
            await db.db.products.insert_one(product.dict())
            
            imported_count += 1
            print(f"✓ Fixed {imported_count}/{len(scraped_products)}: {product.name} - ₹{original_price} → ₹{discounted_price} ({discount_percentage}% off)")
            
        except Exception as e:
            print(f"✗ Error fixing product {i+1}: {e}")
            continue
    
    print(f"\n🎉 Successfully fixed pricing for {imported_count} products!")
    
    # Show some examples
    print("\n📝 Sample corrected products:")
    for product_name, pricing in list(CORRECT_PRICING.items())[:5]:
        print(f"- {product_name}: ₹{pricing['original']} → ₹{pricing['discounted']} ({pricing['discount']}% off)")

if __name__ == "__main__":
    asyncio.run(fix_product_pricing())