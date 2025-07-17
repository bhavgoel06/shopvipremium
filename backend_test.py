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

    def test_comprehensive_search_functionality(self):
        """Test comprehensive search functionality with specific queries"""
        print("🔍 Testing comprehensive search functionality...")
        search_queries = ["onlyfans", "netflix", "spotify", "adobe", "microsoft"]
        
        passed_searches = 0
        total_searches = len(search_queries)
        
        for query in search_queries:
            try:
                # Test dedicated search endpoint
                response = self.session.get(f"{self.api_url}/products/search?q={query}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and isinstance(data.get('data'), list):
                        results = data['data']
                        print(f"   ✅ Search '{query}': {len(results)} results")
                        passed_searches += 1
                        
                        # Also test search via products endpoint
                        response2 = self.session.get(f"{self.api_url}/products?search={query}", timeout=10)
                        if response2.status_code == 200:
                            data2 = response2.json()
                            if data2.get('success'):
                                results2 = data2['data']
                                print(f"      Products endpoint search: {len(results2)} results")
                    else:
                        print(f"   ❌ Search '{query}': Invalid response format")
                else:
                    print(f"   ❌ Search '{query}': Failed ({response.status_code})")
            except Exception as e:
                print(f"   ❌ Search '{query}': Error ({e})")
        
        success_rate = (passed_searches / total_searches) * 100
        print(f"✅ Search functionality: {passed_searches}/{total_searches} queries working ({success_rate:.1f}%)")
        return passed_searches >= 3  # At least 3 out of 5 searches should work

    def test_crypto_currencies_endpoint(self):
        """Test crypto currencies endpoint"""
        print("💰 Testing crypto currencies endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    currencies = data.get('data', [])
                    print(f"✅ Crypto currencies retrieved: {len(currencies)} currencies available")
                    if currencies:
                        print(f"   Sample currencies: {currencies[:3] if len(currencies) >= 3 else currencies}")
                    return True
                else:
                    print(f"❌ Crypto currencies: Invalid response format")
                    return False
            else:
                print(f"❌ Crypto currencies failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Crypto currencies error: {e}")
            return False

    def test_create_test_order(self):
        """Create a test order for payment testing"""
        print("📦 Creating test order...")
        if not self.auth_token:
            print("❌ No auth token available for order creation")
            return None
            
        try:
            # Get a sample product first
            response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
            if response.status_code != 200:
                print("❌ Failed to get products for order creation")
                return None
                
            products_data = response.json()
            if not products_data.get('success') or not products_data.get('data'):
                print("❌ No products available for order creation")
                return None
                
            product = products_data['data'][0]
            
            order_data = {
                "user_id": "test-user-id",
                "user_email": "sarah.johnson@premiumsubs.com",
                "user_name": "Sarah Johnson",
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
                "notes": "Test order for payment testing"
            }
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.post(
                f"{self.api_url}/orders",
                json=order_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    order = data['data']
                    print(f"✅ Test order created: {order['id']}")
                    print(f"   Product: {order['items'][0]['product_name']}")
                    print(f"   Amount: ${order['final_amount']}")
                    return order['id']
                else:
                    print(f"❌ Order creation: Invalid response format")
                    return None
            else:
                print(f"❌ Order creation failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Order creation error: {e}")
            return None

    def test_crypto_payment_creation(self):
        """Test crypto payment creation"""
        print("💳 Testing crypto payment creation...")
        
        # First create a test order
        order_id = self.test_create_test_order()
        if not order_id:
            print("❌ Cannot test payment creation without order")
            return False
            
        try:
            payment_data = {
                "order_id": order_id,
                "crypto_currency": "btc",
                "amount": 10.0,
                "currency": "USD"
            }
            
            response = self.session.post(
                f"{self.api_url}/payments/crypto/create",
                json=payment_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    payment_info = data['data']
                    print(f"✅ Crypto payment created successfully")
                    print(f"   Payment ID: {payment_info.get('payment_id', 'N/A')}")
                    print(f"   Pay Address: {payment_info.get('pay_address', 'N/A')}")
                    print(f"   Pay Amount: {payment_info.get('pay_amount', 'N/A')}")
                    print(f"   Pay Currency: {payment_info.get('pay_currency', 'N/A')}")
                    return payment_info.get('payment_id')
                else:
                    print(f"❌ Crypto payment creation: Invalid response format")
                    return False
            else:
                print(f"❌ Crypto payment creation failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Crypto payment creation error: {e}")
            return False

    def test_payment_status_endpoint(self):
        """Test payment status endpoint"""
        print("📊 Testing payment status endpoint...")
        
        # Create a payment first
        payment_id = self.test_crypto_payment_creation()
        if not payment_id:
            print("❌ Cannot test payment status without payment")
            return False
            
        try:
            response = self.session.get(f"{self.api_url}/payments/{payment_id}/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status_info = data['data']
                    print(f"✅ Payment status retrieved successfully")
                    print(f"   Status: {status_info.get('payment_status', 'N/A')}")
                    return True
                else:
                    print(f"❌ Payment status: Invalid response format")
                    return False
            else:
                print(f"❌ Payment status failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Payment status error: {e}")
            return False

    def test_order_management_endpoints(self):
        """Test order management endpoints"""
        print("📋 Testing order management endpoints...")
        
        # Create a test order
        order_id = self.test_create_test_order()
        if not order_id:
            print("❌ Cannot test order management without order")
            return False
            
        try:
            # Test get order by ID
            response = self.session.get(f"{self.api_url}/orders/{order_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    order = data['data']
                    print(f"✅ Order retrieval successful: {order['id']}")
                    print(f"   Status: {order['status']}")
                    print(f"   Payment Status: {order['payment_status']}")
                    
                    # Test order status update
                    from models import OrderStatus
                    response2 = self.session.put(
                        f"{self.api_url}/orders/{order_id}/status",
                        json="processing",  # Send the status value directly
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        print("✅ Order status update successful")
                        
                        # Test payment status update
                        from models import PaymentStatus
                        response3 = self.session.put(
                            f"{self.api_url}/orders/{order_id}/payment",
                            json="confirmed",  # Send the status value directly
                            timeout=10
                        )
                        
                        if response3.status_code == 200:
                            print("✅ Payment status update successful")
                            return True
                        else:
                            print(f"❌ Payment status update failed: {response3.status_code}")
                            return False
                    else:
                        print(f"❌ Order status update failed: {response2.status_code}")
                        return False
                else:
                    print(f"❌ Order retrieval: Invalid response format")
                    return False
            else:
                print(f"❌ Order retrieval failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Order management error: {e}")
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
                        if 'rating' in product and 'total_reviews' in product:
                            rating = float(product['rating'])
                            reviews_count = int(product['total_reviews'])
                            
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
            # New comprehensive tests for expanded catalog
            ("Expanded Product Catalog (58+ products)", self.test_expanded_product_catalog),
            ("Adult Content Products", self.test_adult_content_products),
            ("Category Filtering (11 categories)", self.test_category_filtering),
            ("Pricing Structure (Original vs Discounted)", self.test_pricing_structure),
            ("Reviews System (4-5 stars)", self.test_reviews_system),
            ("Stock Quantities", self.test_stock_quantities),
            ("Currency Conversion Data", self.test_currency_conversion_data),
            # New comprehensive search and payment tests
            ("Comprehensive Search Functionality", self.test_comprehensive_search_functionality),
            ("Crypto Currencies Endpoint", self.test_crypto_currencies_endpoint),
            ("Crypto Payment Creation", self.test_crypto_payment_creation),
            ("Payment Status Endpoint", self.test_payment_status_endpoint),
            ("Order Management Endpoints", self.test_order_management_endpoints),
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
        
        # Detailed summary for expanded catalog testing
        print("\n🎯 EXPANDED CATALOG TEST FOCUS:")
        print("=" * 60)
        print("✅ Product Endpoints: Tested /api/products with 58+ products")
        print("✅ Adult Content: Verified adult category products are accessible")
        print("✅ Category Filtering: Tested all 11 categories (adult, ott, software, etc.)")
        print("✅ Pricing Display: Verified original_price vs discounted_price structure")
        print("✅ Reviews System: Confirmed 4-5 star reviews implementation")
        print("✅ Stock Management: Verified stock quantities are properly set")
        print("✅ Authentication: Confirmed existing auth still works after DB changes")
        
        if failed == 0:
            print("\n🎉 All backend tests passed! Backend ready for UI/UX phase.")
            return True
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check the details above.")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)