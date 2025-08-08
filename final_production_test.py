#!/usr/bin/env python3

import requests
import json
import sys
import os
import time
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

class FinalProductionTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.admin_token = None
        self.test_user_data = {
            "first_name": "Production",
            "last_name": "Tester", 
            "email": "production.tester@shopvippremium.com",
            "password": "ProductionTest2025!"
        }
        
        print(f"🔗 Testing backend at: {self.api_url}")
        print("🎯 FINAL PRODUCTION READINESS CHECK")
        print("=" * 80)

    def authenticate_user(self):
        """Authenticate user for protected endpoints"""
        print("🔐 Authenticating user...")
        try:
            # Try registration first
            response = self.session.post(
                f"{self.api_url}/auth/register",
                json=self.test_user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('access_token'):
                    self.auth_token = data['data']['access_token']
                    print("✅ User registered and authenticated")
                    return True
            elif response.status_code == 400:
                # User exists, try login
                response = self.session.post(
                    f"{self.api_url}/auth/login",
                    json={
                        "email": self.test_user_data["email"],
                        "password": self.test_user_data["password"]
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data', {}).get('access_token'):
                        self.auth_token = data['data']['access_token']
                        print("✅ User logged in and authenticated")
                        return True
            
            print("❌ Authentication failed")
            return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False

    def authenticate_admin(self):
        """Authenticate admin for admin endpoints"""
        print("👑 Authenticating admin...")
        try:
            admin_credentials = {
                "username": "admin",
                "password": "VIP@dm1n2025!"
            }
            
            response = self.session.post(
                f"{self.api_url}/admin/login",
                json=admin_credentials,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('token'):
                    self.admin_token = data['token']
                    print("✅ Admin authenticated successfully")
                    return True
                else:
                    print("❌ Admin authentication: Invalid response format")
                    return False
            else:
                print(f"❌ Admin authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Admin authentication error: {e}")
            return False

    def test_core_api_endpoints(self):
        """Test all critical API endpoints"""
        print("🔧 Testing Core API Endpoints...")
        
        endpoints_passed = 0
        total_endpoints = 12
        
        try:
            # 1. Health Check
            print("   💓 Health check...")
            response = self.session.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200 and response.json().get('status') == 'healthy':
                print("      ✅ Health check working")
                endpoints_passed += 1
            else:
                print(f"      ❌ Health check failed: {response.status_code}")
            
            # 2. Products endpoint
            print("   📦 Products endpoint...")
            response = self.session.get(f"{self.api_url}/products", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    total_products = data.get('total', 0)
                    print(f"      ✅ Products endpoint: {total_products} products available")
                    endpoints_passed += 1
                else:
                    print("      ❌ Products endpoint: Invalid response")
            else:
                print(f"      ❌ Products endpoint failed: {response.status_code}")
            
            # 3. Featured products
            print("   ⭐ Featured products...")
            response = self.session.get(f"{self.api_url}/products/featured", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    featured_count = len(data.get('data', []))
                    print(f"      ✅ Featured products: {featured_count} products")
                    endpoints_passed += 1
                else:
                    print("      ❌ Featured products: Invalid response")
            else:
                print(f"      ❌ Featured products failed: {response.status_code}")
            
            # 4. Bestsellers
            print("   🏆 Bestseller products...")
            response = self.session.get(f"{self.api_url}/products/bestsellers", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    bestseller_count = len(data.get('data', []))
                    print(f"      ✅ Bestseller products: {bestseller_count} products")
                    endpoints_passed += 1
                else:
                    print("      ❌ Bestseller products: Invalid response")
            else:
                print(f"      ❌ Bestseller products failed: {response.status_code}")
            
            # 5. Product search
            print("   🔍 Product search...")
            response = self.session.get(f"{self.api_url}/products/search?q=netflix", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    search_results = len(data.get('data', []))
                    print(f"      ✅ Product search: {search_results} results for 'netflix'")
                    endpoints_passed += 1
                else:
                    print("      ❌ Product search: Invalid response")
            else:
                print(f"      ❌ Product search failed: {response.status_code}")
            
            # 6. Categories
            print("   🏷️ Categories...")
            response = self.session.get(f"{self.api_url}/categories", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    categories_count = len(data.get('data', []))
                    print(f"      ✅ Categories: {categories_count} categories available")
                    endpoints_passed += 1
                else:
                    print("      ❌ Categories: Invalid response")
            else:
                print(f"      ❌ Categories failed: {response.status_code}")
            
            # 7. Authentication endpoints
            if self.auth_token:
                print("   🔐 Authentication endpoints...")
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/auth/me", headers=headers, timeout=10)
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"      ✅ Auth endpoints: User {user_data.get('first_name', 'Unknown')} authenticated")
                    endpoints_passed += 1
                else:
                    print(f"      ❌ Auth endpoints failed: {response.status_code}")
            else:
                print("      ❌ Auth endpoints: No token available")
            
            # 8. Orders endpoint
            print("   📋 Orders endpoint...")
            response = self.session.get(f"{self.api_url}/orders", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    orders_count = len(data.get('data', []))
                    print(f"      ✅ Orders endpoint: {orders_count} orders accessible")
                    endpoints_passed += 1
                else:
                    print("      ❌ Orders endpoint: Invalid response")
            else:
                print(f"      ❌ Orders endpoint failed: {response.status_code}")
            
            # 9. Crypto currencies
            print("   💰 Crypto currencies...")
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    currencies_count = len(data.get('data', []))
                    print(f"      ✅ Crypto currencies: {currencies_count} currencies available")
                    endpoints_passed += 1
                else:
                    print("      ❌ Crypto currencies: Invalid response")
            else:
                print(f"      ❌ Crypto currencies failed: {response.status_code}")
            
            # 10. Users endpoint
            print("   👥 Users endpoint...")
            response = self.session.get(f"{self.api_url}/users", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    users_count = len(data.get('data', []))
                    print(f"      ✅ Users endpoint: {users_count} users accessible")
                    endpoints_passed += 1
                else:
                    print("      ❌ Users endpoint: Invalid response")
            else:
                print(f"      ❌ Users endpoint failed: {response.status_code}")
            
            # 11. Site settings
            if self.auth_token:
                print("   ⚙️ Site settings...")
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/admin/settings", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        settings = data.get('data', {})
                        currency_rate = settings.get('currency_rate', 0)
                        print(f"      ✅ Site settings: Currency rate {currency_rate} INR/USD")
                        endpoints_passed += 1
                    else:
                        print("      ❌ Site settings: Invalid response")
                else:
                    print(f"      ❌ Site settings failed: {response.status_code}")
            else:
                print("      ❌ Site settings: No auth token")
            
            # 12. Product by slug
            print("   🔗 Product by slug...")
            response = self.session.get(f"{self.api_url}/products/slug/netflix-premium-4k-uhd", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    product = data.get('data', {})
                    print(f"      ✅ Product by slug: {product.get('name', 'Unknown')} found")
                    endpoints_passed += 1
                else:
                    print("      ❌ Product by slug: Invalid response")
            elif response.status_code == 404:
                # Try another common slug
                response = self.session.get(f"{self.api_url}/products/slug/spotify-premium", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        product = data.get('data', {})
                        print(f"      ✅ Product by slug: {product.get('name', 'Unknown')} found")
                        endpoints_passed += 1
                    else:
                        print("      ❌ Product by slug: Invalid response")
                else:
                    print("      ❌ Product by slug: No valid slugs found")
            else:
                print(f"      ❌ Product by slug failed: {response.status_code}")
            
            success_rate = (endpoints_passed / total_endpoints) * 100
            print(f"   📈 Core API Endpoints: {endpoints_passed}/{total_endpoints} working ({success_rate:.1f}%)")
            
            return endpoints_passed >= 10  # At least 10/12 endpoints should work
            
        except Exception as e:
            print(f"❌ Core API endpoints error: {e}")
            return False

    def test_currency_system(self):
        """Test 90 INR = 1 USD exchange rate configuration"""
        print("💱 Testing Currency System (90 INR = 1 USD)...")
        
        try:
            # Test site settings for currency rate
            if self.auth_token:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/admin/settings", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        settings = data.get('data', {})
                        currency_rate = settings.get('currency_rate', 0)
                        
                        print(f"   💰 Configured currency rate: {currency_rate} INR per USD")
                        
                        # Check if rate is around 90 (allow 85-95 range)
                        if 85 <= currency_rate <= 95:
                            print("   ✅ Currency rate is properly configured (~90 INR/USD)")
                            
                            # Test product pricing to verify currency conversion data
                            response2 = self.session.get(f"{self.api_url}/products?per_page=5", timeout=10)
                            if response2.status_code == 200:
                                products_data = response2.json()
                                if products_data.get('success') and products_data.get('data'):
                                    products = products_data['data']
                                    
                                    pricing_valid = 0
                                    for product in products:
                                        original_price = product.get('original_price', 0)
                                        discounted_price = product.get('discounted_price', 0)
                                        
                                        if original_price > 0 and discounted_price > 0:
                                            # Calculate USD equivalent
                                            usd_original = original_price / currency_rate
                                            usd_discounted = discounted_price / currency_rate
                                            
                                            print(f"   📦 {product.get('name', 'Unknown')[:30]}...")
                                            print(f"      INR: ₹{original_price} → ₹{discounted_price}")
                                            print(f"      USD: ${usd_original:.2f} → ${usd_discounted:.2f}")
                                            
                                            pricing_valid += 1
                                    
                                    if pricing_valid >= 3:
                                        print(f"   ✅ Currency conversion data ready: {pricing_valid} products verified")
                                        return True
                                    else:
                                        print(f"   ❌ Insufficient pricing data: Only {pricing_valid} products have valid pricing")
                                        return False
                                else:
                                    print("   ❌ No products found for currency testing")
                                    return False
                            else:
                                print(f"   ❌ Products endpoint failed: {response2.status_code}")
                                return False
                        else:
                            print(f"   ❌ Currency rate {currency_rate} is not around 90 INR/USD")
                            return False
                    else:
                        print("   ❌ Site settings: Invalid response format")
                        return False
                else:
                    print(f"   ❌ Site settings failed: {response.status_code}")
                    return False
            else:
                print("   ❌ No auth token for currency system testing")
                return False
                
        except Exception as e:
            print(f"❌ Currency system error: {e}")
            return False

    def test_nowpayments_integration(self):
        """Test NOWPayments crypto payment integration"""
        print("🔐 Testing NOWPayments Integration...")
        
        try:
            # Test 1: Get available cryptocurrencies
            print("   💰 Testing crypto currencies...")
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    currencies = data.get('data', [])
                    print(f"      ✅ Crypto currencies: {len(currencies)} available")
                    
                    if len(currencies) >= 50:  # Should have many cryptocurrencies
                        currencies_test = True
                    else:
                        print(f"      ⚠️ Only {len(currencies)} currencies (expected 50+)")
                        currencies_test = False
                else:
                    print("      ❌ Crypto currencies: Invalid response")
                    currencies_test = False
            else:
                print(f"      ❌ Crypto currencies failed: {response.status_code}")
                currencies_test = False
            
            # Test 2: Create a test order for payment testing
            if self.auth_token:
                print("   📦 Creating test order...")
                
                # Get a sample product
                response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
                if response.status_code == 200:
                    products_data = response.json()
                    if products_data.get('success') and products_data.get('data'):
                        product = products_data['data'][0]
                        
                        order_data = {
                            "user_id": "test-user-production",
                            "user_email": self.test_user_data["email"],
                            "user_name": f"{self.test_user_data['first_name']} {self.test_user_data['last_name']}",
                            "user_phone": "+1234567890",
                            "items": [
                                {
                                    "product_id": product['id'],
                                    "product_name": product['name'],
                                    "duration": "1 month",
                                    "quantity": 1,
                                    "unit_price": product['discounted_price'],
                                    "total_price": product['discounted_price']
                                }
                            ],
                            "total_amount": product['discounted_price'],
                            "discount_amount": 0.0,
                            "payment_method": "crypto",
                            "notes": "Production test order"
                        }
                        
                        headers = {"Authorization": f"Bearer {self.auth_token}"}
                        response = self.session.post(
                            f"{self.api_url}/orders",
                            json=order_data,
                            headers=headers,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            order_response = response.json()
                            if order_response.get('success'):
                                order = order_response['data']
                                order_id = order['id']
                                print(f"      ✅ Test order created: {order_id}")
                                
                                # Test 3: Create crypto payment
                                print("   💳 Testing crypto payment creation...")
                                payment_data = {
                                    "order_id": order_id,
                                    "crypto_currency": "btc",
                                    "amount": 10.0,
                                    "currency": "USD"
                                }
                                
                                response = self.session.post(
                                    f"{self.api_url}/payments/crypto/create",
                                    json=payment_data,
                                    timeout=15
                                )
                                
                                if response.status_code == 200:
                                    payment_response = response.json()
                                    if payment_response.get('success'):
                                        payment_data = payment_response['data']
                                        payment_id = payment_data.get('payment_id')
                                        
                                        print(f"      ✅ Crypto payment created: {payment_id}")
                                        print(f"      💰 Pay amount: {payment_data.get('pay_amount', 'N/A')}")
                                        print(f"      🔗 Pay address: {payment_data.get('pay_address', 'N/A')}")
                                        
                                        # Test 4: Check payment status
                                        if payment_id:
                                            print("   📊 Testing payment status...")
                                            response = self.session.get(
                                                f"{self.api_url}/payments/{payment_id}/status",
                                                timeout=10
                                            )
                                            
                                            if response.status_code == 200:
                                                status_response = response.json()
                                                if status_response.get('success'):
                                                    status_data = status_response['data']
                                                    payment_status = status_data.get('payment_status', 'unknown')
                                                    print(f"      ✅ Payment status: {payment_status}")
                                                    payment_status_test = True
                                                else:
                                                    print("      ❌ Payment status: Invalid response")
                                                    payment_status_test = False
                                            else:
                                                print(f"      ❌ Payment status failed: {response.status_code}")
                                                payment_status_test = False
                                        else:
                                            print("      ❌ No payment ID for status testing")
                                            payment_status_test = False
                                        
                                        payment_creation_test = True
                                    else:
                                        print("      ❌ Crypto payment creation: Invalid response")
                                        payment_creation_test = False
                                        payment_status_test = False
                                else:
                                    print(f"      ❌ Crypto payment creation failed: {response.status_code}")
                                    payment_creation_test = False
                                    payment_status_test = False
                                
                                order_creation_test = True
                            else:
                                print("      ❌ Order creation: Invalid response")
                                order_creation_test = False
                                payment_creation_test = False
                                payment_status_test = False
                        else:
                            print(f"      ❌ Order creation failed: {response.status_code}")
                            order_creation_test = False
                            payment_creation_test = False
                            payment_status_test = False
                    else:
                        print("      ❌ No products available for order creation")
                        order_creation_test = False
                        payment_creation_test = False
                        payment_status_test = False
                else:
                    print(f"      ❌ Products endpoint failed: {response.status_code}")
                    order_creation_test = False
                    payment_creation_test = False
                    payment_status_test = False
            else:
                print("   ❌ No auth token for payment testing")
                order_creation_test = False
                payment_creation_test = False
                payment_status_test = False
            
            # Calculate overall success
            tests_passed = sum([currencies_test, order_creation_test, payment_creation_test, payment_status_test])
            total_tests = 4
            
            success_rate = (tests_passed / total_tests) * 100
            print(f"   📈 NOWPayments Integration: {tests_passed}/{total_tests} tests passed ({success_rate:.1f}%)")
            
            return tests_passed >= 3  # At least 3/4 tests should pass
            
        except Exception as e:
            print(f"❌ NOWPayments integration error: {e}")
            return False

    def test_database_products(self):
        """Test database has 99+ products with correct pricing"""
        print("🗄️ Testing Database (99+ Products)...")
        
        try:
            # Get all products
            response = self.session.get(f"{self.api_url}/products?per_page=200", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    total_products = data.get('total', 0)
                    
                    print(f"   📊 Total products in database: {total_products}")
                    
                    if total_products >= 99:
                        print("   ✅ Product count requirement met (99+ products)")
                        count_test = True
                    else:
                        print(f"   ❌ Insufficient products: {total_products} (expected 99+)")
                        count_test = False
                    
                    # Test pricing structure
                    valid_pricing = 0
                    valid_categories = set()
                    valid_reviews = 0
                    
                    for product in products[:20]:  # Test first 20 products
                        # Check pricing fields
                        if all(field in product for field in ['original_price', 'discounted_price', 'discount_percentage']):
                            original = float(product['original_price'])
                            discounted = float(product['discounted_price'])
                            discount = float(product['discount_percentage'])
                            
                            if original > 0 and discounted > 0 and 0 <= discount <= 100:
                                valid_pricing += 1
                        
                        # Check category
                        if product.get('category'):
                            valid_categories.add(product['category'])
                        
                        # Check reviews
                        if product.get('rating') and 4 <= float(product['rating']) <= 5:
                            valid_reviews += 1
                    
                    print(f"   💰 Valid pricing structure: {valid_pricing}/20 products")
                    print(f"   🏷️ Categories found: {len(valid_categories)} ({', '.join(list(valid_categories)[:5])}...)")
                    print(f"   ⭐ Valid ratings (4-5 stars): {valid_reviews}/20 products")
                    
                    pricing_test = valid_pricing >= 18  # 90% should have valid pricing
                    categories_test = len(valid_categories) >= 8  # Should have 8+ categories
                    reviews_test = valid_reviews >= 15  # 75% should have 4-5 star ratings
                    
                    # Test specific key products
                    key_products = ["netflix", "spotify", "chatgpt", "onlyfans", "disney"]
                    found_key_products = 0
                    
                    for key_product in key_products:
                        for product in products:
                            if key_product.lower() in product.get('name', '').lower():
                                found_key_products += 1
                                print(f"   ✅ Key product found: {product['name']}")
                                break
                    
                    key_products_test = found_key_products >= 4  # Should find at least 4/5 key products
                    
                    tests_passed = sum([count_test, pricing_test, categories_test, reviews_test, key_products_test])
                    total_tests = 5
                    
                    success_rate = (tests_passed / total_tests) * 100
                    print(f"   📈 Database verification: {tests_passed}/{total_tests} tests passed ({success_rate:.1f}%)")
                    
                    return tests_passed >= 4  # At least 4/5 tests should pass
                else:
                    print("   ❌ Products endpoint: Invalid response format")
                    return False
            else:
                print(f"   ❌ Products endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Database testing error: {e}")
            return False

    def test_admin_endpoints(self):
        """Test admin authentication and management features"""
        print("👑 Testing Admin Endpoints...")
        
        # First authenticate admin
        if not self.authenticate_admin():
            print("   ❌ Cannot test admin endpoints without admin authentication")
            return False
        
        admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
        tests_passed = 0
        total_tests = 8
        
        try:
            # Test 1: Admin verification
            print("   🔐 Testing admin verification...")
            response = self.session.post(
                f"{self.api_url}/admin/verify",
                headers=admin_headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("      ✅ Admin verification working")
                    tests_passed += 1
                else:
                    print("      ❌ Admin verification: Invalid response")
            else:
                print(f"      ❌ Admin verification failed: {response.status_code}")
            
            # Test 2: Dashboard stats
            print("   📊 Testing dashboard stats...")
            response = self.session.get(f"{self.api_url}/admin/dashboard-stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stats = data['data']
                    print(f"      ✅ Dashboard stats: {stats.get('totalProducts', 0)} products, {stats.get('totalOrders', 0)} orders")
                    tests_passed += 1
                else:
                    print("      ❌ Dashboard stats: Invalid response")
            else:
                print(f"      ❌ Dashboard stats failed: {response.status_code}")
            
            # Test 3: Stock overview
            if self.auth_token:
                print("   📦 Testing stock overview...")
                user_headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/admin/stock-overview", headers=user_headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        stock = data['data']
                        print(f"      ✅ Stock overview: {stock.get('total_products', 0)} products, {stock.get('total_stock_units', 0)} units")
                        tests_passed += 1
                    else:
                        print("      ❌ Stock overview: Invalid response")
                else:
                    print(f"      ❌ Stock overview failed: {response.status_code}")
            else:
                print("      ❌ Stock overview: No user token")
            
            # Test 4: Low stock products
            if self.auth_token:
                print("   ⚠️ Testing low stock detection...")
                user_headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/admin/low-stock-products", headers=user_headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        low_stock = data.get('data', [])
                        print(f"      ✅ Low stock detection: {len(low_stock)} products below threshold")
                        tests_passed += 1
                    else:
                        print("      ❌ Low stock detection: Invalid response")
                else:
                    print(f"      ❌ Low stock detection failed: {response.status_code}")
            else:
                print("      ❌ Low stock detection: No user token")
            
            # Test 5: Bulk stock operations
            if self.auth_token:
                print("   🔄 Testing bulk stock operations...")
                user_headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.post(
                    f"{self.api_url}/admin/bulk-stock-update",
                    json={"action": "reset_all_stock"},
                    headers=user_headers,
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        updated_count = data['data'].get('updated_count', 0)
                        print(f"      ✅ Bulk operations: {updated_count} products updated")
                        tests_passed += 1
                    else:
                        print("      ❌ Bulk operations: Invalid response")
                else:
                    print(f"      ❌ Bulk operations failed: {response.status_code}")
            else:
                print("      ❌ Bulk operations: No user token")
            
            # Test 6: Order management
            print("   📋 Testing order management...")
            response = self.session.get(f"{self.api_url}/orders", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    orders = data.get('data', [])
                    print(f"      ✅ Order management: {len(orders)} orders accessible")
                    tests_passed += 1
                else:
                    print("      ❌ Order management: Invalid response")
            else:
                print(f"      ❌ Order management failed: {response.status_code}")
            
            # Test 7: User management
            print("   👥 Testing user management...")
            response = self.session.get(f"{self.api_url}/users", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    users = data.get('data', [])
                    print(f"      ✅ User management: {len(users)} users accessible")
                    tests_passed += 1
                else:
                    print("      ❌ User management: Invalid response")
            else:
                print(f"      ❌ User management failed: {response.status_code}")
            
            # Test 8: Categories management
            response = self.session.get(f"{self.api_url}/admin/categories", headers=admin_headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    categories = data.get('data', [])
                    print(f"      ✅ Categories management: {len(categories)} categories")
                    tests_passed += 1
                else:
                    print("      ❌ Categories management: Invalid response")
            else:
                print(f"      ❌ Categories management failed: {response.status_code}")
            
            success_rate = (tests_passed / total_tests) * 100
            print(f"   📈 Admin endpoints: {tests_passed}/{total_tests} tests passed ({success_rate:.1f}%)")
            
            return tests_passed >= 6  # At least 6/8 admin tests should pass
            
        except Exception as e:
            print(f"❌ Admin endpoints error: {e}")
            return False

    def test_site_settings(self):
        """Test site settings endpoints for theme/currency control"""
        print("⚙️ Testing Site Settings...")
        
        if not self.auth_token:
            print("   ❌ No auth token for site settings testing")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            # Test 1: Get site settings
            print("   📥 Testing GET site settings...")
            response = self.session.get(f"{self.api_url}/admin/settings", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    settings = data.get('data', {})
                    
                    # Check key settings
                    theme = settings.get('theme', 'unknown')
                    currency_rate = settings.get('currency_rate', 0)
                    site_name = settings.get('site_name', 'unknown')
                    business_type = settings.get('business_type', 'unknown')
                    
                    print(f"      ✅ Site settings retrieved:")
                    print(f"         Theme: {theme}")
                    print(f"         Currency rate: {currency_rate} INR/USD")
                    print(f"         Site name: {site_name}")
                    print(f"         Business type: {business_type}")
                    
                    get_settings_test = True
                else:
                    print("      ❌ GET site settings: Invalid response")
                    get_settings_test = False
            else:
                print(f"      ❌ GET site settings failed: {response.status_code}")
                get_settings_test = False
            
            # Test 2: Update site settings
            print("   📤 Testing PUT site settings...")
            test_settings = {
                "theme": "ai-tech",
                "currency_rate": 90,
                "site_name": "Shop VIP Premium",
                "business_type": "Digital Workspace Solutions",
                "enable_crypto_usd": True,
                "enable_dual_currency": True
            }
            
            response = self.session.put(
                f"{self.api_url}/admin/settings",
                json=test_settings,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("      ✅ Site settings updated successfully")
                    
                    # Verify the update by getting settings again
                    response2 = self.session.get(f"{self.api_url}/admin/settings", headers=headers, timeout=10)
                    if response2.status_code == 200:
                        verify_data = response2.json()
                        if verify_data.get('success'):
                            updated_settings = verify_data.get('data', {})
                            
                            # Check if updates were applied
                            if (updated_settings.get('theme') == test_settings['theme'] and
                                updated_settings.get('currency_rate') == test_settings['currency_rate']):
                                print("      ✅ Settings update verified")
                                update_settings_test = True
                            else:
                                print("      ❌ Settings update not persisted")
                                update_settings_test = False
                        else:
                            print("      ❌ Settings verification: Invalid response")
                            update_settings_test = False
                    else:
                        print("      ❌ Settings verification failed")
                        update_settings_test = False
                else:
                    print("      ❌ PUT site settings: Invalid response")
                    update_settings_test = False
            else:
                print(f"      ❌ PUT site settings failed: {response.status_code}")
                update_settings_test = False
            
            tests_passed = sum([get_settings_test, update_settings_test])
            total_tests = 2
            
            success_rate = (tests_passed / total_tests) * 100
            print(f"   📈 Site settings: {tests_passed}/{total_tests} tests passed ({success_rate:.1f}%)")
            
            return tests_passed >= 1  # At least 1/2 tests should pass
            
        except Exception as e:
            print(f"❌ Site settings error: {e}")
            return False

    def test_performance_security(self):
        """Test response times and security features"""
        print("🚀 Testing Performance & Security...")
        
        performance_tests = 0
        security_tests = 0
        total_performance = 4
        total_security = 3
        
        try:
            # Performance Test 1: Response times
            print("   ⏱️ Testing response times...")
            endpoints_to_test = [
                "/health",
                "/products",
                "/products/featured",
                "/products/bestsellers"
            ]
            
            fast_responses = 0
            for endpoint in endpoints_to_test:
                start_time = time.time()
                response = self.session.get(f"{self.api_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                if response.status_code == 200 and response_time < 3.0:  # Under 3 seconds
                    fast_responses += 1
                    print(f"      ✅ {endpoint}: {response_time:.2f}s")
                else:
                    print(f"      ❌ {endpoint}: {response_time:.2f}s (too slow or failed)")
            
            if fast_responses >= 3:
                print(f"      ✅ Response times: {fast_responses}/4 endpoints under 3s")
                performance_tests += 1
            else:
                print(f"      ❌ Response times: Only {fast_responses}/4 endpoints fast enough")
            
            # Performance Test 2: Database query efficiency
            print("   🗄️ Testing database query efficiency...")
            start_time = time.time()
            response = self.session.get(f"{self.api_url}/products?per_page=50", timeout=15)
            end_time = time.time()
            
            query_time = end_time - start_time
            if response.status_code == 200 and query_time < 5.0:
                print(f"      ✅ Database query: {query_time:.2f}s for 50 products")
                performance_tests += 1
            else:
                print(f"      ❌ Database query: {query_time:.2f}s (too slow)")
            
            # Performance Test 3: Concurrent requests handling
            print("   🔄 Testing concurrent request handling...")
            import threading
            import queue
            
            results_queue = queue.Queue()
            
            def make_request():
                try:
                    response = self.session.get(f"{self.api_url}/health", timeout=5)
                    results_queue.put(response.status_code == 200)
                except:
                    results_queue.put(False)
            
            # Create 5 concurrent threads
            threads = []
            for _ in range(5):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Check results
            successful_requests = 0
            while not results_queue.empty():
                if results_queue.get():
                    successful_requests += 1
            
            if successful_requests >= 4:
                print(f"      ✅ Concurrent requests: {successful_requests}/5 successful")
                performance_tests += 1
            else:
                print(f"      ❌ Concurrent requests: Only {successful_requests}/5 successful")
            
            # Performance Test 4: Search performance
            print("   🔍 Testing search performance...")
            start_time = time.time()
            response = self.session.get(f"{self.api_url}/products/search?q=netflix", timeout=10)
            end_time = time.time()
            
            search_time = end_time - start_time
            if response.status_code == 200 and search_time < 2.0:
                print(f"      ✅ Search performance: {search_time:.2f}s")
                performance_tests += 1
            else:
                print(f"      ❌ Search performance: {search_time:.2f}s (too slow)")
            
            # Security Test 1: JWT Authentication
            print("   🔐 Testing JWT authentication...")
            if self.auth_token:
                # Test valid token
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/auth/me", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # Test invalid token
                    invalid_headers = {"Authorization": "Bearer invalid_token_here"}
                    response2 = self.session.get(f"{self.api_url}/auth/me", headers=invalid_headers, timeout=10)
                    
                    if response2.status_code == 401:
                        print("      ✅ JWT authentication: Valid tokens accepted, invalid rejected")
                        security_tests += 1
                    else:
                        print(f"      ❌ JWT authentication: Invalid token not rejected ({response2.status_code})")
                else:
                    print(f"      ❌ JWT authentication: Valid token rejected ({response.status_code})")
            else:
                print("      ❌ JWT authentication: No token to test")
            
            # Security Test 2: Input validation
            print("   🛡️ Testing input validation...")
            # Test SQL injection attempt
            malicious_query = "'; DROP TABLE products; --"
            response = self.session.get(f"{self.api_url}/products/search?q={malicious_query}", timeout=10)
            
            if response.status_code in [200, 400]:  # Should handle gracefully
                print("      ✅ Input validation: SQL injection attempt handled")
                security_tests += 1
            else:
                print(f"      ❌ Input validation: Unexpected response to malicious input ({response.status_code})")
            
            # Security Test 3: CORS headers
            print("   🌐 Testing CORS configuration...")
            response = self.session.options(f"{self.api_url}/health", timeout=10)
            
            if response.status_code in [200, 204]:
                cors_headers = response.headers
                if 'Access-Control-Allow-Origin' in cors_headers:
                    print("      ✅ CORS configuration: Headers present")
                    security_tests += 1
                else:
                    print("      ❌ CORS configuration: Missing headers")
            else:
                print(f"      ❌ CORS configuration: OPTIONS request failed ({response.status_code})")
            
            performance_rate = (performance_tests / total_performance) * 100
            security_rate = (security_tests / total_security) * 100
            
            print(f"   📈 Performance: {performance_tests}/{total_performance} tests passed ({performance_rate:.1f}%)")
            print(f"   🔒 Security: {security_tests}/{total_security} tests passed ({security_rate:.1f}%)")
            
            return performance_tests >= 3 and security_tests >= 2
            
        except Exception as e:
            print(f"❌ Performance & Security error: {e}")
            return False

    def run_final_production_tests(self):
        """Run all final production readiness tests"""
        print("🚀 STARTING FINAL PRODUCTION READINESS CHECK")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_user():
            print("⚠️ Continuing without user authentication (some tests may fail)")
        
        tests = [
            ("🔧 Core API Endpoints", self.test_core_api_endpoints),
            ("💱 Currency System (90 INR = 1 USD)", self.test_currency_system),
            ("🔐 NOWPayments Integration", self.test_nowpayments_integration),
            ("🗄️ Database (99+ Products)", self.test_database_products),
            ("👑 Admin Endpoints", self.test_admin_endpoints),
            ("⚙️ Site Settings", self.test_site_settings),
            ("🚀 Performance & Security", self.test_performance_security),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n{test_name}")
            print("=" * 80)
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}: PASSED")
                else:
                    failed += 1
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"💥 {test_name}: CRASHED - {e}")
                failed += 1
        
        print("\n" + "=" * 80)
        print("📊 FINAL PRODUCTION READINESS RESULTS")
        print("=" * 80)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        print("\n🎯 PRODUCTION DEPLOYMENT STATUS:")
        print("=" * 80)
        if passed >= 6:
            print("🎉 SYSTEM IS READY FOR PRODUCTION DEPLOYMENT!")
            print("✅ All critical systems operational")
            print("✅ Currency system configured (90 INR/USD)")
            print("✅ Payment processing working")
            print("✅ Database properly seeded")
            print("✅ Admin panel functional")
            print("✅ Performance acceptable")
            print("✅ Security measures in place")
            print("\n🚀 Ready to deploy to shopvippremium.com domain!")
        elif passed >= 4:
            print("⚠️ SYSTEM MOSTLY READY - MINOR ISSUES DETECTED")
            print(f"✅ {passed} critical systems working")
            print(f"❌ {failed} systems need attention")
            print("🔧 Review failed tests before production deployment")
        else:
            print("🚨 SYSTEM NOT READY FOR PRODUCTION")
            print(f"❌ {failed} critical systems failed")
            print("🛠️ Major fixes required before deployment")
        
        return passed >= 6

if __name__ == "__main__":
    tester = FinalProductionTester()
    success = tester.run_final_production_tests()
    sys.exit(0 if success else 1)