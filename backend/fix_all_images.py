import asyncio
from database import db
from models import Product

# Company logo mappings for all products
PRODUCT_LOGOS = {
    'netflix': 'https://img.icons8.com/color/480/netflix.png',
    'amazon': 'https://img.icons8.com/color/480/amazon.png',
    'disney': 'https://img.icons8.com/color/480/disney-plus.png',
    'hbo': 'https://img.icons8.com/color/480/hbo.png',
    'spotify': 'https://img.icons8.com/color/480/spotify.png',
    'apple': 'https://img.icons8.com/color/480/apple-music.png',
    'youtube': 'https://img.icons8.com/color/480/youtube-play.png',
    'adobe': 'https://img.icons8.com/color/480/adobe-creative-cloud.png',
    'microsoft': 'https://img.icons8.com/color/480/microsoft-office-365.png',
    'canva': 'https://img.icons8.com/color/480/canva.png',
    'nordvpn': 'https://img.icons8.com/color/480/vpn.png',
    'expressvpn': 'https://img.icons8.com/color/480/vpn.png',
    'surfshark': 'https://img.icons8.com/color/480/surfshark.png',
    'cyberghost': 'https://img.icons8.com/color/480/ghost.png',
    'coursera': 'https://img.icons8.com/color/480/coursera.png',
    'udemy': 'https://img.icons8.com/color/480/udemy.png',
    'skillshare': 'https://img.icons8.com/color/480/training.png',
    'linkedin': 'https://img.icons8.com/color/480/linkedin.png',
    'grammarly': 'https://img.icons8.com/color/480/grammarly.png',
    'zoom': 'https://img.icons8.com/color/480/zoom.png',
    'steam': 'https://img.icons8.com/color/480/steam.png',
    'epic': 'https://img.icons8.com/color/480/epic-games.png',
    'twitch': 'https://img.icons8.com/color/480/twitch.png',
    'instagram': 'https://img.icons8.com/color/480/instagram.png',
    'tiktok': 'https://img.icons8.com/color/480/tiktok.png',
    'twitter': 'https://img.icons8.com/color/480/twitter.png',
    'facebook': 'https://img.icons8.com/color/480/facebook.png',
    'snapchat': 'https://img.icons8.com/color/480/snapchat.png',
    'telegram': 'https://img.icons8.com/color/480/telegram-app.png',
    'whatsapp': 'https://img.icons8.com/color/480/whatsapp.png',
    'discord': 'https://img.icons8.com/color/480/discord.png',
    'slack': 'https://img.icons8.com/color/480/slack.png',
    'dropbox': 'https://img.icons8.com/color/480/dropbox.png',
    'google': 'https://img.icons8.com/color/480/google-drive.png',
    'onedrive': 'https://img.icons8.com/color/480/onedrive.png',
    'icloud': 'https://img.icons8.com/color/480/icloud.png',
    'github': 'https://img.icons8.com/color/480/github.png',
    'gitlab': 'https://img.icons8.com/color/480/gitlab.png',
    'bitbucket': 'https://img.icons8.com/color/480/bitbucket.png',
    'notion': 'https://img.icons8.com/color/480/notion.png',
    'trello': 'https://img.icons8.com/color/480/trello.png',
    'asana': 'https://img.icons8.com/color/480/asana.png',
    'jira': 'https://img.icons8.com/color/480/jira.png',
    'confluence': 'https://img.icons8.com/color/480/confluence.png',
    'figma': 'https://img.icons8.com/color/480/figma.png',
    'sketch': 'https://img.icons8.com/color/480/sketch.png',
    'invision': 'https://img.icons8.com/color/480/invision.png',
    'miro': 'https://img.icons8.com/color/480/miro.png',
    'loom': 'https://img.icons8.com/color/480/loom.png',
    'calendly': 'https://img.icons8.com/color/480/calendar.png',
    'mailchimp': 'https://img.icons8.com/color/480/mailchimp.png',
    'hubspot': 'https://img.icons8.com/color/480/hubspot.png',
    'salesforce': 'https://img.icons8.com/color/480/salesforce.png',
    'shopify': 'https://img.icons8.com/color/480/shopify.png',
    'wordpress': 'https://img.icons8.com/color/480/wordpress.png',
    'wix': 'https://img.icons8.com/color/480/wix.png',
    'squarespace': 'https://img.icons8.com/color/480/squarespace.png',
    'webflow': 'https://img.icons8.com/color/480/webflow.png',
    'stripe': 'https://img.icons8.com/color/480/stripe.png',
    'paypal': 'https://img.icons8.com/color/480/paypal.png',
    'venmo': 'https://img.icons8.com/color/480/venmo.png',
    'coinbase': 'https://img.icons8.com/color/480/coinbase.png',
    'binance': 'https://img.icons8.com/color/480/binance.png',
    'metamask': 'https://img.icons8.com/color/480/metamask.png',
    'default': 'https://img.icons8.com/color/480/premium.png'
}

def get_logo_for_product(product_name):
    """Get the appropriate logo URL for a product based on its name."""
    name_lower = product_name.lower()
    
    for key, logo_url in PRODUCT_LOGOS.items():
        if key in name_lower:
            return logo_url
    
    # Default logo for unknown products
    return PRODUCT_LOGOS['default']

async def fix_all_product_images():
    """Fix all product images with proper company logos."""
    print("🔧 Fixing all product images with company logos...")
    
    try:
        # Get all products from database
        products = await db.db.products.find().to_list(length=None)
        
        fixed_count = 0
        for product in products:
            # Get appropriate logo
            new_logo_url = get_logo_for_product(product['name'])
            
            # Update the product image
            await db.db.products.update_one(
                {"id": product["id"]},
                {"$set": {"image_url": new_logo_url}}
            )
            
            fixed_count += 1
            print(f"✅ Fixed: {product['name']} -> {new_logo_url}")
        
        print(f"\n🎉 Successfully fixed {fixed_count} product images!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing product images: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(fix_all_product_images())