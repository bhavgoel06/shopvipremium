import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin
import random

class DetailedProductScraper:
    def __init__(self):
        self.base_url = "https://shopallpremium.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove common unwanted text
        text = re.sub(r'All Premium Shop.*?CategoryWhat\'s New.*?Porn', '', text, flags=re.DOTALL)
        text = re.sub(r'Track My Order.*?Contact Us', '', text, flags=re.DOTALL)
        text = re.sub(r'My Account.*?Account details', '', text, flags=re.DOTALL)
        return text.strip()
    
    def generate_realistic_reviews(self, product_name, count=None):
        """Generate realistic reviews with mixed names"""
        if count is None:
            count = random.randint(15, 45)
            
        indian_names = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anita', 'Ravi', 'Deepika', 'Arjun', 'Kavya', 'Suresh', 'Meera', 'Akash', 'Pooja', 'Nikhil', 'Shreya', 'Karan', 'Ritu', 'Sanjay', 'Nisha']
        international_names = ['John', 'Emma', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Anna', 'James', 'Maria', 'William', 'Jennifer', 'Richard', 'Jessica', 'Thomas', 'Ashley', 'Daniel', 'Amanda', 'Mark', 'Michelle']
        
        review_templates = [
            "Works perfectly! Quick delivery and great customer service.",
            "Amazing service. Got my account within 24 hours as promised.",
            "Excellent quality and very affordable. Highly recommend!",
            "Great value for money. The account is working flawlessly.",
            "Fast delivery and responsive support team. Will buy again!",
            "Perfect service! Account details were sent immediately.",
            "Very satisfied with the purchase. Everything works as expected.",
            "Outstanding service and genuine accounts. 5 stars!",
            "Quick and reliable service. Account is working perfectly.",
            "Excellent experience. Will definitely recommend to others.",
            "Great quality service at an affordable price point.",
            "Fast delivery and great customer support. Very happy!",
            "Reliable service with instant delivery. Highly recommended.",
            "Perfect transaction. Account is working without any issues.",
            "Exceptional service quality. Will be a returning customer.",
            "Great value and excellent customer service. Five stars!",
            "Quick delivery and responsive support. Very satisfied.",
            "Excellent service with genuine accounts. Highly recommend!",
            "Fast and reliable service. Account works perfectly.",
            "Amazing experience. Great service and quick delivery."
        ]
        
        reviews = []
        all_names = indian_names + international_names
        
        for i in range(count):
            name = random.choice(all_names)
            review_text = random.choice(review_templates)
            rating = random.choice([4, 4, 4, 5, 5, 5, 5])  # Weighted towards 4-5 stars
            
            # Add product-specific touches
            if 'netflix' in product_name.lower():
                review_text = review_text.replace('account', 'Netflix account')
            elif 'spotify' in product_name.lower():
                review_text = review_text.replace('account', 'Spotify premium')
            elif 'onlyfans' in product_name.lower():
                review_text = review_text.replace('account', 'OnlyFans account')
            
            reviews.append({
                'reviewer_name': name,
                'rating': rating,
                'review_text': review_text,
                'date': f'2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
            })
        
        return reviews
    
    def scrape_product_details(self, product_url):
        """Scrape detailed product information"""
        try:
            print(f"Scraping: {product_url}")
            response = self.session.get(product_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1', class_='product_title') or soup.find('h1')
            product_name = self.clean_text(name_elem.text) if name_elem else ""
            
            # Extract proper description from the Description tab
            description = ""
            desc_tab = soup.find('div', {'id': 'tab-description'})
            if desc_tab:
                # Get all paragraphs and clean them
                paragraphs = desc_tab.find_all(['p', 'div', 'span'])
                desc_parts = []
                for p in paragraphs:
                    text = self.clean_text(p.text)
                    if text and len(text) > 10:  # Only meaningful text
                        desc_parts.append(text)
                description = ' '.join(desc_parts[:3])  # First 3 meaningful paragraphs
            
            # If no description found, create one
            if not description:
                description = f"Get premium access to {product_name} with full features and benefits. Instant delivery within 24 hours with 30-day warranty included."
            
            # Extract features
            features = []
            
            # Look for feature lists
            feature_lists = soup.find_all(['ul', 'ol'])
            for ul in feature_lists:
                items = ul.find_all('li')
                for item in items:
                    feature_text = self.clean_text(item.text)
                    if feature_text and len(feature_text) > 5 and len(feature_text) < 100:
                        features.append(feature_text)
            
            # Look for key features in product description
            if desc_tab:
                feature_keywords = ['✓', '•', '-', 'includes', 'features', 'access', 'premium', 'unlimited']
                text_content = desc_tab.text
                lines = text_content.split('\n')
                for line in lines:
                    line = self.clean_text(line)
                    if any(keyword in line.lower() for keyword in feature_keywords) and len(line) > 10 and len(line) < 100:
                        features.append(line)
            
            # Default features if none found
            if not features:
                features = [
                    "Instant delivery within 24 hours",
                    "Premium account with full access",
                    "30-day warranty included",
                    "24/7 customer support",
                    "100% genuine accounts",
                    "Multiple duration options available",
                    "Secure payment processing"
                ]
            
            # Clean and limit features
            features = list(set(features))[:8]  # Remove duplicates and limit to 8
            
            # Extract pricing
            price_elem = soup.find('p', class_='price')
            original_price = 0
            discounted_price = 0
            
            if price_elem:
                # Look for original price (struck through)
                original_elem = price_elem.find('del') or price_elem.find('span', class_='woocommerce-Price-amount')
                if original_elem:
                    original_text = original_elem.text
                    price_match = re.search(r'₹([0-9,]+)', original_text)
                    if price_match:
                        original_price = float(price_match.group(1).replace(',', ''))
                
                # Look for discounted price
                discounted_elem = price_elem.find('ins')
                if discounted_elem:
                    discounted_text = discounted_elem.text
                    price_match = re.search(r'₹([0-9,]+)', discounted_text)
                    if price_match:
                        discounted_price = float(price_match.group(1).replace(',', ''))
                else:
                    # Single price
                    price_match = re.search(r'₹([0-9,]+)', price_elem.text)
                    if price_match:
                        discounted_price = float(price_match.group(1).replace(',', ''))
                        original_price = discounted_price * 1.5  # Assume some discount
            
            # Calculate discount
            discount_percentage = 0
            if original_price > 0 and discounted_price > 0:
                discount_percentage = int(((original_price - discounted_price) / original_price) * 100)
            
            # Generate reviews
            reviews = self.generate_realistic_reviews(product_name)
            
            return {
                'name': product_name,
                'description': description,
                'features': features,
                'original_price': original_price,
                'discounted_price': discounted_price,
                'discount_percentage': discount_percentage,
                'reviews': reviews,
                'total_reviews': len(reviews),
                'rating': round(sum(r['rating'] for r in reviews) / len(reviews), 1) if reviews else 4.5
            }
            
        except Exception as e:
            print(f"Error scraping {product_url}: {e}")
            return None
    
    def scrape_all_product_details(self):
        """Scrape all product details from the site"""
        print("Getting product URLs...")
        
        # Get all product URLs
        product_urls = set()
        
        # Scrape from main pages
        pages_to_scrape = [
            f"{self.base_url}/",
            f"{self.base_url}/shop/",
            f"{self.base_url}/shop/page/2/",
            f"{self.base_url}/shop/page/3/",
            f"{self.base_url}/popular/",
        ]
        
        for page_url in pages_to_scrape:
            try:
                response = self.session.get(page_url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find product links
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if '/product/' in href:
                        full_url = urljoin(self.base_url, href)
                        product_urls.add(full_url)
                        
            except Exception as e:
                print(f"Error scraping {page_url}: {e}")
            
            time.sleep(1)
        
        print(f"Found {len(product_urls)} product URLs")
        
        # Scrape each product
        all_products = []
        for i, url in enumerate(product_urls):
            print(f"Processing {i+1}/{len(product_urls)}: {url}")
            
            product_data = self.scrape_product_details(url)
            if product_data:
                all_products.append(product_data)
            
            time.sleep(1)  # Be respectful
        
        # Save to file
        with open('detailed_products.json', 'w', encoding='utf-8') as f:
            json.dump(all_products, f, indent=2, ensure_ascii=False)
        
        print(f"\nScraping complete! Found {len(all_products)} products with detailed information.")
        
        return all_products

if __name__ == "__main__":
    scraper = DetailedProductScraper()
    products = scraper.scrape_all_product_details()
    
    # Show samples
    print("\n=== SAMPLE PRODUCTS ===")
    for i, product in enumerate(products[:3]):
        print(f"\n{i+1}. {product['name']}")
        print(f"   Description: {product['description'][:100]}...")
        print(f"   Features: {product['features'][:3]}")
        print(f"   Price: ₹{product['original_price']} → ₹{product['discounted_price']} ({product['discount_percentage']}% off)")
        print(f"   Reviews: {product['total_reviews']} reviews, {product['rating']} stars")