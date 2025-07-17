import json
import asyncio
from database import db
from models import SearchFilters
from datetime import datetime

async def update_products_only():
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
                # Clean up features - remove bad ones
                clean_features = []
                for feature in detailed_info['features']:
                    if (len(feature) > 10 and len(feature) < 100 and 
                        '$0.00' not in feature and 
                        'November 13, 2024' not in feature and
                        'Helpful?' not in feature and
                        'Reply' not in feature and
                        'Reseller' not in feature):
                        clean_features.append(feature)
                
                # Add default features if not enough clean ones
                if len(clean_features) < 3:
                    default_features = [
                        "Instant delivery within 24 hours",
                        "Premium account with full access",
                        "30-day warranty included",
                        "24/7 customer support",
                        "100% genuine accounts",
                        "Multiple duration options available",
                        "Secure payment processing",
                        "Compatible with all devices"
                    ]
                    clean_features.extend(default_features)
                
                # Update product with detailed information
                update_data = {
                    'description': detailed_info['description'],
                    'features': clean_features[:8],  # Limit to 8 features
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
                print(f"  Features: {len(clean_features)} features")
                
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

if __name__ == "__main__":
    asyncio.run(update_products_only())