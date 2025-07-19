#!/usr/bin/env python3
"""
Enhanced scraper specifically for shopallpremium.com with multiple approaches
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_with_selenium():
    """Scrape using Selenium for JavaScript-heavy content"""
    logger.info("Starting Selenium scraper...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://shopallpremium.com/shop/")
        
        # Wait for page to load
        time.sleep(5)
        
        # Try to find products
        products = []
        
        # Common WooCommerce selectors
        product_selectors = [
            ".woocommerce-loop-product",
            ".product",
            ".shop-item",
            ".product-item",
            ".wc-block-grid__product",
            "[data-product-id]"
        ]
        
        for selector in product_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                logger.info(f"Found {len(elements)} elements with selector: {selector}")
                
                for element in elements:
                    product = extract_product_selenium(element)
                    if product:
                        products.append(product)
                        
                if elements:  # If we found elements, break
                    break
                    
            except Exception as e:
                logger.warning(f"Error with selector {selector}: {e}")
                continue
        
        # Get page source for additional analysis
        page_source = driver.page_source
        
        driver.quit()
        
        return products, page_source
        
    except Exception as e:
        logger.error(f"Selenium scraping failed: {e}")
        return [], ""

def extract_product_selenium(element):
    """Extract product info from Selenium WebElement"""
    try:
        product = {}
        
        # Product name
        try:
            name_elem = element.find_element(By.CSS_SELECTOR, "h2, h3, .woocommerce-loop-product__title, .product-title")
            product['name'] = name_elem.text.strip()
        except:
            pass
        
        # Price
        try:
            price_elem = element.find_element(By.CSS_SELECTOR, ".price, .woocommerce-Price-amount")
            product['price'] = price_elem.text.strip()
        except:
            pass
        
        # Link
        try:
            link_elem = element.find_element(By.CSS_SELECTOR, "a")
            product['link'] = link_elem.get_attribute('href')
        except:
            pass
        
        # Image
        try:
            img_elem = element.find_element(By.CSS_SELECTOR, "img")
            product['image'] = img_elem.get_attribute('src')
        except:
            pass
        
        return product if product.get('name') else None
        
    except Exception as e:
        logger.warning(f"Error extracting product: {e}")
        return None

def scrape_with_requests():
    """Enhanced requests scraping with better error handling"""
    logger.info("Starting enhanced requests scraper...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    urls_to_try = [
        "https://shopallpremium.com/shop/",
        "https://shopallpremium.com/",
        "https://shopallpremium.com/products/",
        "https://shopallpremium.com/wc-api/",
    ]
    
    results = {}
    
    for url in urls_to_try:
        try:
            logger.info(f"Trying URL: {url}")
            response = session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Analyze page structure
            analysis = analyze_page_structure(soup, url)
            results[url] = analysis
            
            logger.info(f"Successfully scraped {url}: {len(analysis.get('potential_products', []))} potential products found")
            
        except Exception as e:
            logger.warning(f"Failed to scrape {url}: {e}")
            results[url] = {"error": str(e)}
    
    return results

def analyze_page_structure(soup, url):
    """Deep analysis of page structure to find products"""
    analysis = {
        'url': url,
        'title': soup.title.text if soup.title else "No title",
        'potential_products': [],
        'navigation_links': [],
        'promotional_content': [],
        'form_data': {},
        'script_content': []
    }
    
    # Extract all text content
    page_text = soup.get_text()
    
    # Look for product-like patterns
    product_patterns = [
        r'(netflix|spotify|disney|prime|adobe|vpn|subscription)',
        r'\$(\d+(?:\.\d{2})?)',
        r'₹(\d+(?:,\d{3})*)',
        r'(\d+%\s*off)',
        r'(buy\s+now|add\s+to\s+cart|purchase)',
    ]
    
    for pattern in product_patterns:
        matches = re.findall(pattern, page_text, re.IGNORECASE)
        if matches:
            analysis['potential_products'].extend([match if isinstance(match, str) else match[0] for match in matches])
    
    # Extract navigation links
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text(strip=True)
        if text and len(text) < 100 and href:
            analysis['navigation_links'].append({
                'text': text,
                'href': href
            })
    
    # Look for promotional content
    promo_keywords = ['sale', 'offer', 'discount', 'special', 'deal', 'limited', 'exclusive']
    for keyword in promo_keywords:
        if keyword in page_text.lower():
            # Extract surrounding text
            pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
            matches = re.findall(pattern, page_text, re.IGNORECASE)
            analysis['promotional_content'].extend(matches)
    
    # Extract form data
    forms = soup.find_all('form')
    for i, form in enumerate(forms):
        inputs = form.find_all(['input', 'select', 'textarea'])
        form_data = {}
        for inp in inputs:
            name = inp.get('name')
            if name:
                form_data[name] = {
                    'type': inp.get('type', inp.name),
                    'value': inp.get('value', ''),
                    'placeholder': inp.get('placeholder', ''),
                }
        if form_data:
            analysis['form_data'][f'form_{i}'] = form_data
    
    # Extract JavaScript content
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string:
            # Look for interesting patterns in JavaScript
            if any(keyword in script.string.lower() for keyword in ['product', 'price', 'cart', 'woocommerce']):
                analysis['script_content'].append(script.string[:500] + "..." if len(script.string) > 500 else script.string)
    
    return analysis

def create_sample_products():
    """Create sample products based on shopallpremium.com's known structure"""
    logger.info("Creating sample products based on known structure...")
    
    sample_products = [
        {
            "name": "Netflix Premium 4K UHD (1 Month)",
            "category": "streaming",
            "original_price": 649,
            "discounted_price": 199,
            "description": "Netflix Premium subscription with 4K streaming, multiple screens, and offline downloads.",
            "features": ["4K Ultra HD", "Watch on 4 screens", "Download & watch offline", "No ads"],
            "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=400&h=300&fit=crop",
            "stock_quantity": 100,
            "discount_percentage": 69
        },
        {
            "name": "Spotify Premium Individual (3 Months)",
            "category": "music",
            "original_price": 399,
            "discounted_price": 299,
            "description": "Ad-free music streaming with offline downloads and unlimited skips.",
            "features": ["Ad-free music", "Offline listening", "Unlimited skips", "High quality audio"],
            "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop",
            "stock_quantity": 100,
            "discount_percentage": 25
        },
        {
            "name": "Disney+ Hotstar Super (1 Year)",
            "category": "streaming", 
            "original_price": 1499,
            "discounted_price": 799,
            "description": "Complete entertainment with Disney+ content, live sports, and Indian shows.",
            "features": ["Disney+ Originals", "Live Sports", "Indian Content", "Multiple devices"],
            "image_url": "https://images.unsplash.com/photo-1489599314773-1b98e69cced3?w=400&h=300&fit=crop",
            "stock_quantity": 100,
            "discount_percentage": 47
        },
        {
            "name": "Amazon Prime Video (1 Year)",
            "category": "streaming",
            "original_price": 1499,
            "discounted_price": 899,
            "description": "Prime Video subscription with exclusive shows, movies, and faster delivery.",
            "features": ["Prime Originals", "Free delivery", "Prime Music", "Exclusive deals"],
            "image_url": "https://images.unsplash.com/photo-1560472355-536de3962603?w=400&h=300&fit=crop",
            "stock_quantity": 100,
            "discount_percentage": 40
        },
        {
            "name": "NordVPN 2-Year Plan",
            "category": "vpn",
            "original_price": 11600,
            "discounted_price": 6999,
            "description": "Secure VPN with 5400+ servers worldwide and advanced security features.",
            "features": ["5400+ servers", "No-logs policy", "Kill switch", "6 devices"],
            "image_url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400&h=300&fit=crop",
            "stock_quantity": 100,
            "discount_percentage": 40
        },
        {
            "name": "Adobe Creative Cloud (1 Year)",
            "category": "software",
            "original_price": 52999,
            "discounted_price": 24999,
            "description": "Complete Adobe Creative Suite including Photoshop, Illustrator, Premiere Pro.",
            "features": ["20+ apps", "100GB cloud storage", "Premium fonts", "Regular updates"],
            "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400&h=300&fit=crop",
            "stock_quantity": 50,
            "discount_percentage": 53
        }
    ]
    
    return sample_products

