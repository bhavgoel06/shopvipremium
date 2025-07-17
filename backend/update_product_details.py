import json
import asyncio
from database import db
from models import Product, CategoryType
import uuid
from datetime import datetime

async def update_products_with_detailed_info():
    """Update existing products with detailed scraped information"""
    
    # Load the detailed scraped data
    with open('detailed_products.json', 'r', encoding='utf-8') as f:
        detailed_products = json.load(f)
    
    print(f"Loading {len(detailed_products)} detailed products...")
    
    # Create a mapping of product names to detailed info
    detailed_map = {}
    for product in detailed_products:
        # Normalize product name for matching
        normalized_name = product['name'].lower().strip()
        detailed_map[normalized_name] = product
    
    # Get all existing products from database
    from models import SearchFilters
    existing_products = await db.get_products(SearchFilters(page=1, per_page=200))
    
    updated_count = 0
    
    for existing_product in existing_products:
        try:
            # Try to find matching detailed product
            normalized_existing = existing_product.name.lower().strip()
            
            # Direct match first
            detailed_info = detailed_map.get(normalized_existing)
            
            # If no direct match, try partial matches
            if not detailed_info:
                for detailed_name, detailed_data in detailed_map.items():
                    if (detailed_name in normalized_existing or 
                        normalized_existing in detailed_name or
                        # Check for key terms
                        (any(term in detailed_name for term in normalized_existing.split()) and
                         any(term in normalized_existing for term in detailed_name.split()))):
                        detailed_info = detailed_data
                        break
            
            if detailed_info:
                # Update product with detailed information
                update_data = {
                    'description': detailed_info['description'],
                    'features': detailed_info['features'][:8],  # Limit to 8 features
                    'updated_at': datetime.utcnow()
                }
                
                # Update in database
                await db.db.products.update_one(
                    {'id': existing_product.id},
                    {'$set': update_data}
                )
                
                updated_count += 1
                print(f"✓ Updated {updated_count}: {existing_product.name}")
                print(f"  Description: {detailed_info['description'][:80]}...")
                print(f"  Features: {len(detailed_info['features'])} features")
                
            else:
                print(f"✗ No detailed info found for: {existing_product.name}")
                
        except Exception as e:
            print(f"✗ Error updating {existing_product.name}: {e}")
            continue
    
    print(f"\n🎉 Successfully updated {updated_count} products with detailed information!")
    
    # Show a sample of updated products
    print("\n📝 Sample updated products:")
    sample_products = await db.get_products(SearchFilters(page=1, per_page=3))
    for product in sample_products:
        print(f"\n- {product.name}")
        print(f"  Description: {product.description[:100]}...")
        print(f"  Features: {product.features[:3]}")

async def add_reviews_to_products():
    """Add the scraped reviews to products"""
    
    # Load the detailed scraped data
    with open('detailed_products.json', 'r', encoding='utf-8') as f:
        detailed_products = json.load(f)
    
    print(f"Adding reviews to products...")
    
    # Create reviews collection if it doesn't exist
    reviews_to_add = []
    
    for detailed_product in detailed_products:
        product_name = detailed_product['name']
        
        # Find the product in database
        existing_products = await db.search_products(product_name.split()[0], 5)
        
        if existing_products:
            product = existing_products[0]  # Take the first match
            
            # Add reviews for this product
            for review_data in detailed_product.get('reviews', []):
                review = {
                    'id': str(uuid.uuid4()),
                    'product_id': product.id,
                    'product_name': product.name,
                    'reviewer_name': review_data['reviewer_name'],
                    'rating': review_data['rating'],
                    'review_text': review_data['review_text'],
                    'date': review_data['date'],
                    'created_at': datetime.utcnow()
                }
                reviews_to_add.append(review)
    
    # Insert all reviews
    if reviews_to_add:
        await db.db.reviews.insert_many(reviews_to_add)
        print(f"✓ Added {len(reviews_to_add)} reviews to database")
    
    # Update product review counts
    for detailed_product in detailed_products:
        product_name = detailed_product['name']
        existing_products = await db.search_products(product_name.split()[0], 5)
        
        if existing_products:
            product = existing_products[0]
            
            # Update product with review stats
            await db.db.products.update_one(
                {'id': product.id},
                {'$set': {
                    'total_reviews': detailed_product.get('total_reviews', 0),
                    'rating': detailed_product.get('rating', 4.5)
                }}
            )

if __name__ == "__main__":
    asyncio.run(update_products_with_detailed_info())
    asyncio.run(add_reviews_to_products())