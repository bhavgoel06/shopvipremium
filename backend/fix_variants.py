import asyncio
from database import db
from models import SearchFilters
from datetime import datetime

async def fix_all_product_variants():
    """Fix all product variants with proper duration options"""
    
    # Get all products
    all_products = await db.get_products(SearchFilters(page=1, per_page=200))
    
    print(f"Fixing variants for {len(all_products)} products...")
    
    # Define proper duration options for different categories
    duration_options = {
        'ott': ['1 month', '3 months', '6 months', '1 year'],
        'software': ['1 month', '3 months', '6 months', '1 year', 'Lifetime'],
        'vpn': ['1 month', '6 months', '1 year', '2 years'],
        'education': ['1 month', '3 months', '6 months', '1 year'],
        'adult': ['1 month', '3 months', '6 months'],
        'gaming': ['1 month', '3 months', '6 months'],
        'health': ['1 month', '3 months', '6 months', '1 year'],
        'social_media': ['1 month', '3 months', '6 months'],
        'membership': ['1 month', '3 months', '6 months', '1 year'],
        'professional': ['1 month', '3 months', '6 months', '1 year'],
        'financial': ['1 month', '3 months', '6 months', '1 year']
    }
    
    # Special variants for specific products
    special_variants = {
        'Netflix': ['1 Screen', '2 Screens', '4 Screens (4K)', 'Mobile Only'],
        'Spotify': ['Individual', 'Family', 'Student', 'Duo'],
        'Disney+': ['1 month', '3 months', '6 months', '1 year'],
        'Amazon Prime': ['1 month', '3 months', '6 months', '1 year'],
        'YouTube Premium': ['Individual', 'Family', 'Student'],
        'OnlyFans': ['$10 Balance', '$25 Balance', '$50 Balance', '$100 Balance'],
        'ChatGPT': ['Plus Monthly', 'Plus Yearly', 'Team Monthly', 'Team Yearly'],
        'Office 365': ['Personal', 'Family', 'Business Basic', 'Business Premium'],
        'Adobe': ['Single App', 'All Apps', 'Student', 'Business'],
        'Canva': ['Pro Monthly', 'Pro Yearly', 'Team Monthly', 'Team Yearly'],
        'VPN': ['1 month', '6 months', '1 year', '2 years', '3 years'],
        'Coursera': ['Individual', 'Plus', 'For Teams', 'For Universities'],
        'Udemy': ['Personal Plan', 'Pro Plan', 'Team Plan'],
        'LinkedIn': ['Premium Career', 'Premium Business', 'Sales Navigator', 'Recruiter Lite']
    }
    
    updated_count = 0
    
    for product in all_products:
        try:
            # Determine the correct duration options
            product_name = product.name.lower()
            product_category = product.category.value if hasattr(product.category, 'value') else str(product.category)
            
            # Check for special variants first
            correct_variants = None
            for key, variants in special_variants.items():
                if key.lower() in product_name:
                    correct_variants = variants
                    break
            
            # If no special variants, use category-based variants
            if not correct_variants:
                correct_variants = duration_options.get(product_category, ['1 month', '3 months', '6 months', '1 year'])
            
            # Update the product
            await db.db.products.update_one(
                {'id': product.id},
                {'$set': {
                    'duration_options': correct_variants,
                    'updated_at': datetime.utcnow()
                }}
            )
            
            updated_count += 1
            print(f"✓ Updated {updated_count}: {product.name}")
            print(f"  New variants: {correct_variants}")
            
        except Exception as e:
            print(f"✗ Error updating {product.name}: {e}")
            continue
    
    print(f"\n🎉 Successfully updated variants for {updated_count} products!")
    
    # Show some examples
    print("\n📝 Sample updated products:")
    sample_products = await db.get_products(SearchFilters(page=1, per_page=5))
    for product in sample_products:
        print(f"\n- {product.name}")
        print(f"  Variants: {product.duration_options}")
        print(f"  Category: {product.category}")

if __name__ == "__main__":
    asyncio.run(fix_all_product_variants())