#!/usr/bin/env python3
"""
Comprehensive scraper for shopallpremium.com
Scrapes all product information including descriptions, features, variants, and pricing
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from typing import Dict, List, Optional

class ShopAllPremiumScraper:
    def __init__(self):
        self.base_url = "https://shopallpremium.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.products = []
        
    def scrape_product_listing(self) -> List[Dict]:
        """Scrape the main shop page to get all product links"""
        print("🔍 Scraping product listing from shop page...")
        
        try:
            response = self.session.get(f"{self.base_url}/shop/")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product links
            product_links = []
            
            # Look for product cards/links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and '/product/' in href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in product_links:
                        product_links.append(full_url)
            
            print(f"✅ Found {len(product_links)} product links")
            return product_links
            
        except Exception as e:
            print(f"❌ Error scraping product listing: {e}")
            return []
    
    def extract_product_details(self, product_url: str) -> Optional[Dict]:
        """Extract detailed product information from individual product page"""
        print(f"📄 Scraping product: {product_url}")
        
        try:
            response = self.session.get(product_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product information
            product_data = {
                'url': product_url,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Product title
            title_selectors = [
                'h1.product-title',
                'h1.entry-title', 
                'h1.woocommerce-product-title',
                'h1',
                '.product-title',
                '.entry-title'
            ]
            
            title = None
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            if title:
                product_data['name'] = title
            
            # Price information
            price_selectors = [
                '.price .woocommerce-Price-amount',
                '.price-current',
                '.price',
                '.product-price',
                '.woocommerce-Price-amount'
            ]
            
            prices = []
            for selector in price_selectors:
                price_elems = soup.select(selector)
                for elem in price_elems:
                    price_text = elem.get_text(strip=True)
                    # Extract numbers from price text
                    price_match = re.search(r'[\d,]+', price_text.replace('₹', '').replace('$', ''))
                    if price_match:
                        prices.append(int(price_match.group().replace(',', '')))
            
            if prices:
                product_data['prices'] = prices
                product_data['original_price'] = max(prices) if len(prices) > 1 else prices[0]
                product_data['discounted_price'] = min(prices) if len(prices) > 1 else prices[0]
            
            # Product description
            desc_selectors = [
                '.product-description',
                '.product-content',
                '.entry-content',
                '.woocommerce-product-details__short-description',
                '.product-details'
            ]
            
            description = None
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    break
            
            if description:
                product_data['description'] = description
            
            # Product features (extract from description or separate section)
            features = []
            
            # Look for bullet points or lists
            feature_lists = soup.select('ul li, ol li')
            for li in feature_lists:
                feature_text = li.get_text(strip=True)
                if feature_text and len(feature_text) > 5 and len(feature_text) < 200:
                    features.append(feature_text)
            
            # Look for features in description text
            if description:
                # Extract lines starting with bullet points or dashes
                lines = description.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('•') or line.startswith('-') or line.startswith('★'):
                        feature_text = line.lstrip('•-★ ').strip()
                        if feature_text and len(feature_text) > 5:
                            features.append(feature_text)
            
            if features:
                product_data['features'] = features[:10]  # Limit to 10 features
            
            # Product variants (duration options, plans, etc.)
            variants = []
            
            # Look for variation selectors
            variant_selectors = [
                '.variations select option',
                '.product-variations option',
                '.duration-options option',
                '.variation-selector option'
            ]
            
            for selector in variant_selectors:
                options = soup.select(selector)
                for option in options:
                    variant_text = option.get_text(strip=True)
                    if variant_text and variant_text.lower() not in ['choose an option', 'select', '']:
                        variants.append(variant_text)
            
            # Look for variants in description text
            if description:
                # Common variant patterns
                variant_patterns = [
                    r'VALIDITY[:\s]*([^,\n]+)',
                    r'Duration[:\s]*([^,\n]+)',
                    r'Plan[:\s]*([^,\n]+)',
                    r'(\d+\s*(?:Month|Year|Day)s?)',
                    r'(\$\d+\s*Balance)',
                    r'(\d+\s*Screen)',
                    r'(Basic|Standard|Premium|Pro|Individual|Family|Team|Enterprise)',
                ]
                
                for pattern in variant_patterns:
                    matches = re.findall(pattern, description, re.IGNORECASE)
                    for match in matches:
                        variant_text = match.strip()
                        if variant_text and variant_text not in variants:
                            variants.append(variant_text)
            
            if variants:
                product_data['duration_options'] = variants[:6]  # Limit to 6 variants
            
            # Category (extract from URL or breadcrumbs)
            category = None
            
            # Try to extract from URL
            url_parts = product_url.split('/')
            if 'product' in url_parts:
                # Category might be in the URL structure
                for i, part in enumerate(url_parts):
                    if part == 'product' and i > 0:
                        category = url_parts[i-1]
                        break
            
            # Try to extract from breadcrumbs
            breadcrumb_selectors = [
                '.breadcrumb a',
                '.breadcrumbs a',
                '.woocommerce-breadcrumb a'
            ]
            
            for selector in breadcrumb_selectors:
                breadcrumb_links = soup.select(selector)
                for link in breadcrumb_links:
                    link_text = link.get_text(strip=True).lower()
                    if link_text in ['ott', 'software', 'vpn', 'education', 'gaming', 'adult', 'membership']:
                        category = link_text
                        break
            
            if category:
                product_data['category'] = category
            
            # Extract short description
            short_desc_selectors = [
                '.short-description',
                '.product-summary',
                '.woocommerce-product-details__short-description'
            ]
            
            short_description = None
            for selector in short_desc_selectors:
                short_desc_elem = soup.select_one(selector)
                if short_desc_elem:
                    short_description = short_desc_elem.get_text(strip=True)
                    break
            
            if short_description:
                product_data['short_description'] = short_description
            elif description:
                # Create short description from first sentence of description
                sentences = description.split('.')
                if sentences:
                    product_data['short_description'] = sentences[0].strip() + '.'
            
            return product_data
            
        except Exception as e:
            print(f"❌ Error scraping product {product_url}: {e}")
            return None
    
    def scrape_all_products(self) -> List[Dict]:
        """Scrape all products from the site"""
        print("🚀 Starting comprehensive product scraping...")
        
        # Get all product links
        product_links = self.scrape_product_listing()
        
        if not product_links:
            print("❌ No product links found")
            return []
        
        # Scrape each product
        for i, product_url in enumerate(product_links, 1):
            print(f"📋 Processing product {i}/{len(product_links)}")
            
            product_data = self.extract_product_details(product_url)
            if product_data:
                self.products.append(product_data)
            
            # Add delay to avoid overwhelming the server
            time.sleep(2)
        
        print(f"✅ Scraped {len(self.products)} products successfully")
        return self.products
    
    def save_to_json(self, filename: str = "shopallpremium_scraped_products.json"):
        """Save scraped products to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved {len(self.products)} products to {filename}")