def main():
    results = {
        'scraping_timestamp': time.time(),
        'selenium_results': [],
        'requests_results': {},
        'sample_products': []
    }
    
    # Try Selenium scraping
    try:
        products, page_source = scrape_with_selenium()
        results['selenium_results'] = products
        logger.info(f"Selenium found {len(products)} products")
    except Exception as e:
        logger.error(f"Selenium scraping completely failed: {e}")
    
    # Try requests scraping
    try:
        requests_results = scrape_with_requests()
        results['requests_results'] = requests_results
    except Exception as e:
        logger.error(f"Requests scraping failed: {e}")
    
    # Create sample products based on knowledge
    results['sample_products'] = create_sample_products()
    
    # Save results
    with open('/app/backend/scraped_data.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print("\n=== ENHANCED SCRAPING RESULTS ===")
    print(f"Selenium products: {len(results['selenium_results'])}")
    print(f"Requests analysis: {len(results['requests_results'])} URLs analyzed")
    print(f"Sample products created: {len(results['sample_products'])}")
    
    # Show analysis summary
    for url, analysis in results['requests_results'].items():
        if 'error' not in analysis:
            print(f"\n{url}:")
            print(f"  - Title: {analysis['title']}")
            print(f"  - Potential products: {len(analysis['potential_products'])}")
            print(f"  - Navigation links: {len(analysis['navigation_links'])}")
            print(f"  - Promotional content: {len(analysis['promotional_content'])}")
    
    return results

if __name__ == "__main__":
    main()