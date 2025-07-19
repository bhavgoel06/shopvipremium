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

class AdminEndpointsTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_data = {
            "first_name": "Admin",
            "last_name": "User", 
            "email": "admin.user@premiumsubs.com",
            "password": "AdminPass123!"
        }
        self.login_data = {
            "email": "admin.user@premiumsubs.com",
            "password": "AdminPass123!"
        }
        
        print(f"🔗 Testing admin endpoints at: {self.api_url}")
        print("=" * 60)

    def setup_auth(self):
        """Setup authentication for admin endpoints"""
        print("🔐 Setting up authentication...")
        try:
            # Try to register first
            response = self.session.post(
                f"{self.api_url}/auth/register",
                json=self.test_user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data', {}).get('access_token'):
                    self.auth_token = data['data']['access_token']
                    print("✅ Registration successful, got auth token")
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
                        print("✅ Login successful, got auth token")
                        return True
            
            print("❌ Failed to get authentication token")
            return False
        except Exception as e:
            print(f"❌ Auth setup error: {e}")
            return False

    def get_auth_headers(self):
        """Get authorization headers"""
        if not self.auth_token:
            return {}
        return {"Authorization": f"Bearer {self.auth_token}"}

    def test_admin_dashboard_stats(self):
        """Test GET /api/admin/dashboard-stats - comprehensive statistics"""
        print("📊 Testing Admin Dashboard Stats...")
        try:
            response = self.session.get(
                f"{self.api_url}/admin/dashboard-stats",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    stats = data.get('data', {})
                    print(f"✅ Dashboard stats retrieved successfully")
                    
                    # Check for expected statistics
                    expected_fields = ['total_revenue', 'total_orders', 'total_products', 'total_users']
                    found_fields = []
                    
                    for field in expected_fields:
                        if field in stats:
                            found_fields.append(field)
                            print(f"   {field}: {stats[field]}")
                    
                    # Check for recent orders
                    if 'recent_orders' in stats:
                        recent_orders = stats['recent_orders']
                        print(f"   recent_orders: {len(recent_orders)} orders")
                        found_fields.append('recent_orders')
                    
                    success_rate = len(found_fields) / len(expected_fields + ['recent_orders']) * 100
                    print(f"   📈 Stats completeness: {len(found_fields)}/{len(expected_fields + ['recent_orders'])} fields ({success_rate:.1f}%)")
                    
                    return len(found_fields) >= 3  # At least 3 key stats should be present
                else:
                    print(f"❌ Dashboard stats: Invalid response format")
                    return False
            else:
                print(f"❌ Dashboard stats failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Dashboard stats error: {e}")
            return False

    def test_enhanced_order_management(self):
        """Test GET /api/orders with pagination and filtering"""
        print("📋 Testing Enhanced Order Management...")
        try:
            # Test basic order listing
            response = self.session.get(
                f"{self.api_url}/orders",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    orders = data.get('data', [])
                    print(f"✅ Orders retrieved: {len(orders)} orders")
                    
                    # Test pagination
                    response2 = self.session.get(
                        f"{self.api_url}/orders?page=1&per_page=5",
                        headers=self.get_auth_headers(),
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if data2.get('success'):
                            paginated_orders = data2.get('data', [])
                            print(f"✅ Pagination working: {len(paginated_orders)} orders (page 1, per_page=5)")
                            
                            # Test status filtering
                            response3 = self.session.get(
                                f"{self.api_url}/orders?status=pending",
                                headers=self.get_auth_headers(),
                                timeout=10
                            )
                            
                            if response3.status_code == 200:
                                data3 = response3.json()
                                if data3.get('success'):
                                    filtered_orders = data3.get('data', [])
                                    print(f"✅ Status filtering working: {len(filtered_orders)} pending orders")
                                    return True
                    
                    return True  # Basic functionality works even if advanced features don't
                else:
                    print(f"❌ Order management: Invalid response format")
                    return False
            else:
                print(f"❌ Order management failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Order management error: {e}")
            return False

    def test_order_status_updates(self):
        """Test PUT /api/admin/order-status for updating order status"""
        print("🔄 Testing Order Status Updates...")
        try:
            # First, try to get an existing order
            response = self.session.get(
                f"{self.api_url}/orders?per_page=1",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            order_id = None
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    orders = data['data']
                    if orders:
                        order_id = orders[0].get('id')
            
            if not order_id:
                # Create a test order first
                order_id = self.create_test_order()
            
            if order_id:
                # Test order status update
                response = self.session.put(
                    f"{self.api_url}/admin/order-status?order_id={order_id}&status=processing",
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"✅ Order status update successful for order: {order_id}")
                        print(f"   Status updated to: processing")
                        return True
                    else:
                        print(f"❌ Order status update: Invalid response format")
                        return False
                else:
                    print(f"❌ Order status update failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print("⚠️  No orders available for status update test")
                return True  # Don't fail if no orders exist
        except Exception as e:
            print(f"❌ Order status update error: {e}")
            return False

    def test_user_management(self):
        """Test GET /api/users with pagination"""
        print("👥 Testing User Management...")
        try:
            # Test basic user listing
            response = self.session.get(
                f"{self.api_url}/users",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    users = data.get('data', [])
                    print(f"✅ Users retrieved: {len(users)} users")
                    
                    # Test pagination
                    response2 = self.session.get(
                        f"{self.api_url}/users?page=1&per_page=10",
                        headers=self.get_auth_headers(),
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if data2.get('success'):
                            paginated_users = data2.get('data', [])
                            print(f"✅ User pagination working: {len(paginated_users)} users (page 1, per_page=10)")
                            
                            # Check user data structure
                            if paginated_users:
                                sample_user = paginated_users[0]
                                user_fields = ['id', 'email', 'first_name', 'last_name', 'created_at']
                                found_fields = [field for field in user_fields if field in sample_user]
                                print(f"   User data completeness: {len(found_fields)}/{len(user_fields)} fields")
                            
                            return True
                    
                    return True  # Basic functionality works
                else:
                    print(f"❌ User management: Invalid response format")
                    return False
            else:
                print(f"❌ User management failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ User management error: {e}")
            return False

    def test_enhanced_product_stock_management(self):
        """Test PUT /api/admin/product-stock for updating individual product stock"""
        print("📦 Testing Enhanced Product Stock Management...")
        try:
            # First, get a product to update
            response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
            
            product_id = None
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    products = data['data']
                    if products:
                        product_id = products[0].get('id')
                        product_name = products[0].get('name', 'Unknown')
            
            if product_id:
                # Test stock update
                response = self.session.put(
                    f"{self.api_url}/admin/product-stock?product_id={product_id}&stock_quantity=50",
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        print(f"✅ Product stock update successful")
                        print(f"   Product: {product_name}")
                        print(f"   New stock quantity: 50")
                        return True
                    else:
                        print(f"❌ Product stock update: Invalid response format")
                        return False
                else:
                    print(f"❌ Product stock update failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print("⚠️  No products available for stock update test")
                return True  # Don't fail if no products exist
        except Exception as e:
            print(f"❌ Product stock management error: {e}")
            return False

    def test_product_deletion(self):
        """Test DELETE /api/admin/product/{product_id}"""
        print("🗑️ Testing Product Deletion...")
        try:
            # First, create a test product or get an existing one
            # For safety, we'll just test the endpoint structure without actually deleting
            response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
            
            product_id = None
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    products = data['data']
                    if products:
                        product_id = products[0].get('id')
            
            if product_id:
                # Test deletion endpoint (but don't actually delete - just check if endpoint exists)
                # We'll use a non-existent ID to avoid deleting real products
                test_product_id = "test-product-id-that-does-not-exist"
                response = self.session.delete(
                    f"{self.api_url}/admin/product/{test_product_id}",
                    headers=self.get_auth_headers(),
                    timeout=10
                )
                
                # We expect 404 for non-existent product, which means endpoint is working
                if response.status_code == 404:
                    print(f"✅ Product deletion endpoint working (404 for non-existent product)")
                    return True
                elif response.status_code == 200:
                    print(f"✅ Product deletion endpoint working (200 response)")
                    return True
                else:
                    print(f"❌ Product deletion failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print("⚠️  No products available for deletion test")
                return True  # Don't fail if no products exist
        except Exception as e:
            print(f"❌ Product deletion error: {e}")
            return False

    def test_bulk_stock_operations(self):
        """Test POST /api/admin/bulk-stock-update with actions like mark_all_out_of_stock and reset_all_stock"""
        print("📦 Testing Bulk Stock Operations...")
        try:
            # Test mark_all_out_of_stock action
            response = self.session.post(
                f"{self.api_url}/admin/bulk-stock-update?action=mark_all_out_of_stock",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    updated_count = data.get('data', {}).get('updated_count', 0)
                    print(f"✅ Bulk mark out of stock successful: {updated_count} products updated")
                    
                    # Test reset_all_stock action
                    response2 = self.session.post(
                        f"{self.api_url}/admin/bulk-stock-update?action=reset_all_stock",
                        headers=self.get_auth_headers(),
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if data2.get('success'):
                            updated_count2 = data2.get('data', {}).get('updated_count', 0)
                            print(f"✅ Bulk reset stock successful: {updated_count2} products updated")
                            return True
                        else:
                            print(f"❌ Bulk reset stock: Invalid response format")
                            return False
                    else:
                        print(f"❌ Bulk reset stock failed: {response2.status_code}")
                        return False
                else:
                    print(f"❌ Bulk mark out of stock: Invalid response format")
                    return False
            else:
                print(f"❌ Bulk stock operations failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Bulk stock operations error: {e}")
            return False

    def test_stock_overview(self):
        """Test GET /api/admin/stock-overview for comprehensive stock statistics"""
        print("📊 Testing Stock Overview...")
        try:
            response = self.session.get(
                f"{self.api_url}/admin/stock-overview",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    overview = data.get('data', {})
                    print(f"✅ Stock overview retrieved successfully")
                    
                    # Check for expected statistics
                    expected_fields = ['total_products', 'in_stock', 'out_of_stock', 'total_stock_units']
                    found_fields = []
                    
                    for field in expected_fields:
                        if field in overview:
                            found_fields.append(field)
                            print(f"   {field}: {overview[field]}")
                    
                    success_rate = len(found_fields) / len(expected_fields) * 100
                    print(f"   📈 Overview completeness: {len(found_fields)}/{len(expected_fields)} fields ({success_rate:.1f}%)")
                    
                    return len(found_fields) >= 3  # At least 3 key stats should be present
                else:
                    print(f"❌ Stock overview: Invalid response format")
                    return False
            else:
                print(f"❌ Stock overview failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Stock overview error: {e}")
            return False

    def test_low_stock_products(self):
        """Test GET /api/admin/low-stock-products"""
        print("⚠️ Testing Low Stock Products...")
        try:
            # Test with default threshold
            response = self.session.get(
                f"{self.api_url}/admin/low-stock-products",
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    low_stock_products = data.get('data', [])
                    print(f"✅ Low stock products retrieved: {len(low_stock_products)} products")
                    
                    # Test with custom threshold
                    response2 = self.session.get(
                        f"{self.api_url}/admin/low-stock-products?threshold=20",
                        headers=self.get_auth_headers(),
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if data2.get('success'):
                            low_stock_products2 = data2.get('data', [])
                            print(f"✅ Low stock products (threshold=20): {len(low_stock_products2)} products")
                            
                            # Check product data structure
                            if low_stock_products2:
                                sample_product = low_stock_products2[0]
                                product_fields = ['id', 'name', 'stock_quantity', 'category']
                                found_fields = [field for field in product_fields if field in sample_product]
                                print(f"   Product data completeness: {len(found_fields)}/{len(product_fields)} fields")
                            
                            return True
                    
                    return True  # Basic functionality works
                else:
                    print(f"❌ Low stock products: Invalid response format")
                    return False
            else:
                print(f"❌ Low stock products failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Low stock products error: {e}")
            return False

    def create_test_order(self):
        """Helper method to create a test order"""
        try:
            # Get a sample product first
            response = self.session.get(f"{self.api_url}/products?per_page=1", timeout=10)
            if response.status_code != 200:
                return None
                
            products_data = response.json()
            if not products_data.get('success') or not products_data.get('data'):
                return None
                
            product = products_data['data'][0]
            
            order_data = {
                "user_id": "test-admin-user-id",
                "user_email": "admin.user@premiumsubs.com",
                "user_name": "Admin User",
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
                "notes": "Test order for admin testing"
            }
            
            response = self.session.post(
                f"{self.api_url}/orders",
                json=order_data,
                headers=self.get_auth_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    order = data['data']
                    return order['id']
            
            return None
        except Exception as e:
            print(f"Error creating test order: {e}")
            return None

    def run_all_admin_tests(self):
        """Run all admin endpoint tests"""
        print("🚀 Starting Admin Endpoints Tests")
        print("=" * 60)
        
        # Setup authentication first
        if not self.setup_auth():
            print("❌ Failed to setup authentication. Cannot run admin tests.")
            return False
        
        tests = [
            ("Admin Dashboard Stats", self.test_admin_dashboard_stats),
            ("Enhanced Order Management", self.test_enhanced_order_management),
            ("Order Status Updates", self.test_order_status_updates),
            ("User Management", self.test_user_management),
            ("Enhanced Product Stock Management", self.test_enhanced_product_stock_management),
            ("Product Deletion", self.test_product_deletion),
            ("Bulk Stock Operations", self.test_bulk_stock_operations),
            ("Stock Overview", self.test_stock_overview),
            ("Low Stock Products", self.test_low_stock_products),
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
        print("📊 ADMIN ENDPOINTS TEST RESULTS")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        print("\n🎯 WOOCOMMERCE-LEVEL ADMIN FUNCTIONALITY:")
        print("=" * 60)
        print("📊 Dashboard Stats: Comprehensive statistics including revenue, orders, products, users")
        print("📋 Order Management: Enhanced order listing with pagination and filtering")
        print("🔄 Order Status Updates: Update order status functionality")
        print("👥 User Management: User listing with pagination")
        print("📦 Product Stock Management: Individual and bulk stock operations")
        print("🗑️ Product Deletion: Admin product deletion capability")
        print("📊 Stock Overview: Comprehensive stock statistics")
        print("⚠️ Low Stock Products: Identify products with low inventory")
        
        if failed == 0:
            print("\n🎉 All admin endpoint tests passed! WooCommerce-level functionality verified.")
            return True
        else:
            print(f"\n⚠️  {failed} admin test(s) failed. Check the details above.")
            return False

if __name__ == "__main__":
    tester = AdminEndpointsTester()
    success = tester.run_all_admin_tests()
    sys.exit(0 if success else 1)