class DatabaseUpdater:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
        self.db = self.client[os.environ.get('DB_NAME', 'premium_shop')]
    
    async def update_products_from_scraped_data(self, scraped_products: List[Dict]):
        """Update database products with scraped data"""
        print("🔄 Updating database with scraped product data...")
        
        updated_count = 0
        total_products = len(scraped_products)
        
        for scraped_product in scraped_products:
            try:
                product_name = scraped_product.get('name')
                if not product_name:
                    continue
                
                # Find matching product in database
                db_product = await self.db.products.find_one({
                    "name": {"$regex": f"^{re.escape(product_name)}$", "$options": "i"}
                })
                
                if not db_product:
                    # Try partial match
                    db_product = await self.db.products.find_one({
                        "name": {"$regex": re.escape(product_name.split()[0]), "$options": "i"}
                    })
                
                if db_product:
                    # Prepare update data
                    update_data = {
                        "updated_at": datetime.utcnow()
                    }
                    
                    # Update description if available
                    if scraped_product.get('description'):
                        update_data['description'] = scraped_product['description']
                    
                    # Update short description if available
                    if scraped_product.get('short_description'):
                        update_data['short_description'] = scraped_product['short_description']
                    
                    # Update features if available
                    if scraped_product.get('features'):
                        update_data['features'] = scraped_product['features']
                    
                    # Update variants if available
                    if scraped_product.get('duration_options'):
                        update_data['duration_options'] = scraped_product['duration_options']
                    
                    # Update pricing if available
                    if scraped_product.get('original_price'):
                        update_data['original_price'] = scraped_product['original_price']
                    
                    if scraped_product.get('discounted_price'):
                        update_data['discounted_price'] = scraped_product['discounted_price']
                    
                    # Update category if available
                    if scraped_product.get('category'):
                        update_data['category'] = scraped_product['category']
                    
                    # Update the product
                    result = await self.db.products.update_one(
                        {"id": db_product["id"]},
                        {"$set": update_data}
                    )
                    
                    if result.modified_count > 0:
                        updated_count += 1
                        print(f"✅ Updated: {product_name}")
                    
                else:
                    print(f"⚠️  Product not found in database: {product_name}")
                    
            except Exception as e:
                print(f"❌ Error updating product {scraped_product.get('name', 'Unknown')}: {e}")
        
        print(f"\n📊 Database update summary:")
        print(f"   - Scraped products: {total_products}")
        print(f"   - Successfully updated: {updated_count}")
        print(f"   - Update rate: {(updated_count/total_products)*100:.1f}%")
        
        self.client.close()
        return updated_count

async def main():
    """Main function to run the comprehensive scraping and updating"""
    
    print("🏪 SHOPALLPREMIUM.COM COMPREHENSIVE SCRAPER")
    print("=" * 60)
    
    # Initialize scraper
    scraper = ShopAllPremiumScraper()
    
    # Scrape all products
    scraped_products = scraper.scrape_all_products()
    
    if not scraped_products:
        print("❌ No products scraped. Exiting.")
        return
    
    # Save to JSON file
    scraper.save_to_json()
    
    # Update database
    updater = DatabaseUpdater()
    updated_count = await updater.update_products_from_scraped_data(scraped_products)
    
    print("\n" + "=" * 60)
    print("✅ COMPREHENSIVE SCRAPING COMPLETED!")
    print(f"📊 Results: {len(scraped_products)} products scraped, {updated_count} database updates")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())