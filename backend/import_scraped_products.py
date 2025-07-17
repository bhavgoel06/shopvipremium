import json
import asyncio
from database import db
from models import Product, CategoryType
import uuid
from datetime import datetime, timedelta
import random

async def import_products_from_json():
    """Import all products from the scraped JSON file"""
    
    # Load the scraped data
    with open('shopallpremium_products.json', 'r', encoding='utf-8') as f:
        scraped_products = json.load(f)
    
    print(f"Loading {len(scraped_products)} products from JSON...")
    
    # Clear existing products
    try:
        await db.db.products.delete_many({})
        print("Cleared existing products from database")
    except Exception as e:
        print(f"Error clearing products: {e}")
    
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
    
    # Import products
    imported_count = 0
    
    for i, scraped_product in enumerate(scraped_products):
        try:
            # Enhanced category detection
            name_lower = scraped_product.get('name', '').lower()
            category = 'ott'  # default
            
            if any(keyword in name_lower for keyword in ['onlyfans', 'mofos', 'reality kings', 'teamskeet', 'digital playground', 'adult', 'xvid', 'porn']):
                category = 'adult'
            elif any(keyword in name_lower for keyword in ['adobe', 'canva', 'picsart', 'office', 'software', 'malwarebytes', 'antivirus']):
                category = 'software'
            elif any(keyword in name_lower for keyword in ['vpn', 'proxy', 'security']):
                category = 'vpn'
            elif any(keyword in name_lower for keyword in ['udemy', 'coursera', 'leetcode', 'education', 'learning', 'course']):
                category = 'education'
            elif any(keyword in name_lower for keyword in ['linkedin', 'instagram', 'twitter', 'social']):
                category = 'social_media'
            elif any(keyword in name_lower for keyword in ['gaming', 'game', 'steam', 'xbox', 'playstation']):
                category = 'gaming'
            elif any(keyword in name_lower for keyword in ['health', 'fitness', 'workout', 'medical']):
                category = 'health'
            elif any(keyword in name_lower for keyword in ['membership', 'vip', 'premium', 'reseller']):
                category = 'membership'
            elif any(keyword in name_lower for keyword in ['trading', 'business', 'professional', 'work']):
                category = 'professional'
            elif any(keyword in name_lower for keyword in ['financial', 'money', 'investment', 'trading']):
                category = 'financial'
            
            # Generate product data
            product_data = {
                'id': str(uuid.uuid4()),
                'name': scraped_product.get('name', ''),
                'slug': scraped_product.get('name', '').lower().replace(' ', '-').replace('–', '-'),
                'short_description': scraped_product.get('short_description', '')[:200] or f"Premium {scraped_product.get('name', '')} subscription at discounted price",
                'description': scraped_product.get('description', '') or f"Get access to {scraped_product.get('name', '')} premium features at an unbeatable price. Instant delivery guaranteed.",
                'features': scraped_product.get('features', [])[:5] or [
                    "Instant delivery within 24 hours",
                    "Premium account with full access",
                    "30-day warranty included",
                    "24/7 customer support",
                    "100% genuine accounts"
                ],
                'original_price': scraped_product.get('original_price', 100.0) or 100.0,
                'discounted_price': scraped_product.get('discounted_price', 50.0) or 50.0,
                'discount_percentage': scraped_product.get('discount_percentage', 50) or 50,
                'currency': 'INR',
                'category': category_mapping.get(category, CategoryType.OTT),
                'subcategory': scraped_product.get('name', '').split(' ')[0] if scraped_product.get('name') else 'premium',
                'image_url': scraped_product.get('image_url', '') or 'https://via.placeholder.com/300x200',
                'gallery_images': scraped_product.get('gallery_images', [])[:3],
                'rating': scraped_product.get('rating', 0.0) or round(random.uniform(4.0, 5.0), 1),
                'total_reviews': scraped_product.get('total_reviews', 0) or random.randint(50, 500),
                'stock_quantity': scraped_product.get('stock_quantity', 100) or random.randint(50, 200),
                'is_featured': scraped_product.get('is_featured', False) or (i < 10),  # First 10 are featured
                'is_bestseller': scraped_product.get('is_bestseller', False) or (i < 5),  # First 5 are bestsellers
                'status': 'active',
                'seo_title': f"{scraped_product.get('name', '')} - Premium Subscription | Shop For Premium",
                'seo_description': f"Get {scraped_product.get('name', '')} premium subscription at {scraped_product.get('discount_percentage', 50)}% off. Instant delivery, 30-day warranty, 24/7 support.",
                'seo_keywords': scraped_product.get('seo_keywords', []) or [
                    scraped_product.get('name', '').lower(),
                    'premium',
                    'subscription',
                    'discount'
                ],
                'duration_options': scraped_product.get('variants', []) or [
                    "1 month",
                    "3 months", 
                    "6 months",
                    "1 year"
                ],
                'subscription_options': scraped_product.get('variants', []) or [
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
            print(f"✓ Imported {imported_count}/{len(scraped_products)}: {product.name}")
            
        except Exception as e:
            print(f"✗ Error importing product {i+1}: {e}")
            continue
    
    print(f"\n🎉 Successfully imported {imported_count} products!")
    
    # Show category breakdown
    category_counts = {}
    for product in scraped_products:
        name_lower = product.get('name', '').lower()
        category = 'ott'  # default
        
        if any(keyword in name_lower for keyword in ['onlyfans', 'mofos', 'reality kings', 'teamskeet', 'digital playground', 'adult', 'xvid', 'porn']):
            category = 'adult'
        elif any(keyword in name_lower for keyword in ['adobe', 'canva', 'picsart', 'office', 'software', 'malwarebytes', 'antivirus']):
            category = 'software'
        elif any(keyword in name_lower for keyword in ['vpn', 'proxy', 'security']):
            category = 'vpn'
        elif any(keyword in name_lower for keyword in ['udemy', 'coursera', 'leetcode', 'education', 'learning', 'course']):
            category = 'education'
        elif any(keyword in name_lower for keyword in ['linkedin', 'instagram', 'twitter', 'social']):
            category = 'social_media'
        elif any(keyword in name_lower for keyword in ['gaming', 'game', 'steam', 'xbox', 'playstation']):
            category = 'gaming'
        elif any(keyword in name_lower for keyword in ['health', 'fitness', 'workout', 'medical']):
            category = 'health'
        elif any(keyword in name_lower for keyword in ['membership', 'vip', 'premium', 'reseller']):
            category = 'membership'
        elif any(keyword in name_lower for keyword in ['trading', 'business', 'professional', 'work']):
            category = 'professional'
        elif any(keyword in name_lower for keyword in ['financial', 'money', 'investment', 'trading']):
            category = 'financial'
        
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\n📊 Category breakdown:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} products")

if __name__ == "__main__":
    asyncio.run(import_products_from_json())