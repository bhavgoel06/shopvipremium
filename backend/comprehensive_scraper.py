import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin, urlparse
import sys
import os

class ShopAllPremiumScraper:
    def __init__(self):
        self.base_url = "https://shopallpremium.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.products = []
        self.scraped_urls = set()
        
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text.strip())
    
    def extract_price(self, price_text):
        """Extract price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract number
        price_match = re.search(r'₹?(\d+(?:,\d+)*(?:\.\d+)?)', price_text.replace(',', ''))
        if price_match:
            return float(price_match.group(1))
        return None
    
    def scrape_product_page(self, product_url):
        """Scrape individual product page for detailed information"""
        try:
            print(f"Scraping product: {product_url}")
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product details
            product_data = {
                'name': '',
                'original_price': None,
                'discounted_price': None,
                'discount_percentage': 0,
                'short_description': '',
                'description': '',
                'features': [],
                'variants': [],
                'image_url': '',
                'gallery_images': [],
                'rating': 0.0,
                'total_reviews': 0,
                'category': '',
                'is_featured': False,
                'is_bestseller': False,
                'stock_quantity': 100,
                'status': 'active',
                'seo_keywords': []
            }
            
            # Product name
            name_elem = soup.find('h1', class_='product_title') or soup.find('h1')
            if name_elem:
                product_data['name'] = self.clean_text(name_elem.text)
            
            # Price extraction
            price_elem = soup.find('p', class_='price') or soup.find('span', class_='price')
            if price_elem:
                # Look for original and sale price
                original_price_elem = price_elem.find('del') or price_elem.find('span', class_='original-price')
                sale_price_elem = price_elem.find('ins') or price_elem.find('span', class_='sale-price')
                
                if original_price_elem and sale_price_elem:
                    product_data['original_price'] = self.extract_price(original_price_elem.text)
                    product_data['discounted_price'] = self.extract_price(sale_price_elem.text)
                else:
                    # Single price
                    single_price = self.extract_price(price_elem.text)
                    product_data['discounted_price'] = single_price
                    product_data['original_price'] = single_price * 1.5  # Assume 33% discount
            
            # Calculate discount percentage
            if product_data['original_price'] and product_data['discounted_price']:
                discount = ((product_data['original_price'] - product_data['discounted_price']) / product_data['original_price']) * 100
                product_data['discount_percentage'] = int(discount)
            
            # Product description
            desc_elem = soup.find('div', class_='woocommerce-product-details__short-description') or soup.find('div', class_='summary')
            if desc_elem:
                product_data['short_description'] = self.clean_text(desc_elem.text)
            
            # Full description
            full_desc_elem = soup.find('div', {'id': 'tab-description'}) or soup.find('div', class_='woocommerce-tabs')
            if full_desc_elem:
                product_data['description'] = self.clean_text(full_desc_elem.text)
            
            # Features
            features_list = soup.find_all('li') or soup.find_all('p')
            for feature in features_list:
                feature_text = self.clean_text(feature.text)
                if feature_text and len(feature_text) > 10 and len(feature_text) < 200:
                    product_data['features'].append(feature_text)
            
            # Variants (from select options)
            variant_select = soup.find('select', {'name': 'attribute_pa_plan'}) or soup.find('select')
            if variant_select:
                options = variant_select.find_all('option')
                for option in options:
                    if option.get('value') and option.text.strip():
                        product_data['variants'].append({
                            'name': self.clean_text(option.text),
                            'value': option.get('value')
                        })
            
            # Main image
            img_elem = soup.find('img', class_='wp-post-image') or soup.find('img')
            if img_elem and img_elem.get('src'):
                product_data['image_url'] = urljoin(self.base_url, img_elem.get('src'))
            
            # Gallery images
            gallery_imgs = soup.find_all('img', class_='gallery-image') or soup.find_all('img')
            for img in gallery_imgs[:5]:  # Limit to 5 images
                if img.get('src'):
                    img_url = urljoin(self.base_url, img.get('src'))
                    if img_url not in product_data['gallery_images']:
                        product_data['gallery_images'].append(img_url)
            
            # Rating
            rating_elem = soup.find('div', class_='star-rating') or soup.find('span', class_='rating')
            if rating_elem:
                rating_text = rating_elem.get('title', '') or rating_elem.text
                rating_match = re.search(r'(\d+(?:\.\d+)?)', rating_text)
                if rating_match:
                    product_data['rating'] = float(rating_match.group(1))
            
            # Reviews count
            reviews_elem = soup.find('a', class_='woocommerce-review-link') or soup.find('span', class_='count')
            if reviews_elem:
                reviews_text = reviews_elem.text
                reviews_match = re.search(r'(\d+)', reviews_text)
                if reviews_match:
                    product_data['total_reviews'] = int(reviews_match.group(1))
            
            # Category detection
            category_elem = soup.find('nav', class_='woocommerce-breadcrumb') or soup.find('span', class_='posted_in')
            if category_elem:
                category_text = category_elem.text.lower()
                if 'netflix' in category_text or 'prime' in category_text or 'disney' in category_text:
                    product_data['category'] = 'ott'
                elif 'spotify' in category_text or 'music' in category_text:
                    product_data['category'] = 'ott'
                elif 'vpn' in category_text:
                    product_data['category'] = 'vpn'
                elif 'adobe' in category_text or 'canva' in category_text:
                    product_data['category'] = 'software'
                elif 'adult' in category_text or 'premium' in category_text:
                    product_data['category'] = 'adult'
                else:
                    product_data['category'] = 'ott'
            
            # Check for bestseller/featured
            if soup.find('span', class_='onsale') or 'best seller' in soup.text.lower():
                product_data['is_bestseller'] = True
            
            # SEO keywords
            keywords = [word.lower() for word in product_data['name'].split() if len(word) > 2]
            product_data['seo_keywords'] = keywords
            
            return product_data
            
        except Exception as e:
            print(f"Error scraping product {product_url}: {e}")
            return None
    
    def scrape_product_list(self, url):
        """Scrape product list page"""
        try:
            print(f"Scraping product list: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product links
            product_links = []
            
            # Different possible selectors for product links
            selectors = [
                'a[href*="/product/"]',
                '.product-item a',
                '.product a',
                'h2.woocommerce-loop-product__title a',
                '.products li a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href and '/product/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in self.scraped_urls:
                            product_links.append(full_url)
                            self.scraped_urls.add(full_url)
            
            return product_links
            
        except Exception as e:
            print(f"Error scraping product list {url}: {e}")
            return []
    
    def scrape_all_products(self):
        """Main scraping function"""
        print("Starting to scrape all products from shopallpremium.com...")
        
        # URLs to scrape
        urls_to_scrape = [
            f"{self.base_url}/",
            f"{self.base_url}/shop/",
            f"{self.base_url}/shop/page/2/",
            f"{self.base_url}/shop/page/3/",
            f"{self.base_url}/shop/page/4/",
            f"{self.base_url}/shop/page/5/",
        ]
        
        # Collect all product URLs
        all_product_urls = set()
        
        for url in urls_to_scrape:
            product_urls = self.scrape_product_list(url)
            all_product_urls.update(product_urls)
            time.sleep(1)  # Be respectful
        
        print(f"Found {len(all_product_urls)} product URLs")
        
        # Scrape each product
        for i, product_url in enumerate(all_product_urls):
            print(f"Processing product {i+1}/{len(all_product_urls)}")
            product_data = self.scrape_product_page(product_url)
            
            if product_data and product_data['name']:
                self.products.append(product_data)
                print(f"✓ Scraped: {product_data['name']}")
            
            time.sleep(1)  # Be respectful to the server
        
        print(f"\nScraping completed! Found {len(self.products)} products.")
        
        # Save to JSON file
        with open('shopallpremium_products.json', 'w', encoding='utf-8') as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)
        
        print("Products saved to shopallpremium_products.json")
        
        return self.products

if __name__ == "__main__":
    scraper = ShopAllPremiumScraper()
    products = scraper.scrape_all_products()
    
    print(f"\nScraping Summary:")
    print(f"Total products scraped: {len(products)}")
    
    # Show sample products
    for i, product in enumerate(products[:5]):
        print(f"\n{i+1}. {product['name']}")
        print(f"   Original: ₹{product['original_price']}")
        print(f"   Discounted: ₹{product['discounted_price']}")
        print(f"   Discount: {product['discount_percentage']}%")
        print(f"   Category: {product['category']}")