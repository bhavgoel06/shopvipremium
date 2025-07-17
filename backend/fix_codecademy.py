import asyncio
from database import db
from models import SearchFilters

async def update_codecademy_description():
    """Update Codecademy PRO with correct description and features"""
    
    # Get Codecademy product
    products = await db.get_products(SearchFilters(search='codecademy', limit=1))
    if not products:
        print("Codecademy product not found")
        return
    
    product = products[0]
    print(f"Updating: {product.name}")
    
    # Correct description from shopallpremium.com
    description = """Codecademy PRO helps you review and practice what you learn on the web, anywhere, anytime. Learn to code the easy way.

"Taking a few minutes a day to reinforce the underlying concepts has been an easy way to remember them, even on days when I'm not coding." — Chance N., Codecademy Go Learner

"Comparing it to all of the other coding apps I have tried this one is best at bringing together learning, practicing, and practicality via articles into one place." — Sean M., Codecademy Go Learner

Comes with 6 Months | 1 Year Subscription Plan. Important Terms: Do Not try to change the E-Mail or Password. TYPE: Account (EMAIL & Password). VALIDITY: 6 Months | 1 Year. Cracked Account."""
    
    # Correct features from shopallpremium.com
    features = [
        "Discover a new way to practice coding syntax",
        "Remember more with daily flashcards that you can quickly skim",
        "Review whenever, wherever. Leave the desktop",
        "Learn how to apply your skills in your day-to-day with advice from industry leaders",
        "Maintain streaks and track your progress",
        "Learn Web Development, Data Science, Computer Science",
        "HTML & CSS, Python, JavaScript, SQL support",
        "6 Months | 1 Year subscription options"
    ]
    
    # Update the product
    await db.db.products.update_one(
        {'id': product.id},
        {'$set': {
            'description': description,
            'features': features,
            'short_description': "Codecademy PRO helps you review and practice what you learn on the web, anywhere, anytime. Learn to code the easy way."
        }}
    )
    
    print("✓ Updated Codecademy PRO description and features")
    
    # Show the updated product
    updated_product = await db.get_products(SearchFilters(search='codecademy', limit=1))
    if updated_product:
        product = updated_product[0]
        print(f"\nUpdated product:")
        print(f"Name: {product.name}")
        print(f"Price: ₹{product.original_price} → ₹{product.discounted_price}")
        print(f"Description: {product.description[:100]}...")
        print(f"Features: {product.features}")

if __name__ == "__main__":
    asyncio.run(update_codecademy_description())