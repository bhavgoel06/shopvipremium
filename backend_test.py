#!/usr/bin/env python3

import requests
import json
import sys
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

class BackendTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_data = {
            "first_name": "Sarah",
            "last_name": "Johnson", 
            "email": "sarah.johnson@premiumsubs.com",
            "password": "SecurePass123!"
        }
        self.login_data = {
            "email": "sarah.johnson@premiumsubs.com",
            "password": "SecurePass123!"
        }
        
        print(f"🔗 Testing backend at: {self.api_url}")
        print("=" * 60)

    def test_health_check(self):
        """Test basic health check endpoint"""
        print("🏥 Testing health check...")
        try:
            response = self.session.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data.get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

    def test_root_endpoint(self):
        """Test root API endpoint"""
        print("🏠 Testing root endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint working: {data.get('message', 'unknown')}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False

    def test_user_registration(self):
        """Test user registration endpoint"""
        print("👤 Testing user registration...")
        try:
            response = self.session.post(
                f"{self.api_url}/auth/register",
                json=self.test_user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('access_token'):
                    self.auth_token = data['data']['access_token']
                    user_info = data['data']['user']
                    print(f"✅ Registration successful for: {user_info['first_name']} {user_info['last_name']}")
                    print(f"   Email: {user_info['email']}")
                    print(f"   User ID: {user_info['id']}")
                    return True
                else:
                    print(f"❌ Registration failed: Invalid response format")
                    return False
            elif response.status_code == 400:
                # User might already exist, try to continue with login
                print("⚠️  User already exists, will test login instead")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False

    def test_user_login(self):
        """Test user login endpoint"""
        print("🔐 Testing user login...")
        try:
            response = self.session.post(
                f"{self.api_url}/auth/login",
                json=self.login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('access_token'):
                    self.auth_token = data['data']['access_token']
                    user_info = data['data']['user']
                    print(f"✅ Login successful for: {user_info['first_name']} {user_info['last_name']}")
                    print(f"   Token type: {data['data']['token_type']}")
                    return True
                else:
                    print(f"❌ Login failed: Invalid response format")
                    return False
            else:
                print(f"❌ Login failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        print("🚫 Testing invalid login...")
        try:
            invalid_data = {
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
            response = self.session.post(
                f"{self.api_url}/auth/login",
                json=invalid_data,
                timeout=10
            )
            
            if response.status_code == 401:
                print("✅ Invalid login correctly rejected")
                return True
            else:
                print(f"❌ Invalid login should return 401, got: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Invalid login test error: {e}")
            return False

    def test_current_user(self):
        """Test getting current user info with JWT token"""
        print("👥 Testing current user endpoint...")
        if not self.auth_token:
            print("❌ No auth token available for current user test")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.get(
                f"{self.api_url}/auth/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Current user retrieved: {user_data['first_name']} {user_data['last_name']}")
                print(f"   Email: {user_data['email']}")
                return True
            else:
                print(f"❌ Current user failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Current user error: {e}")
            return False

    def test_current_user_without_token(self):
        """Test accessing protected endpoint without token"""
        print("🔒 Testing protected endpoint without token...")
        try:
            response = self.session.get(f"{self.api_url}/auth/me", timeout=10)
            
            if response.status_code == 403:
                print("✅ Protected endpoint correctly requires authentication")
                return True
            else:
                print(f"❌ Protected endpoint should return 403, got: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Protected endpoint test error: {e}")
            return False

    def test_products_endpoint(self):
        """Test products listing endpoint"""
        print("📦 Testing products endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/products", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    total = data.get('total', 0)
                    print(f"✅ Products retrieved successfully: {len(products)} products (Total: {total})")
                    
                    if products:
                        sample_product = products[0]
                        print(f"   Sample product: {sample_product.get('name', 'Unknown')}")
                        print(f"   Category: {sample_product.get('category', 'Unknown')}")
                        print(f"   Price: ${sample_product.get('discounted_price', 0)}")
                    
                    return True
                else:
                    print(f"❌ Products endpoint: Invalid response format")
                    return False
            else:
                print(f"❌ Products endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Products endpoint error: {e}")
            return False

    def test_featured_products(self):
        """Test featured products endpoint"""
        print("⭐ Testing featured products...")
        try:
            response = self.session.get(f"{self.api_url}/products/featured", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    featured = data['data']
                    print(f"✅ Featured products retrieved: {len(featured)} products")
                    
                    if featured:
                        sample = featured[0]
                        print(f"   Featured product: {sample.get('name', 'Unknown')}")
                    
                    return True
                else:
                    print(f"❌ Featured products: Invalid response format")
                    return False
            else:
                print(f"❌ Featured products failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Featured products error: {e}")
            return False

    def test_bestseller_products(self):
        """Test bestseller products endpoint"""
        print("🏆 Testing bestseller products...")
        try:
            response = self.session.get(f"{self.api_url}/products/bestsellers", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    bestsellers = data['data']
                    print(f"✅ Bestseller products retrieved: {len(bestsellers)} products")
                    
                    if bestsellers:
                        sample = bestsellers[0]
                        print(f"   Bestseller product: {sample.get('name', 'Unknown')}")
                    
                    return True
                else:
                    print(f"❌ Bestseller products: Invalid response format")
                    return False
            else:
                print(f"❌ Bestseller products failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Bestseller products error: {e}")
            return False

    def test_product_search(self):
        """Test product search endpoint"""
        print("🔍 Testing product search...")
        try:
            response = self.session.get(f"{self.api_url}/products/search?q=netflix", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    results = data['data']
                    print(f"✅ Product search working: {len(results)} results for 'netflix'")
                    return True
                else:
                    print(f"❌ Product search: Invalid response format")
                    return False
            else:
                print(f"❌ Product search failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product search error: {e}")
            return False

    def test_expanded_product_catalog(self):
        """Test the expanded product catalog with 58 products"""
        print("📈 Testing expanded product catalog (58 products)...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=100", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    total = data.get('total', 0)
                    print(f"✅ Expanded catalog retrieved: {len(products)} products shown, {total} total")
                    
                    if total >= 58:
                        print(f"✅ Catalog expansion successful: {total} products (target: 58+)")
                        return True
                    else:
                        print(f"❌ Catalog expansion incomplete: {total} products (expected: 58+)")
                        return False
                else:
                    print(f"❌ Expanded catalog: Invalid response format")
                    return False
            else:
                print(f"❌ Expanded catalog failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Expanded catalog error: {e}")
            return False

    def test_adult_content_products(self):
        """Test adult content products are included and accessible"""
        print("🔞 Testing adult content products...")
        try:
            response = self.session.get(f"{self.api_url}/products?category=adult", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    adult_products = data['data']
                    print(f"✅ Adult content products accessible: {len(adult_products)} products")
                    
                    if adult_products:
                        sample = adult_products[0]
                        print(f"   Sample adult product: {sample.get('name', 'Unknown')}")
                        print(f"   Category: {sample.get('category', 'Unknown')}")
                        
                        # Verify pricing structure
                        if 'original_price' in sample and 'discounted_price' in sample:
                            print(f"   Pricing: ${sample.get('original_price')} → ${sample.get('discounted_price')}")
                            return True
                        else:
                            print("❌ Adult products missing pricing structure")
                            return False
                    else:
                        print("❌ No adult content products found")
                        return False
                else:
                    print(f"❌ Adult content: Invalid response format")
                    return False
            else:
                print(f"❌ Adult content failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Adult content error: {e}")
            return False

    def test_category_filtering(self):
        """Test product filtering by all categories"""
        print("🏷️ Testing category filtering...")
        categories_to_test = [
            'adult', 'ott', 'software', 'vpn', 'education', 
            'social_media', 'gaming', 'health', 'membership', 
            'professional', 'financial'
        ]
        
        passed_categories = 0
        total_categories = len(categories_to_test)
        
        for category in categories_to_test:
            try:
                response = self.session.get(f"{self.api_url}/products?category={category}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and isinstance(data.get('data'), list):
                        products = data['data']
                        print(f"   ✅ {category}: {len(products)} products")
                        passed_categories += 1
                    else:
                        print(f"   ❌ {category}: Invalid response format")
                else:
                    print(f"   ❌ {category}: Failed ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {category}: Error ({e})")
        
        success_rate = (passed_categories / total_categories) * 100
        print(f"✅ Category filtering: {passed_categories}/{total_categories} categories working ({success_rate:.1f}%)")
        return passed_categories >= 8  # At least 8 out of 11 categories should work

    def test_pricing_structure(self):
        """Test pricing display with original vs discounted prices"""
        print("💰 Testing pricing structure...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=10", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    pricing_valid = 0
                    discount_valid = 0
                    
                    for product in products:
                        # Check required pricing fields
                        if all(field in product for field in ['original_price', 'discounted_price', 'discount_percentage']):
                            pricing_valid += 1
                            
                            # Verify discount calculation
                            original = float(product['original_price'])
                            discounted = float(product['discounted_price'])
                            discount_pct = float(product['discount_percentage'])
                            
                            expected_discount = ((original - discounted) / original) * 100
                            if abs(expected_discount - discount_pct) < 1:  # Allow 1% tolerance
                                discount_valid += 1
                    
                    print(f"✅ Pricing structure: {pricing_valid}/{len(products)} products have complete pricing")
                    print(f"✅ Discount calculations: {discount_valid}/{len(products)} products have correct discounts")
                    
                    if pricing_valid >= len(products) * 0.9:  # 90% should have complete pricing
                        return True
                    else:
                        print("❌ Too many products missing pricing structure")
                        return False
                else:
                    print(f"❌ Pricing test: Invalid response format")
                    return False
            else:
                print(f"❌ Pricing test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Pricing test error: {e}")
            return False

    def test_reviews_system(self):
        """Test that products have 4-5 star reviews"""
        print("⭐ Testing reviews system...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=10", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    reviews_valid = 0
                    
                    for product in products:
                        if 'rating' in product and 'reviews_count' in product:
                            rating = float(product['rating'])
                            reviews_count = int(product['reviews_count'])
                            
                            if 4.0 <= rating <= 5.0 and reviews_count > 0:
                                reviews_valid += 1
                    
                    print(f"✅ Reviews system: {reviews_valid}/{len(products)} products have 4-5 star reviews")
                    
                    if reviews_valid >= len(products) * 0.8:  # 80% should have good reviews
                        return True
                    else:
                        print("❌ Too many products missing proper reviews")
                        return False
                else:
                    print(f"❌ Reviews test: Invalid response format")
                    return False
            else:
                print(f"❌ Reviews test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Reviews test error: {e}")
            return False

    def test_stock_quantities(self):
        """Test that products have proper stock quantities"""
        print("📦 Testing stock quantities...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=20", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    stock_valid = 0
                    
                    for product in products:
                        if 'stock_quantity' in product and 'status' in product:
                            stock = int(product['stock_quantity'])
                            status = product['status']
                            
                            if stock > 0 and status == 'active':
                                stock_valid += 1
                    
                    print(f"✅ Stock management: {stock_valid}/{len(products)} products have proper stock")
                    
                    if stock_valid >= len(products) * 0.9:  # 90% should have stock
                        return True
                    else:
                        print("❌ Too many products out of stock or invalid status")
                        return False
                else:
                    print(f"❌ Stock test: Invalid response format")
                    return False
            else:
                print(f"❌ Stock test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Stock test error: {e}")
            return False

    def test_currency_conversion_data(self):
        """Test that backend provides proper data for USD/INR conversion"""
        print("💱 Testing currency conversion data...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=5", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    
                    for product in products:
                        # Check that backend provides the necessary price data
                        required_fields = ['original_price', 'discounted_price', 'discount_percentage']
                        if all(field in product for field in required_fields):
                            print(f"   ✅ {product.get('name', 'Unknown')}: Complete pricing data")
                        else:
                            print(f"   ❌ {product.get('name', 'Unknown')}: Missing pricing fields")
                            return False
                    
                    print("✅ Currency conversion: Backend provides proper price data for frontend conversion")
                    return True
                else:
                    print(f"❌ Currency test: Invalid response format")
                    return False
            else:
                print(f"❌ Currency test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Currency test error: {e}")
            return False

    def test_categories_endpoint(self):
        """Test categories endpoint"""
        print("📂 Testing categories endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/categories", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    categories = data['data']
                    print(f"✅ Categories retrieved: {len(categories)} categories")
                    
                    if categories:
                        sample = categories[0]
                        print(f"   Sample category: {sample.get('name', 'Unknown')}")
                    
                    return True
                else:
                    print(f"❌ Categories: Invalid response format")
                    return False
            else:
                print(f"❌ Categories failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Categories error: {e}")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Backend API Tests")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("Root Endpoint", self.test_root_endpoint),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Invalid Login", self.test_invalid_login),
            ("Current User (Protected)", self.test_current_user),
            ("Protected Without Token", self.test_current_user_without_token),
            ("Products Listing", self.test_products_endpoint),
            ("Featured Products", self.test_featured_products),
            ("Bestseller Products", self.test_bestseller_products),
            ("Product Search", self.test_product_search),
            ("Categories", self.test_categories_endpoint),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                failed += 1
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 All backend tests passed!")
            return True
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check the details above.")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)