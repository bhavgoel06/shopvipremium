import asyncio
from database import db
from models import SearchFilters
from collections import defaultdict

async def remove_duplicates():
    """Remove duplicate products from database"""
    
    products = await db.get_products(SearchFilters(page=1, per_page=200))
    print(f'Total products before cleanup: {len(products)}')
    
    # Group products by name
    product_groups = defaultdict(list)
    for product in products:
        product_groups[product.name].append(product)
    
    # Remove duplicates (keep the first one)
    removed_count = 0
    for name, group in product_groups.items():
        if len(group) > 1:
            print(f'Removing duplicates for: {name} ({len(group)} copies)')
            # Keep the first one, remove the rest
            for product in group[1:]:
                await db.db.products.delete_one({'id': product.id})
                removed_count += 1
    
    print(f'Removed {removed_count} duplicate products')
    
    # Check final count
    final_products = await db.get_products(SearchFilters(page=1, per_page=200))
    print(f'Total products after cleanup: {len(final_products)}')

if __name__ == "__main__":
    asyncio.run(remove_duplicates())