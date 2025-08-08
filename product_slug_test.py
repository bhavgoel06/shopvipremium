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

class ProductSlugTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        
        print(f"🔗 Testing product endpoints at: {self.api_url}")
        print("=" * 60)

    def test_products_list_with_slugs(self):
        """Test GET /api/products - list all products and check if they have slugs"""
        print("📦 Testing GET /api/products - checking for slugs...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=20", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    total = data.get('total', 0)
                    print(f"✅ Products retrieved: {len(products)} products shown, {total} total")
                    
                    # Check for slugs in products
                    products_with_slugs = 0
                    sample_slugs = []
                    
                    for product in products:
                        if 'slug' in product and product['slug']:
                            products_with_slugs += 1
                            if len(sample_slugs) < 5:
                                sample_slugs.append({
                                    'name': product.get('name', 'Unknown'),
                                    'slug': product['slug'],
                                    'id': product.get('id', 'Unknown')
                                })
                    
                    slug_percentage = (products_with_slugs / len(products)) * 100 if products else 0
                    print(f"   📊 Products with slugs: {products_with_slugs}/{len(products)} ({slug_percentage:.1f}%)")
                    
                    if sample_slugs:
                        print("   📝 Sample slugs found:")
                        for sample in sample_slugs:
                            print(f"      • {sample['name']} → slug: '{sample['slug']}'")
                    
                    # Store slugs for further testing
                    self.sample_slugs = sample_slugs
                    
                    return products_with_slugs > 0
                else:
                    print(f"❌ Products endpoint: Invalid response format")
                    return False
            else:
                print(f"❌ Products endpoint failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Products endpoint error: {e}")
            return False

    def test_product_by_slug_routing(self):
        """Test GET /api/products/slug/{slug} - test with different product slugs"""
        print("🔗 Testing GET /api/products/slug/{slug} - slug routing...")
        
        if not hasattr(self, 'sample_slugs') or not self.sample_slugs:
            print("❌ No slugs available from previous test")
            return False
        
        successful_slug_tests = 0
        total_slug_tests = min(len(self.sample_slugs), 5)  # Test up to 5 slugs
        
        for sample in self.sample_slugs[:5]:
            slug = sample['slug']
            expected_name = sample['name']
            
            try:
                response = self.session.get(f"{self.api_url}/products/slug/{slug}", timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        product = data['data']
                        retrieved_name = product.get('name', 'Unknown')
                        
                        print(f"   ✅ Slug '{slug}' → Product: {retrieved_name}")
                        
                        # Verify it's the correct product
                        if retrieved_name == expected_name:
                            print(f"      ✅ Correct product retrieved")
                            successful_slug_tests += 1
                        else:
                            print(f"      ⚠️  Product name mismatch: expected '{expected_name}', got '{retrieved_name}'")
                            successful_slug_tests += 0.5  # Partial credit
                    else:
                        print(f"   ❌ Slug '{slug}': Invalid response format")
                elif response.status_code == 404:
                    print(f"   ❌ Slug '{slug}': Product not found (404)")
                else:
                    print(f"   ❌ Slug '{slug}': Failed ({response.status_code})")
                    try:
                        error_data = response.json()
                        print(f"      Error: {error_data.get('detail', 'Unknown error')}")
                    except:
                        print(f"      Raw response: {response.text}")
            except Exception as e:
                print(f"   ❌ Slug '{slug}': Error ({e})")
        
        success_rate = (successful_slug_tests / total_slug_tests) * 100 if total_slug_tests > 0 else 0
        print(f"✅ Slug routing: {successful_slug_tests}/{total_slug_tests} slugs working ({success_rate:.1f}%)")
        
        return successful_slug_tests >= (total_slug_tests * 0.8)  # 80% success rate required

    def test_currency_conversion_data(self):
        """Test currency conversion by checking product data includes proper pricing fields"""
        print("💱 Testing currency conversion data (USD/INR support)...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=10", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    
                    currency_ready_products = 0
                    sample_pricing = []
                    
                    for product in products:
                        # Check for required pricing fields for currency conversion
                        required_fields = ['original_price', 'discounted_price', 'discount_percentage']
                        
                        if all(field in product and product[field] is not None for field in required_fields):
                            currency_ready_products += 1
                            
                            # Verify pricing data types (should be numbers, not strings)
                            original_price = product['original_price']
                            discounted_price = product['discounted_price']
                            discount_percentage = product['discount_percentage']
                            
                            if len(sample_pricing) < 3:
                                sample_pricing.append({
                                    'name': product.get('name', 'Unknown'),
                                    'original_price': original_price,
                                    'discounted_price': discounted_price,
                                    'discount_percentage': discount_percentage,
                                    'price_types': {
                                        'original': type(original_price).__name__,
                                        'discounted': type(discounted_price).__name__,
                                        'discount': type(discount_percentage).__name__
                                    }
                                })
                    
                    conversion_percentage = (currency_ready_products / len(products)) * 100 if products else 0
                    print(f"   📊 Currency-ready products: {currency_ready_products}/{len(products)} ({conversion_percentage:.1f}%)")
                    
                    if sample_pricing:
                        print("   💰 Sample pricing data:")
                        for sample in sample_pricing:
                            print(f"      • {sample['name']}:")
                            print(f"        Original: {sample['original_price']} ({sample['price_types']['original']})")
                            print(f"        Discounted: {sample['discounted_price']} ({sample['price_types']['discounted']})")
                            print(f"        Discount: {sample['discount_percentage']}% ({sample['price_types']['discount']})")
                            
                            # Test USD to INR conversion calculation (approximate rate: 1 USD = 83 INR)
                            if isinstance(sample['discounted_price'], (int, float)):
                                usd_price = sample['discounted_price']
                                inr_price = usd_price * 83  # Approximate conversion
                                print(f"        USD: ${usd_price:.2f} → INR: ₹{inr_price:.0f}")
                    
                    return conversion_percentage >= 90  # 90% of products should have proper pricing
                else:
                    print(f"❌ Currency test: Invalid response format")
                    return False
            else:
                print(f"❌ Currency test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Currency test error: {e}")
            return False

    def test_product_detail_fields(self):
        """Test that product data includes all necessary fields including valid slugs"""
        print("📋 Testing product detail fields completeness...")
        try:
            response = self.session.get(f"{self.api_url}/products?per_page=15", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    
                    # Define required fields for complete product data
                    required_fields = [
                        'id', 'name', 'slug', 'category', 'description',
                        'original_price', 'discounted_price', 'discount_percentage',
                        'rating', 'total_reviews', 'stock_quantity', 'status'
                    ]
                    
                    complete_products = 0
                    field_statistics = {field: 0 for field in required_fields}
                    slug_quality_issues = []
                    
                    for product in products:
                        product_complete = True
                        
                        for field in required_fields:
                            if field in product and product[field] is not None:
                                field_statistics[field] += 1
                                
                                # Special validation for slug
                                if field == 'slug':
                                    slug = product[field]
                                    if not isinstance(slug, str) or len(slug) < 3:
                                        slug_quality_issues.append({
                                            'name': product.get('name', 'Unknown'),
                                            'slug': slug,
                                            'issue': 'Invalid slug format or too short'
                                        })
                                        product_complete = False
                                    elif ' ' in slug or slug != slug.lower():
                                        slug_quality_issues.append({
                                            'name': product.get('name', 'Unknown'),
                                            'slug': slug,
                                            'issue': 'Slug contains spaces or uppercase letters'
                                        })
                            else:
                                product_complete = False
                        
                        if product_complete:
                            complete_products += 1
                    
                    completeness_rate = (complete_products / len(products)) * 100 if products else 0
                    print(f"   📊 Complete products: {complete_products}/{len(products)} ({completeness_rate:.1f}%)")
                    
                    print("   📋 Field availability:")
                    for field, count in field_statistics.items():
                        percentage = (count / len(products)) * 100 if products else 0
                        status = "✅" if percentage >= 90 else "⚠️" if percentage >= 70 else "❌"
                        print(f"      {status} {field}: {count}/{len(products)} ({percentage:.1f}%)")
                    
                    if slug_quality_issues:
                        print("   ⚠️  Slug quality issues found:")
                        for issue in slug_quality_issues[:3]:  # Show first 3 issues
                            print(f"      • {issue['name']}: '{issue['slug']}' - {issue['issue']}")
                        if len(slug_quality_issues) > 3:
                            print(f"      ... and {len(slug_quality_issues) - 3} more issues")
                    
                    return completeness_rate >= 80  # 80% of products should be complete
                else:
                    print(f"❌ Product fields test: Invalid response format")
                    return False
            else:
                print(f"❌ Product fields test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product fields test error: {e}")
            return False

    def test_404_handling_for_invalid_slugs(self):
        """Test 404 errors for missing products and invalid slugs"""
        print("🚫 Testing 404 handling for invalid slugs...")
        
        invalid_slugs = [
            'non-existent-product',
            'invalid-slug-123',
            'missing-product-slug',
            'test-404-slug'
        ]
        
        correct_404_responses = 0
        total_tests = len(invalid_slugs)
        
        for slug in invalid_slugs:
            try:
                response = self.session.get(f"{self.api_url}/products/slug/{slug}", timeout=10)
                
                if response.status_code == 404:
                    print(f"   ✅ Slug '{slug}': Correctly returns 404")
                    correct_404_responses += 1
                else:
                    print(f"   ❌ Slug '{slug}': Expected 404, got {response.status_code}")
                    if response.status_code == 200:
                        # This would be unexpected - a product was found with this slug
                        data = response.json()
                        if data.get('success') and data.get('data'):
                            product_name = data['data'].get('name', 'Unknown')
                            print(f"      Unexpected: Found product '{product_name}' with slug '{slug}'")
            except Exception as e:
                print(f"   ❌ Slug '{slug}': Error ({e})")
        
        success_rate = (correct_404_responses / total_tests) * 100 if total_tests > 0 else 0
        print(f"✅ 404 handling: {correct_404_responses}/{total_tests} invalid slugs correctly handled ({success_rate:.1f}%)")
        
        return correct_404_responses >= (total_tests * 0.75)  # 75% should return proper 404s

    def test_specific_product_slugs(self):
        """Test specific product slugs that should exist based on common products"""
        print("🎯 Testing specific expected product slugs...")
        
        # Common products that should have slugs
        expected_products = [
            'netflix', 'spotify', 'disney', 'amazon', 'youtube',
            'chatgpt', 'adobe', 'microsoft', 'apple', 'google'
        ]
        
        found_products = 0
        total_searches = len(expected_products)
        
        for product_name in expected_products:
            try:
                # First search for the product
                response = self.session.get(f"{self.api_url}/products/search?q={product_name}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        products = data['data']
                        
                        for product in products:
                            if product_name.lower() in product.get('name', '').lower():
                                slug = product.get('slug')
                                if slug:
                                    # Test if the slug works
                                    slug_response = self.session.get(f"{self.api_url}/products/slug/{slug}", timeout=10)
                                    if slug_response.status_code == 200:
                                        print(f"   ✅ {product_name}: Found '{product['name']}' with working slug '{slug}'")
                                        found_products += 1
                                        break
                                    else:
                                        print(f"   ⚠️  {product_name}: Found '{product['name']}' but slug '{slug}' doesn't work")
                                else:
                                    print(f"   ⚠️  {product_name}: Found '{product['name']}' but no slug")
                                break
                        else:
                            print(f"   ❌ {product_name}: No matching product found in search results")
                    else:
                        print(f"   ❌ {product_name}: Search returned no results")
                else:
                    print(f"   ❌ {product_name}: Search failed ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {product_name}: Error ({e})")
        
        success_rate = (found_products / total_searches) * 100 if total_searches > 0 else 0
        print(f"✅ Specific product slugs: {found_products}/{total_searches} expected products found with working slugs ({success_rate:.1f}%)")
        
        return found_products >= (total_searches * 0.4)  # 40% of common products should be found

    def run_product_slug_tests(self):
        """Run all product slug and currency conversion tests"""
        print("🚀 Starting Product Slug & Currency Conversion Tests")
        print("=" * 60)
        
        tests = [
            ("GET /api/products - List with Slugs", self.test_products_list_with_slugs),
            ("GET /api/products/slug/{slug} - Slug Routing", self.test_product_by_slug_routing),
            ("Currency Conversion Data (USD/INR)", self.test_currency_conversion_data),
            ("Product Detail Fields Completeness", self.test_product_detail_fields),
            ("404 Handling for Invalid Slugs", self.test_404_handling_for_invalid_slugs),
            ("Specific Expected Product Slugs", self.test_specific_product_slugs),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 50)
            try:
                if test_func():
                    passed += 1
                    print(f"✅ {test_name}: PASSED")
                else:
                    failed += 1
                    print(f"❌ {test_name}: FAILED")
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                failed += 1
        
        print("\n" + "=" * 60)
        print("📊 PRODUCT SLUG & CURRENCY TEST RESULTS")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        print("\n🎯 SPECIFIC REVIEW REQUEST RESULTS:")
        print("=" * 60)
        print("1. GET /api/products - List all products and check slugs: TESTED")
        print("2. GET /api/products/slug/{slug} - Test slug routing: TESTED")
        print("3. Currency conversion (USD/INR) data availability: TESTED")
        print("4. Product data completeness including valid slugs: TESTED")
        print("5. 404 error handling for missing products: TESTED")
        
        if failed == 0:
            print("\n🎉 All product slug and currency tests passed!")
            return True
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check the details above.")
            return False

if __name__ == "__main__":
    tester = ProductSlugTester()
    success = tester.run_product_slug_tests()
    sys.exit(0 if success else 1)