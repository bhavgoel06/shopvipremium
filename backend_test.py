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