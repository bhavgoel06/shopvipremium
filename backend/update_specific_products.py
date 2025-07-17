import requests
from bs4 import BeautifulSoup
import asyncio
from database import db
from models import SearchFilters
import time

async def scrape_and_update_specific_products():
    """Scrape specific products and update with real descriptions"""
    
    # Define specific product URLs for better scraping
    product_urls = {
        'LeetCode Premium': 'https://shopallpremium.com/product/leetcode-premium/',
        'Netflix Premium 4K UHD': 'https://shopallpremium.com/product/netflix-premium-4k-uhd/',
        'OnlyFans Accounts': 'https://shopallpremium.com/product/onlyfans-accounts/',
        'ChatGPT Plus': 'https://shopallpremium.com/product/chatgpt-plus/',
        'Spotify Premium': 'https://shopallpremium.com/product/spotify-premium-individual/',
        'Disney+ 1 Year': 'https://shopallpremium.com/product/disney-1-year-no-ads/',
        'Canva PRO': 'https://shopallpremium.com/product/canva-pro/',
        'Amazon Prime Video': 'https://shopallpremium.com/product/amazon-prime-video/',
        'YouTube Premium': 'https://shopallpremium.com/product/youtube-premium-india/',
        'Coursera Plus': 'https://shopallpremium.com/product/coursera-plus/',
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for product_name, url in product_urls.items():
        try:
            print(f"Scraping {product_name}...")
            
            # Scrape the product page
            response = session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract description
            description = ""
            
            # Look for description in the product description tab
            desc_tab = soup.find('div', {'id': 'tab-description'})
            if desc_tab:
                paragraphs = desc_tab.find_all('p')
                if paragraphs:
                    # Get the first meaningful paragraph
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if text and len(text) > 50:  # Meaningful description
                            description = text
                            break
            
            # Fallback to short description
            if not description:
                short_desc = soup.find('div', class_='woocommerce-product-details__short-description')
                if short_desc:
                    description = short_desc.get_text(strip=True)
            
            # Extract features
            features = []
            if desc_tab:
                # Look for bullet points or lists
                lists = desc_tab.find_all(['ul', 'ol'])
                for ul in lists:
                    items = ul.find_all('li')
                    for item in items:
                        feature_text = item.get_text(strip=True)
                        if feature_text and len(feature_text) > 5:
                            features.append(feature_text)
            
            # Default features if none found
            if not features:
                if 'netflix' in product_name.lower():
                    features = [
                        "Stream unlimited movies and TV shows",
                        "4K Ultra HD resolution support",
                        "Multiple device compatibility",
                        "Download content for offline viewing",
                        "No ads, no commitments"
                    ]
                elif 'onlyfans' in product_name.lower():
                    features = [
                        "Premium account with loaded balance",
                        "Subscribe to exclusive content",
                        "Direct messaging with creators",
                        "High-quality photos and videos",
                        "Compatible with all devices"
                    ]
                elif 'chatgpt' in product_name.lower():
                    features = [
                        "Access to GPT-4 model",
                        "Faster response times",
                        "Priority access during peak hours",
                        "Advanced conversation capabilities",
                        "Plugin support"
                    ]
                elif 'spotify' in product_name.lower():
                    features = [
                        "Ad-free music streaming",
                        "Unlimited skips",
                        "Offline download up to 10,000 songs",
                        "High-quality audio",
                        "Access to exclusive content"
                    ]
                else:
                    features = [
                        "Instant delivery within 24 hours",
                        "Premium account with full access",
                        "30-day warranty included",
                        "24/7 customer support",
                        "100% genuine accounts"
                    ]
            
            # Update the product in database
            if description:
                # Find the product in database
                search_results = await db.search_products(product_name.split()[0], 5)
                for product in search_results:
                    if product_name.lower() in product.name.lower():
                        await db.db.products.update_one(
                            {'id': product.id},
                            {'$set': {
                                'description': description,
                                'features': features[:8]
                            }}
                        )
                        print(f"✓ Updated {product.name}")
                        print(f"  Description: {description[:100]}...")
                        print(f"  Features: {len(features)} features")
                        break
            
            time.sleep(1)  # Be respectful
            
        except Exception as e:
            print(f"Error scraping {product_name}: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(scrape_and_update_specific_products())