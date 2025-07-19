#!/usr/bin/env python3
"""
Advanced scraper for shopallpremium.com using multiple scraping methods
"""

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShopAllPremiumScraper:
    def __init__(self):
        self.base_url = "https://shopallpremium.com"
        self.shop_url = "https://shopallpremium.com/shop/"
        self.session = HTMLSession()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def scrape_with_requests_html(self, url):
        """Scrape using requests-html with JavaScript rendering"""
        try:
            logger.info(f"Scraping {url} with requests-html...")
            r = self.session.get(url, timeout=30)
            r.html.render(timeout=20, wait=2)  # Render JavaScript
            return r.html
        except Exception as e:
            logger.error(f"Requests-HTML scraping failed: {e}")
            return None
    
    def scrape_with_beautifulsoup(self, url):
        """Fallback scraping with BeautifulSoup"""
        try:
            logger.info(f"Scraping {url} with BeautifulSoup...")
            response = requests.get(url, headers=self.session.headers, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"BeautifulSoup scraping failed: {e}")
            return None
    
    def extract_product_data(self, html_content):
        """Extract detailed product information"""
        products = []
        
        if hasattr(html_content, 'find'):
            # BeautifulSoup
            product_items = html_content.find_all(['div', 'article'], class_=re.compile(r'product|item'))
        else:
            # requests-html
            product_items = html_content.find('.product, .woocommerce-loop-product__link, article')
        
        logger.info(f"Found {len(product_items) if product_items else 0} potential product containers")
        
        for item in product_items or []:
            try:
                product = self.extract_single_product(item)
                if product and product.get('name'):
                    products.append(product)
                    logger.info(f"Extracted product: {product.get('name', 'Unknown')}")
            except Exception as e:
                logger.warning(f"Failed to extract product: {e}")
                continue
        
        return products
    
    def extract_single_product(self, item):
        """Extract single product details"""
        product = {}
        
        try:
            # Product name
            name_selectors = ['h2', 'h3', '.product-title', '.woocommerce-loop-product__title', 'a[title]']
            for selector in name_selectors:
                if hasattr(item, 'find'):
                    name_elem = item.find(selector)
                    if name_elem:
                        product['name'] = name_elem.get_text(strip=True)
                        break
                else:
                    name_elem = item.find(selector, first=True)
                    if name_elem:
                        product['name'] = name_elem.text.strip()
                        break
            
            # Product link
            link_elem = None
            if hasattr(item, 'find'):
                link_elem = item.find('a')
            else:
                link_elem = item.find('a', first=True)
            
            if link_elem:
                href = link_elem.get('href') if hasattr(link_elem, 'get') else getattr(link_elem, 'attrs', {}).get('href')
                if href:
                    product['link'] = urljoin(self.base_url, href)
            
            # Pricing
            price_patterns = [
                r'\$(\d+(?:\.\d{2})?)',  # $12.99
                r'₹(\d+(?:,\d{3})*)',    # ₹1,299
                r'(\d+(?:\.\d{2})?)\s*USD',  # 12.99 USD
            ]
            
            price_text = item.get_text() if hasattr(item, 'get_text') else item.text
            for pattern in price_patterns:
                matches = re.findall(pattern, price_text)
                if matches:
                    product['prices'] = matches
                    break
            
            # Discount percentage
            discount_match = re.search(r'-(\d+)%', price_text)
            if discount_match:
                product['discount'] = discount_match.group(1) + '%'
            
            # Rating
            rating_match = re.search(r'(\d\.\d+)\s*out\s*of\s*5', price_text)
            if rating_match:
                product['rating'] = rating_match.group(1)
            
            # Category detection
            product_name = product.get('name', '').lower()
            if any(keyword in product_name for keyword in ['netflix', 'disney', 'prime', 'hotstar', 'hbo']):
                product['category'] = 'streaming'
            elif any(keyword in product_name for keyword in ['spotify', 'apple music', 'youtube music']):
                product['category'] = 'music'
            elif any(keyword in product_name for keyword in ['vpn', 'nord', 'express']):
                product['category'] = 'vpn'
            elif any(keyword in product_name for keyword in ['adobe', 'microsoft', 'canva']):
                product['category'] = 'software'
            else:
                product['category'] = 'extras'
            
            # Image URL
            img_elem = None
            if hasattr(item, 'find'):
                img_elem = item.find('img')
            else:
                img_elem = item.find('img', first=True)
            
            if img_elem:
                src = img_elem.get('src') if hasattr(img_elem, 'get') else getattr(img_elem, 'attrs', {}).get('src')
                if src:
                    product['image_url'] = urljoin(self.base_url, src)
            
        except Exception as e:
            logger.warning(f"Error extracting product details: {e}")
        
        return product
    
    def extract_site_structure(self, html_content):
        """Extract navigation and site structure"""
        structure = {
            'categories': [],
            'navigation': [],
            'hero_content': {},
            'trust_elements': [],
            'promotional_content': []
        }
        
        try:
            # Extract navigation
            if hasattr(html_content, 'find_all'):
                nav_items = html_content.find_all('a', href=True)
            else:
                nav_items = html_content.find('a')
            
            for item in nav_items:
                text = item.get_text(strip=True) if hasattr(item, 'get_text') else item.text.strip()
                href = item.get('href') if hasattr(item, 'get') else getattr(item, 'attrs', {}).get('href')
                
                if text and href and len(text) < 50:  # Filter reasonable navigation items
                    structure['navigation'].append({
                        'text': text,
                        'link': urljoin(self.base_url, href)
                    })
            
            # Extract promotional content
            promo_text = html_content.get_text() if hasattr(html_content, 'get_text') else html_content.text
            
            # Look for promotional patterns
            promo_patterns = [
                r'(\d+%\s*off)', 
                r'(save\s*\$\d+)',
                r'(limited\s*time)',
                r'(special\s*offer)',
                r'(use\s*code:?\s*\w+)'
            ]
            
            for pattern in promo_patterns:
                matches = re.findall(pattern, promo_text, re.IGNORECASE)
                structure['promotional_content'].extend(matches)
            
        except Exception as e:
            logger.warning(f"Error extracting site structure: {e}")
        
        return structure
    
    def scrape_shop_page(self):
        """Main scraping function"""
        logger.info("Starting comprehensive shop page scraping...")
        
        results = {
            'products': [],
            'site_structure': {},
            'scraping_info': {
                'timestamp': time.time(),
                'methods_used': [],
                'success': False
            }
        }
        
        # Try requests-html first
        html_content = self.scrape_with_requests_html(self.shop_url)
        if html_content:
            results['scraping_info']['methods_used'].append('requests-html')
            try:
                products = self.extract_product_data(html_content)
                results['products'].extend(products)
                results['site_structure'] = self.extract_site_structure(html_content)
                results['scraping_info']['success'] = True
            except Exception as e:
                logger.error(f"Failed to extract data with requests-html: {e}")
        
        # Fallback to BeautifulSoup if needed
        if not results['products']:
            logger.info("Falling back to BeautifulSoup...")
            soup = self.scrape_with_beautifulsoup(self.shop_url)
            if soup:
                results['scraping_info']['methods_used'].append('beautifulsoup')
                try:
                    products = self.extract_product_data(soup)
                    results['products'].extend(products)
                    if not results['site_structure']:
                        results['site_structure'] = self.extract_site_structure(soup)
                    results['scraping_info']['success'] = True
                except Exception as e:
                    logger.error(f"Failed to extract data with BeautifulSoup: {e}")
        
        # Additional homepage scraping
        try:
            logger.info("Scraping homepage for additional data...")
            home_soup = self.scrape_with_beautifulsoup(self.base_url)
            if home_soup:
                home_structure = self.extract_site_structure(home_soup)
                # Merge with existing structure
                for key in home_structure:
                    if key in results['site_structure']:
                        if isinstance(results['site_structure'][key], list):
                            results['site_structure'][key].extend(home_structure[key])
                    else:
                        results['site_structure'][key] = home_structure[key]
        except Exception as e:
            logger.warning(f"Failed to scrape homepage: {e}")
        
        logger.info(f"Scraping completed. Found {len(results['products'])} products.")
        return results
    
    def save_results(self, results, filename='scraped_data.json'):
        """Save results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

def main():
    scraper = ShopAllPremiumScraper()
    results = scraper.scrape_shop_page()
    
    # Print summary
    print(f"\n=== SCRAPING RESULTS ===")
    print(f"Success: {results['scraping_info']['success']}")
    print(f"Methods used: {', '.join(results['scraping_info']['methods_used'])}")
    print(f"Products found: {len(results['products'])}")
    print(f"Navigation items: {len(results['site_structure'].get('navigation', []))}")
    print(f"Promotional content: {len(results['site_structure'].get('promotional_content', []))}")
    
    if results['products']:
        print(f"\nSample products:")
        for i, product in enumerate(results['products'][:5]):
            print(f"{i+1}. {product.get('name', 'Unknown')} - {product.get('category', 'uncategorized')}")
    
    # Save results
    scraper.save_results(results)
    
    return results

if __name__ == "__main__":
    main()