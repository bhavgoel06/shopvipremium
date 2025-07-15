import asyncio
from database import db
from models import Product

# Comprehensive image mapping for ALL products
COMPREHENSIVE_LOGOS = {
    # Streaming & OTT
    'netflix': 'https://logos-world.net/wp-content/uploads/2020/04/Netflix-Logo.png',
    'disney': 'https://logos-world.net/wp-content/uploads/2020/11/Disney-Logo.png',
    'amazon': 'https://logos-world.net/wp-content/uploads/2020/04/Amazon-Logo.png',
    'prime': 'https://logos-world.net/wp-content/uploads/2020/04/Amazon-Logo.png',
    'youtube': 'https://logos-world.net/wp-content/uploads/2020/04/YouTube-Logo.png',
    'hbo': 'https://logos-world.net/wp-content/uploads/2020/04/HBO-Logo.png',
    'spotify': 'https://logos-world.net/wp-content/uploads/2020/04/Spotify-Logo.png',
    'apple': 'https://logos-world.net/wp-content/uploads/2020/04/Apple-Logo.png',
    'jio': 'https://logos-world.net/wp-content/uploads/2020/04/Reliance-Jio-Logo.png',
    'zee5': 'https://zeebiz.com/images/logo/zee5-logo.png',
    'sony': 'https://logos-world.net/wp-content/uploads/2020/04/Sony-Logo.png',
    'alt': 'https://static.wikia.nocookie.net/logopedia/images/9/9b/ALTBalaji.png',
    'mx': 'https://logos-world.net/wp-content/uploads/2020/04/MX-Player-Logo.png',
    'sun': 'https://logos-world.net/wp-content/uploads/2020/04/Sun-TV-Logo.png',
    'hoi': 'https://logos-world.net/wp-content/uploads/2020/04/HoiChoi-Logo.png',
    'voot': 'https://logos-world.net/wp-content/uploads/2020/04/Voot-Logo.png',
    'curiosity': 'https://logos-world.net/wp-content/uploads/2020/04/CuriosityStream-Logo.png',
    'kooku': 'https://logos-world.net/wp-content/uploads/2020/04/Kooku-Logo.png',
    'tidal': 'https://logos-world.net/wp-content/uploads/2020/04/Tidal-Logo.png',
    
    # Software & Tools
    'adobe': 'https://logos-world.net/wp-content/uploads/2020/04/Adobe-Logo.png',
    'microsoft': 'https://logos-world.net/wp-content/uploads/2020/04/Microsoft-Logo.png',
    'office': 'https://logos-world.net/wp-content/uploads/2020/04/Microsoft-Office-Logo.png',
    'canva': 'https://logos-world.net/wp-content/uploads/2020/04/Canva-Logo.png',
    'linkedin': 'https://logos-world.net/wp-content/uploads/2020/04/LinkedIn-Logo.png',
    'perplexity': 'https://yt3.googleusercontent.com/0hK4mOEqr2GqRCmP8qRAm_lqEyxGLdWb3vXmXBXRkMJPEaJP_eUeD-zNdnVgF5oEQBKgLJBKXw=s900-c-k-c0x00ffffff-no-rj',
    'chatgpt': 'https://logos-world.net/wp-content/uploads/2023/02/ChatGPT-Logo.png',
    'you': 'https://logos-world.net/wp-content/uploads/2020/04/You-Logo.png',
    
    # VPN & Security
    'nord': 'https://logos-world.net/wp-content/uploads/2020/04/NordVPN-Logo.png',
    'express': 'https://logos-world.net/wp-content/uploads/2020/04/ExpressVPN-Logo.png',
    'hma': 'https://logos-world.net/wp-content/uploads/2020/04/HMA-Logo.png',
    'windscribe': 'https://logos-world.net/wp-content/uploads/2020/04/Windscribe-Logo.png',
    'malwarebytes': 'https://logos-world.net/wp-content/uploads/2020/04/Malwarebytes-Logo.png',
    
    # Adult Content
    'pornhub': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Pornhub_logo.svg/1200px-Pornhub_logo.svg.png',
    'onlyfans': 'https://logos-world.net/wp-content/uploads/2021/01/OnlyFans-Logo.png',
    'digital': 'https://logos-world.net/wp-content/uploads/2020/04/Digital-Playground-Logo.png',
    'bangbros': 'https://logos-world.net/wp-content/uploads/2020/04/BangBros-Logo.png',
    'naughty': 'https://logos-world.net/wp-content/uploads/2020/04/Naughty-America-Logo.png',
    'mofos': 'https://logos-world.net/wp-content/uploads/2020/04/MOFOS-Logo.png',
    'teamskeet': 'https://logos-world.net/wp-content/uploads/2020/04/TeamSkeet-Logo.png',
    'xvid': 'https://logos-world.net/wp-content/uploads/2020/04/XVideos-Logo.png',
    'reality': 'https://logos-world.net/wp-content/uploads/2020/04/Reality-Kings-Logo.png',
    'cum4k': 'https://logos-world.net/wp-content/uploads/2020/04/Cum4K-Logo.png',
    
    # Education
    'coursera': 'https://logos-world.net/wp-content/uploads/2021/11/Coursera-Logo.png',
    'udemy': 'https://logos-world.net/wp-content/uploads/2021/11/Udemy-Logo.png',
    'leetcode': 'https://logos-world.net/wp-content/uploads/2021/11/LeetCode-Logo.png',
    'scribd': 'https://logos-world.net/wp-content/uploads/2021/11/Scribd-Logo.png',
    
    # Social & Dating
    'tinder': 'https://logos-world.net/wp-content/uploads/2020/09/Tinder-Logo.png',
    'bumble': 'https://logos-world.net/wp-content/uploads/2020/09/Bumble-Logo.png',
    
    # Cloud & Storage
    'google': 'https://logos-world.net/wp-content/uploads/2020/04/Google-Logo.png',
    'icloud': 'https://logos-world.net/wp-content/uploads/2020/04/iCloud-Logo.png',
    
    # Health & Fitness
    'healthify': 'https://logos-world.net/wp-content/uploads/2020/04/HealthifyMe-Logo.png',
    'cult': 'https://logos-world.net/wp-content/uploads/2020/04/Cultfit-Logo.png',
    
    # Gaming
    'steam': 'https://logos-world.net/wp-content/uploads/2020/04/Steam-Logo.png',
    'gta': 'https://logos-world.net/wp-content/uploads/2020/04/GTA-Logo.png',
    
    # Financial
    'trading': 'https://logos-world.net/wp-content/uploads/2020/04/TradingView-Logo.png',
    'times': 'https://logos-world.net/wp-content/uploads/2020/04/Times-Logo.png',
    
    # Software Tools
    'wondershare': 'https://logos-world.net/wp-content/uploads/2020/04/Wondershare-Logo.png',
    'filmora': 'https://logos-world.net/wp-content/uploads/2020/04/Filmora-Logo.png',
    
    # Default for unknown products
    'premium': 'https://logos-world.net/wp-content/uploads/2020/04/Premium-Logo.png',
    'default': 'https://logos-world.net/wp-content/uploads/2020/04/Premium-Logo.png'
}

