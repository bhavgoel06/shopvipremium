import requests
from bs4 import BeautifulSoup
import asyncio
from database import db
from models import SearchFilters
import time
import re

async def scrape_all_product_details():
    """Scrape detailed descriptions and features for ALL products from shopallpremium.com"""
    
    # First, get the product URLs from the main site
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    # Get all product URLs from shopallpremium.com
    product_urls = []
    pages_to_scrape = [
        'https://shopallpremium.com/',
        'https://shopallpremium.com/shop/',
        'https://shopallpremium.com/shop/page/2/',
        'https://shopallpremium.com/shop/page/3/',
        'https://shopallpremium.com/popular/',
    ]
    
    for page_url in pages_to_scrape:
        try:
            print(f"Getting product URLs from: {page_url}")
            response = session.get(page_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if '/product/' in href:
                    if href.startswith('http'):
                        product_urls.append(href)
                    else:
                        product_urls.append(f"https://shopallpremium.com{href}")
            
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping {page_url}: {e}")
    
    # Remove duplicates
    product_urls = list(set(product_urls))
    print(f"Found {len(product_urls)} unique product URLs")
    
    # Now scrape each product page for detailed info
    scraped_products = {}
    
    for i, url in enumerate(product_urls):
        try:
            print(f"Scraping {i+1}/{len(product_urls)}: {url}")
            
            response = session.get(url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1', class_='product_title') or soup.find('h1')
            if not name_elem:
                continue
                
            product_name = name_elem.get_text(strip=True)
            
            # Extract description from the Description tab
            description = ""
            desc_tab = soup.find('div', {'id': 'tab-description'})
            if desc_tab:
                # Get paragraphs and clean them
                paragraphs = desc_tab.find_all(['p', 'div'])
                desc_parts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:  # Only meaningful text
                        # Clean up the text
                        text = re.sub(r'\s+', ' ', text)
                        text = re.sub(r'[^\w\s\.,!?()-]', '', text)
                        desc_parts.append(text)
                
                if desc_parts:
                    description = ' '.join(desc_parts[:2])  # First 2 paragraphs
            
            # Extract features from lists
            features = []
            if desc_tab:
                # Look for bullet points or lists
                lists = desc_tab.find_all(['ul', 'ol'])
                for ul in lists:
                    items = ul.find_all('li')
                    for item in items:
                        feature_text = item.get_text(strip=True)
                        if feature_text and len(feature_text) > 5 and len(feature_text) < 100:
                            # Clean the feature text
                            feature_text = re.sub(r'\s+', ' ', feature_text)
                            feature_text = re.sub(r'[^\w\s\.,!?()-]', '', feature_text)
                            features.append(feature_text)
            
            # If no description found, try short description
            if not description:
                short_desc = soup.find('div', class_='woocommerce-product-details__short-description')
                if short_desc:
                    description = short_desc.get_text(strip=True)
            
            # If still no description, create a basic one
            if not description:
                description = f"Get premium access to {product_name} with full features and instant delivery."
            
            # If no features found, create basic ones
            if not features:
                features = [
                    "Instant delivery within 24 hours",
                    "Premium account with full access",
                    "30-day warranty included",
                    "24/7 customer support",
                    "100% genuine accounts"
                ]
            
            scraped_products[product_name] = {
                'name': product_name,
                'description': description,
                'features': features[:8]  # Limit to 8 features
            }
            
            print(f"  ✓ Scraped: {product_name}")
            print(f"    Description: {description[:80]}...")
            print(f"    Features: {len(features)} features")
            
            time.sleep(1)  # Be respectful
            
        except Exception as e:
            print(f"  ✗ Error scraping {url}: {e}")
            continue
    
    print(f"\nTotal scraped products: {len(scraped_products)}")
    
    # Now update our database products with scraped info
    our_products = await db.get_products(SearchFilters(page=1, per_page=200))
    updated_count = 0
    
    for product in our_products:
        try:
            # Try to find matching scraped product
            matching_scraped = None
            
            # Direct match first
            if product.name in scraped_products:
                matching_scraped = scraped_products[product.name]
            else:
                # Try partial matches
                for scraped_name, scraped_data in scraped_products.items():
                    if (product.name.lower() in scraped_name.lower() or 
                        scraped_name.lower() in product.name.lower()):
                        matching_scraped = scraped_data
                        break
            
            if matching_scraped:
                # Update the product
                await db.db.products.update_one(
                    {'id': product.id},
                    {'$set': {
                        'description': matching_scraped['description'],
                        'features': matching_scraped['features']
                    }}
                )
                updated_count += 1
                print(f"✓ Updated {updated_count}: {product.name}")
            else:
                print(f"✗ No match found for: {product.name}")
                
        except Exception as e:
            print(f"✗ Error updating {product.name}: {e}")
    
    print(f"\n🎉 Successfully updated {updated_count} products with scraped descriptions and features!")

if __name__ == "__main__":
    asyncio.run(scrape_all_product_details())