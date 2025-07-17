#!/usr/bin/env python3
"""
Test scraper for a few specific products from shopallpremium.com
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def scrape_product_page(url):
    """Scrape a single product page"""
    print(f"🔍 Scraping: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract product name
        title = soup.find('h1')
        product_name = title.get_text(strip=True) if title else "Unknown"
        
        # Extract description
        description = ""
        content_div = soup.find('div', class_='entry-content') or soup.find('div', class_='product-description')
        if content_div:
            # Get all text content
            description = content_div.get_text(strip=True)
        
        # Extract features (look for bullet points)
        features = []
        for li in soup.find_all('li'):
            text = li.get_text(strip=True)
            if text and len(text) > 10 and len(text) < 200:
                features.append(text)
        
        # Extract variants from description
        variants = []
        if description:
            # Look for common variant patterns
            patterns = [
                r'(\d+\s*(?:Screen|Screens?))',
                r'(\$\d+\s*Balance)',
                r'(\d+\s*(?:Month|Year|Day)s?)',
                r'(Basic|Standard|Premium|Pro|Individual|Family|Team|Enterprise)',
                r'VALIDITY[:\s]*([^,\n]+)',
                r'Duration[:\s]*([^,\n]+)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, description, re.IGNORECASE)
                for match in matches:
                    variant = match.strip()
                    if variant and variant not in variants:
                        variants.append(variant)
        
        # Extract pricing
        prices = []
        price_elements = soup.find_all(string=re.compile(r'[₹$]\d+'))
        for price_str in price_elements:
            price_match = re.search(r'[\d,]+', price_str.replace('₹', '').replace('$', ''))
            if price_match:
                try:
                    price_val = int(price_match.group().replace(',', ''))
                    if price_val > 0:  # Only add positive prices
                        prices.append(price_val)
                except ValueError:
                    continue
        
        return {
            'name': product_name,
            'description': description,
            'features': features[:10],
            'variants': variants[:6],
            'prices': prices,
            'url': url
        }
        
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

def main():
    """Test with a few key products"""
    
    # Test URLs
    test_urls = [
        "https://shopallpremium.com/product/onlyfans-accounts/",
        "https://shopallpremium.com/product/netflix-1-screen/",
        "https://shopallpremium.com/product/spotify-premium/",
        "https://shopallpremium.com/product/leetcode-premium/",
        "https://shopallpremium.com/product/coursera-plus/"
    ]
    
    results = []
    
    for url in test_urls:
        result = scrape_product_page(url)
        if result:
            results.append(result)
            print(f"✅ Scraped: {result['name']}")
            print(f"   Description length: {len(result['description'])} chars")
            print(f"   Features: {len(result['features'])}")
            print(f"   Variants: {result['variants']}")
            print(f"   Prices: {result['prices']}")
            print("-" * 50)
    
    # Save results
    with open('/app/backend/test_scraped_products.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Test scraping completed. Scraped {len(results)} products.")

if __name__ == "__main__":
    main()