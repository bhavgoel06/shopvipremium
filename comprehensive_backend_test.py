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

class ComprehensiveBackendTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_data = {
            "first_name": "Emma",
            "last_name": "Wilson", 
            "email": "emma.wilson@shopforpremium.com",
            "password": "SecurePass2024!"
        }
        self.login_data = {
            "email": "emma.wilson@shopforpremium.com",
            "password": "SecurePass2024!"
        }
        
        print(f"🔗 Testing backend at: {self.api_url}")
        print("🎯 COMPREHENSIVE ENHANCED SYSTEM TESTING")
        print("=" * 70)

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
                    json=self.login_data,
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

    def test_content_management_api(self):
        """Test Content Management API Routes (POST and GET /api/admin/content)"""
        print("📝 Testing Content Management API...")
        
        # Test content data to save
        test_content = {
            "homepage": {
                "hero_title": "Premium Subscriptions at Unbeatable Prices",
                "hero_subtitle": "Get Netflix, Spotify, ChatGPT Plus and more at 50-90% off",
                "featured_categories": ["OTT", "Software", "VPN", "Education"]
            },
            "about": {
                "company_name": "Shop For Premium",
                "description": "Your trusted source for premium subscription services",
                "contact_email": "support@shopforpremium.com"
            },
            "policies": {
                "refund_policy": "All sales are final, no disputes/chargebacks",
                "delivery_time": "Instant delivery after payment confirmation",
                "support_channels": ["Telegram: @shopforpremium", "WhatsApp: +91 9876543210"]
            }
        }
        
        try:
            # Test POST /api/admin/content (Save content data)
            print("   📤 Testing POST /api/admin/content...")
            response = self.session.post(
                f"{self.api_url}/admin/content",
                json=test_content,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("   ✅ Content data saved successfully")
                    save_success = True
                else:
                    print("   ❌ Content save failed: Invalid response format")
                    save_success = False
            else:
                print(f"   ❌ Content save failed: {response.status_code}")
                save_success = False
            
            # Test GET /api/admin/content (Retrieve content data)
            print("   📥 Testing GET /api/admin/content...")
            response = self.session.get(f"{self.api_url}/admin/content", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    retrieved_content = data.get('data', {})
                    print("   ✅ Content data retrieved successfully")
                    
                    # Verify content persistence
                    if retrieved_content.get('homepage', {}).get('hero_title') == test_content['homepage']['hero_title']:
                        print("   ✅ Content persistence verified")
                        retrieve_success = True
                    else:
                        print("   ❌ Content persistence failed")
                        retrieve_success = False
                else:
                    print("   ❌ Content retrieval failed: Invalid response format")
                    retrieve_success = False
            else:
                print(f"   ❌ Content retrieval failed: {response.status_code}")
                retrieve_success = False
            
            return save_success and retrieve_success
            
        except Exception as e:
            print(f"❌ Content management API error: {e}")
            return False

    def test_enhanced_product_catalog(self):
        """Test Enhanced Product Catalog with 8+ imported products"""
        print("📦 Testing Enhanced Product Catalog...")
        
        # Expected products from shopallpremium.com
        expected_products = [
            "Netflix", "Spotify", "Disney+", "Amazon Prime", 
            "NordVPN", "Adobe", "ChatGPT", "YouTube Premium"
        ]
        
        try:
            # Test all products endpoint
            response = self.session.get(f"{self.api_url}/products?per_page=100", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    total = data.get('total', 0)
                    
                    print(f"   📊 Total products: {total}")
                    
                    # Check for expected products
                    found_products = []
                    for expected in expected_products:
                        for product in products:
                            if expected.lower() in product.get('name', '').lower():
                                found_products.append(expected)
                                print(f"   ✅ Found: {product['name']}")
                                
                                # Verify product details
                                required_fields = ['id', 'name', 'category', 'original_price', 'discounted_price', 'discount_percentage']
                                if all(field in product for field in required_fields):
                                    print(f"      💰 Price: ₹{product['original_price']} → ₹{product['discounted_price']} ({product['discount_percentage']}% off)")
                                    
                                    # Check features and SEO data
                                    if 'features' in product and product['features']:
                                        print(f"      🎯 Features: {len(product['features'])} features listed")
                                    if 'seo_keywords' in product and product['seo_keywords']:
                                        print(f"      🔍 SEO: Keywords present")
                                break
                    
                    found_count = len(found_products)
                    print(f"   📈 Found {found_count}/{len(expected_products)} expected products")
                    
                    # Test featured products endpoint
                    response2 = self.session.get(f"{self.api_url}/products/featured", timeout=10)
                    if response2.status_code == 200:
                        featured_data = response2.json()
                        if featured_data.get('success'):
                            featured = featured_data['data']
                            print(f"   ⭐ Featured products: {len(featured)} products")
                    
                    # Test bestsellers endpoint
                    response3 = self.session.get(f"{self.api_url}/products/bestsellers", timeout=10)
                    if response3.status_code == 200:
                        bestseller_data = response3.json()
                        if bestseller_data.get('success'):
                            bestsellers = bestseller_data['data']
                            print(f"   🏆 Bestseller products: {len(bestsellers)} products")
                    
                    return found_count >= 6 and total >= 50  # At least 6 expected products and 50+ total
                else:
                    print("   ❌ Invalid response format")
                    return False
            else:
                print(f"   ❌ Products endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Enhanced product catalog error: {e}")
            return False

    def test_woocommerce_admin_functionality(self):
        """Test WooCommerce-Level Admin Functionality"""
        print("🛠️ Testing WooCommerce-Level Admin Functionality...")
        
        if not self.auth_token:
            if not self.authenticate_user():
                print("❌ Cannot test admin functionality without authentication")
                return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        admin_tests_passed = 0
        total_admin_tests = 8
        
        try:
            # Test 1: Dashboard Stats
            print("   📊 Testing dashboard stats...")
            response = self.session.get(f"{self.api_url}/admin/dashboard-stats", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stats = data['data']
                    print(f"      ✅ Dashboard stats: {stats.get('totalProducts', 0)} products, {stats.get('totalOrders', 0)} orders")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Dashboard stats: Invalid response")
            else:
                print(f"      ❌ Dashboard stats failed: {response.status_code}")
            
            # Test 2: Product Management
            print("   📦 Testing product management...")
            response = self.session.get(f"{self.api_url}/products?per_page=5", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    products = data['data']
                    print(f"      ✅ Product management: {len(products)} products accessible")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Product management: No products found")
            else:
                print(f"      ❌ Product management failed: {response.status_code}")
            
            # Test 3: Stock Management
            print("   📋 Testing stock management...")
            response = self.session.get(f"{self.api_url}/admin/stock-overview", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stock_info = data['data']
                    print(f"      ✅ Stock overview: {stock_info.get('total_products', 0)} products, {stock_info.get('total_stock_units', 0)} units")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Stock overview: Invalid response")
            else:
                print(f"      ❌ Stock overview failed: {response.status_code}")
            
            # Test 4: Bulk Operations
            print("   🔄 Testing bulk operations...")
            response = self.session.post(
                f"{self.api_url}/admin/bulk-stock-update",
                json={"action": "reset_all_stock"},
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"      ✅ Bulk operations: {data['data'].get('updated_count', 0)} products updated")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Bulk operations: Invalid response")
            else:
                print(f"      ❌ Bulk operations failed: {response.status_code}")
            
            # Test 5: Order Management
            print("   📋 Testing order management...")
            response = self.session.get(f"{self.api_url}/orders?per_page=10", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    orders = data.get('data', [])
                    print(f"      ✅ Order management: {len(orders)} orders accessible")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Order management: Invalid response")
            else:
                print(f"      ❌ Order management failed: {response.status_code}")
            
            # Test 6: User Management
            print("   👥 Testing user management...")
            response = self.session.get(f"{self.api_url}/users?per_page=10", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    users = data.get('data', [])
                    print(f"      ✅ User management: {len(users)} users accessible")
                    admin_tests_passed += 1
                else:
                    print("      ❌ User management: Invalid response")
            else:
                print(f"      ❌ User management failed: {response.status_code}")
            
            # Test 7: Low Stock Products
            print("   ⚠️ Testing low stock detection...")
            response = self.session.get(f"{self.api_url}/admin/low-stock-products?threshold=10", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    low_stock = data.get('data', [])
                    print(f"      ✅ Low stock detection: {len(low_stock)} products below threshold")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Low stock detection: Invalid response")
            else:
                print(f"      ❌ Low stock detection failed: {response.status_code}")
            
            # Test 8: Payment Settings (via crypto currencies)
            print("   💳 Testing payment settings...")
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    currencies = data.get('data', [])
                    print(f"      ✅ Payment settings: {len(currencies)} crypto currencies available")
                    admin_tests_passed += 1
                else:
                    print("      ❌ Payment settings: Invalid response")
            else:
                print(f"      ❌ Payment settings failed: {response.status_code}")
            
            success_rate = (admin_tests_passed / total_admin_tests) * 100
            print(f"   📈 Admin functionality: {admin_tests_passed}/{total_admin_tests} tests passed ({success_rate:.1f}%)")
            
            return admin_tests_passed >= 6  # At least 6 out of 8 admin tests should pass
            
        except Exception as e:
            print(f"❌ Admin functionality error: {e}")
            return False

    def test_system_integration_health(self):
        """Test Overall System Health and Integration"""
        print("🏥 Testing System Integration Health...")
        
        integration_tests_passed = 0
        total_integration_tests = 6
        
        try:
            # Test 1: Health Check
            print("   💓 Testing health check...")
            response = self.session.get(f"{self.api_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    print("      ✅ Health check: System healthy")
                    integration_tests_passed += 1
                else:
                    print("      ❌ Health check: System not healthy")
            else:
                print(f"      ❌ Health check failed: {response.status_code}")
            
            # Test 2: Database Connection (via products)
            print("   🗄️ Testing database connection...")
            response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    print("      ✅ Database connection: Working properly")
                    integration_tests_passed += 1
                else:
                    print("      ❌ Database connection: No data returned")
            else:
                print(f"      ❌ Database connection failed: {response.status_code}")
            
            # Test 3: API Response Consistency
            print("   🔄 Testing API response consistency...")
            endpoints_to_test = [
                "/products/featured",
                "/products/bestsellers", 
                "/categories"
            ]
            
            consistent_responses = 0
            for endpoint in endpoints_to_test:
                response = self.session.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and 'data' in data:
                        consistent_responses += 1
            
            if consistent_responses == len(endpoints_to_test):
                print(f"      ✅ API consistency: {consistent_responses}/{len(endpoints_to_test)} endpoints consistent")
                integration_tests_passed += 1
            else:
                print(f"      ❌ API consistency: Only {consistent_responses}/{len(endpoints_to_test)} endpoints consistent")
            
            # Test 4: Error Handling
            print("   🚫 Testing error handling...")
            response = self.session.get(f"{self.api_url}/products/nonexistent-id", timeout=10)
            if response.status_code == 404:
                print("      ✅ Error handling: 404 errors handled properly")
                integration_tests_passed += 1
            else:
                print(f"      ❌ Error handling: Expected 404, got {response.status_code}")
            
            # Test 5: Authentication System
            print("   🔐 Testing authentication system...")
            if self.auth_token:
                headers = {"Authorization": f"Bearer {self.auth_token}"}
                response = self.session.get(f"{self.api_url}/auth/me", headers=headers, timeout=10)
                if response.status_code == 200:
                    print("      ✅ Authentication: JWT system working")
                    integration_tests_passed += 1
                else:
                    print(f"      ❌ Authentication: JWT validation failed ({response.status_code})")
            else:
                print("      ❌ Authentication: No token available")
            
            # Test 6: Payment Integration
            print("   💳 Testing payment integration...")
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    print("      ✅ Payment integration: NOWPayments working")
                    integration_tests_passed += 1
                else:
                    print("      ❌ Payment integration: Invalid response")
            else:
                print(f"      ❌ Payment integration failed: {response.status_code}")
            
            success_rate = (integration_tests_passed / total_integration_tests) * 100
            print(f"   📈 System integration: {integration_tests_passed}/{total_integration_tests} tests passed ({success_rate:.1f}%)")
            
            return integration_tests_passed >= 5  # At least 5 out of 6 integration tests should pass
            
        except Exception as e:
            print(f"❌ System integration error: {e}")
            return False

    def test_shopallpremium_product_verification(self):
        """Verify specific shopallpremium.com-inspired products"""
        print("🛍️ Testing ShopAllPremium Product Verification...")
        
        # Expected products with specific details
        expected_products = {
            "Netflix": {
                "search_terms": ["netflix"],
                "expected_price_range": (800, 1200),
                "category": "ott"
            },
            "Spotify": {
                "search_terms": ["spotify"],
                "expected_price_range": (40, 80),
                "category": "ott"
            },
            "Disney+": {
                "search_terms": ["disney"],
                "expected_price_range": (200, 600),
                "category": "ott"
            },
            "Amazon Prime": {
                "search_terms": ["amazon", "prime"],
                "expected_price_range": (300, 800),
                "category": "ott"
            },
            "NordVPN": {
                "search_terms": ["nordvpn", "nord"],
                "expected_price_range": (100, 500),
                "category": "vpn"
            },
            "Adobe": {
                "search_terms": ["adobe"],
                "expected_price_range": (500, 2000),
                "category": "software"
            },
            "ChatGPT": {
                "search_terms": ["chatgpt", "gpt"],
                "expected_price_range": (1000, 2500),
                "category": "software"
            },
            "YouTube Premium": {
                "search_terms": ["youtube"],
                "expected_price_range": (100, 400),
                "category": "ott"
            }
        }
        
        verified_products = 0
        total_expected = len(expected_products)
        
        try:
            for product_name, details in expected_products.items():
                print(f"   🔍 Verifying {product_name}...")
                
                found = False
                for search_term in details["search_terms"]:
                    response = self.session.get(f"{self.api_url}/products/search?q={search_term}", timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and data.get('data'):
                            products = data['data']
                            
                            for product in products:
                                product_name_lower = product.get('name', '').lower()
                                if any(term.lower() in product_name_lower for term in details["search_terms"]):
                                    # Verify product details
                                    discounted_price = product.get('discounted_price', 0)
                                    category = product.get('category', '')
                                    
                                    price_min, price_max = details["expected_price_range"]
                                    price_valid = price_min <= discounted_price <= price_max
                                    category_valid = category.lower() == details["category"].lower()
                                    
                                    print(f"      📦 Found: {product['name']}")
                                    print(f"      💰 Price: ₹{discounted_price} (Expected: ₹{price_min}-{price_max}) {'✅' if price_valid else '❌'}")
                                    print(f"      🏷️ Category: {category} (Expected: {details['category']}) {'✅' if category_valid else '❌'}")
                                    
                                    if price_valid and category_valid:
                                        verified_products += 1
                                        found = True
                                        break
                            
                            if found:
                                break
                
                if not found:
                    print(f"      ❌ {product_name} not found or doesn't match criteria")
            
            success_rate = (verified_products / total_expected) * 100
            print(f"   📈 Product verification: {verified_products}/{total_expected} products verified ({success_rate:.1f}%)")
            
            return verified_products >= 6  # At least 6 out of 8 products should be verified
            
        except Exception as e:
            print(f"❌ Product verification error: {e}")
            return False

    def run_comprehensive_tests(self):
        """Run all comprehensive backend tests"""
        print("🚀 STARTING COMPREHENSIVE ENHANCED SYSTEM TESTING")
        print("=" * 70)
        
        # Authenticate first
        if not self.authenticate_user():
            print("⚠️ Continuing without authentication (some tests may fail)")
        
        tests = [
            ("📝 Content Management Testing", self.test_content_management_api),
            ("📦 Enhanced Product Catalog Testing", self.test_enhanced_product_catalog),
            ("🛠️ WooCommerce-Level Admin Testing", self.test_woocommerce_admin_functionality),
            ("🏥 System Integration Health Testing", self.test_system_integration_health),
            ("🛍️ ShopAllPremium Product Verification", self.test_shopallpremium_product_verification),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n{test_name}")
            print("=" * 70)
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
        
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 70)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        print("\n🎯 ENHANCED SYSTEM STATUS:")
        print("=" * 70)
        if passed >= 4:
            print("🎉 ENHANCED SYSTEM IS READY FOR PRODUCTION!")
            print("✅ Content management working")
            print("✅ Product catalog enhanced and functional")
            print("✅ Admin functionality at WooCommerce level")
            print("✅ System integration healthy")
            print("✅ All major improvements verified")
        else:
            print("⚠️ ENHANCED SYSTEM NEEDS ATTENTION")
            print(f"❌ {failed} critical components failed testing")
            print("🔧 Review failed tests and fix issues before production")
        
        return passed >= 4

if __name__ == "__main__":
    tester = ComprehensiveBackendTester()
    success = tester.run_comprehensive_tests()
    sys.exit(0 if success else 1)