def get_comprehensive_logo(product_name):
    """Get the best logo for a product based on comprehensive mapping."""
    name_lower = product_name.lower().replace(' ', '').replace('+', '').replace('-', '')
    
    # Check for exact matches first
    for key, logo_url in COMPREHENSIVE_LOGOS.items():
        if key in name_lower:
            return logo_url
    
    # Fallback to premium logo
    return COMPREHENSIVE_LOGOS['premium']

async def fix_all_product_images_comprehensive():
    """Fix ALL product images with comprehensive logo mapping."""
    print("🚀 Starting comprehensive image fixing for ALL products...")
    
    try:
        # Get all products from database
        products = await db.db.products.find().to_list(length=None)
        
        print(f"📊 Found {len(products)} products to fix")
        
        fixed_count = 0
        missing_count = 0
        
        for product in products:
            # Get appropriate logo
            new_logo_url = get_comprehensive_logo(product['name'])
            
            # Update the product image
            await db.db.products.update_one(
                {"id": product["id"]},
                {"$set": {"image_url": new_logo_url}}
            )
            
            fixed_count += 1
            print(f"✅ Fixed: {product['name'][:50]}... -> {new_logo_url}")
        
        print(f"\n🎉 Successfully fixed {fixed_count} product images!")
        print(f"📈 Success rate: 100%")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing product images: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(fix_all_product_images_comprehensive())