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

class FocusedBackendTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        
        print(f"🔗 Testing backend at: {self.api_url}")
        print("🎯 FOCUSED TESTING FOR REVIEW REQUEST")
        print("=" * 60)

    def test_pricing_data_types(self):
        """Test that product endpoints return proper pricing data as numbers, not strings"""
        print("💰 Testing PRICING DATA TYPES (numbers, not strings)...")
        try:
            response = self.session.get(f"{self.api_url}/products?limit=10", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    pricing_issues = []
                    valid_pricing = 0
                    
                    for product in products:
                        name = product.get('name', 'Unknown')
                        original_price = product.get('original_price')
                        discounted_price = product.get('discounted_price')
                        discount_percentage = product.get('discount_percentage')
                        
                        # Check if pricing fields are numbers, not strings
                        if isinstance(original_price, (int, float)) and isinstance(discounted_price, (int, float)) and isinstance(discount_percentage, (int, float)):
                            valid_pricing += 1
                            print(f"   ✅ {name}: Original=₹{original_price}, Discounted=₹{discounted_price}, Discount={discount_percentage}%")
                        else:
                            pricing_issues.append({
                                'name': name,
                                'original_price': f"{type(original_price).__name__}: {original_price}",
                                'discounted_price': f"{type(discounted_price).__name__}: {discounted_price}",
                                'discount_percentage': f"{type(discount_percentage).__name__}: {discount_percentage}"
                            })
                    
                    if pricing_issues:
                        print(f"   ❌ PRICING TYPE ISSUES FOUND:")
                        for issue in pricing_issues:
                            print(f"      {issue['name']}:")
                            print(f"        Original: {issue['original_price']}")
                            print(f"        Discounted: {issue['discounted_price']}")
                            print(f"        Discount: {issue['discount_percentage']}")
                    
                    success_rate = (valid_pricing / len(products)) * 100
                    print(f"✅ Pricing Data Types: {valid_pricing}/{len(products)} products have correct number types ({success_rate:.1f}%)")
                    return len(pricing_issues) == 0
                else:
                    print(f"❌ Invalid response format")
                    return False
            else:
                print(f"❌ Products endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Pricing data types test error: {e}")
            return False

    def test_product_variants_specific(self):
        """Test specific product variants for OnlyFans, Netflix, Spotify"""
        print("🔧 Testing PRODUCT VARIANTS (OnlyFans, Netflix, Spotify)...")
        
        # Expected variants for specific products
        expected_variants = {
            "onlyfans": {
                "search_terms": ["onlyfans"],
                "expected_balance_options": ["$100", "$200", "$10", "$25", "$50"],
                "description": "OnlyFans should have balance options like $100, $200"
            },
            "netflix": {
                "search_terms": ["netflix"],
                "expected_screen_options": ["1 Screen", "2 Screens", "4 Screens", "Mobile Only", "4K"],
                "description": "Netflix should have screen options"
            },
            "spotify": {
                "search_terms": ["spotify"],
                "expected_duration_options": ["1 month", "3 months", "6 months", "1 year", "Individual", "Family"],
                "description": "Spotify should have duration options"
            }
        }
        
        variants_correct = 0
        total_products = len(expected_variants)
        
        for product_key, variant_info in expected_variants.items():
            try:
                # Search for the product
                found_product = None
                for search_term in variant_info["search_terms"]:
                    response = self.session.get(f"{self.api_url}/products/search?q={search_term}", timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success') and data.get('data'):
                            products = data['data']
                            
                            # Find the specific product
                            for product in products:
                                product_name = product.get('name', '').lower()
                                if product_key in product_name:
                                    found_product = product
                                    break
                            
                            if found_product:
                                break
                
                if found_product:
                    print(f"   📦 {found_product['name']}:")
                    print(f"      {variant_info['description']}")
                    
                    # Check variants/duration options
                    variants = found_product.get('variants', [])
                    duration_options = found_product.get('duration_options', [])
                    
                    available_options = []
                    if variants:
                        if isinstance(variants, list):
                            for v in variants:
                                if isinstance(v, dict):
                                    available_options.append(v.get('name', ''))
                                elif isinstance(v, str):
                                    available_options.append(v)
                    if duration_options:
                        available_options.extend(duration_options)
                    
                    print(f"      Available options: {available_options}")
                    
                    # Check for expected options based on product type
                    expected_options = []
                    if product_key == "onlyfans":
                        expected_options = variant_info["expected_balance_options"]
                    elif product_key == "netflix":
                        expected_options = variant_info["expected_screen_options"]
                    elif product_key == "spotify":
                        expected_options = variant_info["expected_duration_options"]
                    
                    # Check if any expected options are present
                    options_found = 0
                    for expected_option in expected_options:
                        if any(expected_option.lower() in option.lower() for option in available_options):
                            options_found += 1
                    
                    if options_found > 0:
                        print(f"      ✅ Found {options_found}/{len(expected_options)} expected options")
                        variants_correct += 1
                    else:
                        print(f"      ❌ No expected options found")
                        print(f"      Expected: {expected_options}")
                else:
                    print(f"   ❌ {product_key}: Product not found in search results")
            except Exception as e:
                print(f"   ❌ {product_key}: Error ({e})")
        
        success_rate = (variants_correct / total_products) * 100
        print(f"✅ Product Variants: {variants_correct}/{total_products} products have correct variants ({success_rate:.1f}%)")
        return variants_correct >= 2  # At least 2 out of 3 should have correct variants

    def test_adult_content_not_featured(self):
        """Test that adult products are NOT marked as featured or bestseller"""
        print("🔞 Testing ADULT CONTENT NOT FEATURED/BESTSELLER...")
        
        adult_in_featured = 0
        adult_in_bestsellers = 0
        
        try:
            # Test featured products
            response = self.session.get(f"{self.api_url}/products/featured", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    featured_products = data['data']
                    adult_in_featured = sum(1 for p in featured_products if p.get('category') == 'adult')
                    
                    print(f"   📊 Featured products: {len(featured_products)} total, {adult_in_featured} adult")
                    if adult_in_featured > 0:
                        adult_featured_names = [p.get('name', 'Unknown') for p in featured_products if p.get('category') == 'adult']
                        print(f"      ❌ Adult products in featured: {adult_featured_names}")
                    else:
                        print(f"      ✅ No adult products in featured")
            
            # Test bestseller products
            response = self.session.get(f"{self.api_url}/products/bestsellers", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    bestseller_products = data['data']
                    adult_in_bestsellers = sum(1 for p in bestseller_products if p.get('category') == 'adult')
                    
                    print(f"   📊 Bestseller products: {len(bestseller_products)} total, {adult_in_bestsellers} adult")
                    if adult_in_bestsellers > 0:
                        adult_bestseller_names = [p.get('name', 'Unknown') for p in bestseller_products if p.get('category') == 'adult']
                        print(f"      ❌ Adult products in bestsellers: {adult_bestseller_names}")
                    else:
                        print(f"      ✅ No adult products in bestsellers")
            
            total_adult_prominent = adult_in_featured + adult_in_bestsellers
            print(f"✅ Adult Content Check: {total_adult_prominent} adult products in featured/bestsellers (should be 0)")
            return total_adult_prominent == 0
            
        except Exception as e:
            print(f"❌ Adult content test error: {e}")
            return False

    def test_featured_products_non_adult_only(self):
        """Test that featured products endpoint returns non-adult products only"""
        print("⭐ Testing FEATURED PRODUCTS (non-adult only)...")
        try:
            response = self.session.get(f"{self.api_url}/products/featured", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    featured_products = data['data']
                    non_adult_count = 0
                    adult_count = 0
                    
                    print(f"   📊 Featured products analysis:")
                    for product in featured_products:
                        category = product.get('category', 'unknown')
                        name = product.get('name', 'Unknown')
                        
                        if category == 'adult':
                            adult_count += 1
                            print(f"      ❌ ADULT: {name} (category: {category})")
                        else:
                            non_adult_count += 1
                            print(f"      ✅ NON-ADULT: {name} (category: {category})")
                    
                    print(f"   📈 Summary: {non_adult_count} non-adult, {adult_count} adult products")
                    print(f"✅ Featured Products: {adult_count == 0} (should have 0 adult products)")
                    return adult_count == 0
                else:
                    print(f"❌ Invalid response format")
                    return False
            else:
                print(f"❌ Featured products failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Featured products test error: {e}")
            return False

    def test_bestseller_products_non_adult_only(self):
        """Test that bestseller products endpoint returns non-adult products only"""
        print("🏆 Testing BESTSELLER PRODUCTS (non-adult only)...")
        try:
            response = self.session.get(f"{self.api_url}/products/bestsellers", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    bestseller_products = data['data']
                    non_adult_count = 0
                    adult_count = 0
                    
                    print(f"   📊 Bestseller products analysis:")
                    for product in bestseller_products:
                        category = product.get('category', 'unknown')
                        name = product.get('name', 'Unknown')
                        
                        if category == 'adult':
                            adult_count += 1
                            print(f"      ❌ ADULT: {name} (category: {category})")
                        else:
                            non_adult_count += 1
                            print(f"      ✅ NON-ADULT: {name} (category: {category})")
                    
                    print(f"   📈 Summary: {non_adult_count} non-adult, {adult_count} adult products")
                    print(f"✅ Bestseller Products: {adult_count == 0} (should have 0 adult products)")
                    return adult_count == 0
                else:
                    print(f"❌ Invalid response format")
                    return False
            else:
                print(f"❌ Bestseller products failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Bestseller products test error: {e}")
            return False

    def test_product_descriptions_shopallpremium(self):
        """Test that key products have updated descriptions matching shopallpremium.com"""
        print("📝 Testing PRODUCT DESCRIPTIONS (shopallpremium.com match)...")
        
        # Key products to check descriptions
        key_products = ["onlyfans", "netflix", "spotify"]
        descriptions_updated = 0
        
        for product_key in key_products:
            try:
                response = self.session.get(f"{self.api_url}/products/search?q={product_key}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        products = data['data']
                        
                        # Find the specific product
                        found_product = None
                        for product in products:
                            product_name = product.get('name', '').lower()
                            if product_key in product_name:
                                found_product = product
                                break
                        
                        if found_product:
                            name = found_product.get('name', 'Unknown')
                            description = found_product.get('description', '')
                            short_description = found_product.get('short_description', '')
                            
                            print(f"   📦 {name}:")
                            print(f"      Description length: {len(description)} chars")
                            print(f"      Short description: {short_description[:100]}...")
                            
                            # Check if description is substantial and not generic
                            if len(description) > 50 and 'premium' in description.lower():
                                descriptions_updated += 1
                                print(f"      ✅ Description appears updated and substantial")
                            else:
                                print(f"      ❌ Description appears generic or too short")
                        else:
                            print(f"   ❌ {product_key}: Product not found")
                    else:
                        print(f"   ❌ {product_key}: Search failed or no results")
                else:
                    print(f"   ❌ {product_key}: Search endpoint failed ({response.status_code})")
            except Exception as e:
                print(f"   ❌ {product_key}: Error ({e})")
        
        success_rate = (descriptions_updated / len(key_products)) * 100
        print(f"✅ Product Descriptions: {descriptions_updated}/{len(key_products)} products have updated descriptions ({success_rate:.1f}%)")
        return descriptions_updated >= 2  # At least 2 out of 3 should have updated descriptions

    def test_first_10_products_structure(self):
        """Test first 10 products for complete data structure"""
        print("📋 Testing FIRST 10 PRODUCTS structure...")
        try:
            response = self.session.get(f"{self.api_url}/products?limit=10", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and isinstance(data.get('data'), list):
                    products = data['data']
                    
                    print(f"   📊 Analyzing first {len(products)} products:")
                    complete_products = 0
                    
                    for i, product in enumerate(products, 1):
                        name = product.get('name', 'Unknown')
                        category = product.get('category', 'unknown')
                        original_price = product.get('original_price')
                        discounted_price = product.get('discounted_price')
                        discount_percentage = product.get('discount_percentage')
                        
                        # Check completeness
                        required_fields = ['id', 'name', 'category', 'original_price', 'discounted_price', 'discount_percentage']
                        has_all_fields = all(field in product for field in required_fields)
                        
                        if has_all_fields:
                            complete_products += 1
                            print(f"      {i}. ✅ {name} ({category}) - ₹{original_price}→₹{discounted_price} ({discount_percentage}%)")
                        else:
                            missing_fields = [field for field in required_fields if field not in product]
                            print(f"      {i}. ❌ {name} - Missing: {missing_fields}")
                    
                    completeness_rate = (complete_products / len(products)) * 100
                    print(f"✅ First 10 Products: {complete_products}/{len(products)} complete ({completeness_rate:.1f}%)")
                    return completeness_rate >= 90
                else:
                    print(f"❌ Invalid response format")
                    return False
            else:
                print(f"❌ Products endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ First 10 products test error: {e}")
            return False

    def test_specific_product_searches(self):
        """Test searches for specific products: OnlyFans, Netflix, Spotify"""
        print("🔍 Testing SPECIFIC PRODUCT SEARCHES...")
        
        search_queries = ["OnlyFans", "Netflix", "Spotify"]
        successful_searches = 0
        
        for query in search_queries:
            try:
                response = self.session.get(f"{self.api_url}/products/search?q={query}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and isinstance(data.get('data'), list):
                        results = data['data']
                        
                        if len(results) > 0:
                            successful_searches += 1
                            print(f"   ✅ '{query}': {len(results)} results found")
                            
                            # Show first result details
                            first_result = results[0]
                            name = first_result.get('name', 'Unknown')
                            category = first_result.get('category', 'unknown')
                            price = first_result.get('discounted_price', 0)
                            print(f"      Top result: {name} ({category}) - ₹{price}")
                        else:
                            print(f"   ❌ '{query}': No results found")
                    else:
                        print(f"   ❌ '{query}': Invalid response format")
                else:
                    print(f"   ❌ '{query}': Search failed ({response.status_code})")
            except Exception as e:
                print(f"   ❌ '{query}': Error ({e})")
        
        success_rate = (successful_searches / len(search_queries)) * 100
        print(f"✅ Specific Searches: {successful_searches}/{len(search_queries)} searches successful ({success_rate:.1f}%)")
        return successful_searches >= 2  # At least 2 out of 3 searches should work

    def run_focused_tests(self):
        """Run focused tests for the review request"""
        print("🎯 FOCUSED BACKEND TESTING FOR REVIEW REQUEST")
        print("=" * 60)
        
        tests = [
            ("💰 PRICING DATA (numbers, not strings)", self.test_pricing_data_types),
            ("🔧 PRODUCT VARIANTS (OnlyFans, Netflix, Spotify)", self.test_product_variants_specific),
            ("🔞 ADULT CONTENT NOT FEATURED", self.test_adult_content_not_featured),
            ("⭐ FEATURED PRODUCTS (non-adult only)", self.test_featured_products_non_adult_only),
            ("🏆 BESTSELLER PRODUCTS (non-adult only)", self.test_bestseller_products_non_adult_only),
            ("📝 PRODUCT DESCRIPTIONS (shopallpremium match)", self.test_product_descriptions_shopallpremium),
            ("📋 FIRST 10 PRODUCTS structure", self.test_first_10_products_structure),
            ("🔍 SPECIFIC PRODUCT SEARCHES", self.test_specific_product_searches),
        ]
        
        passed = 0
        failed = 0
        critical_issues = []
        
        for test_name, test_func in tests:
            print(f"\n{test_name}")
            print("-" * 50)
            try:
                if test_func():
                    passed += 1
                    print(f"✅ PASSED: {test_name}")
                else:
                    failed += 1
                    critical_issues.append(test_name)
                    print(f"❌ FAILED: {test_name}")
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                failed += 1
                critical_issues.append(f"{test_name} (CRASHED)")
        
        print("\n" + "=" * 60)
        print("📊 FOCUSED TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for issue in critical_issues:
                print(f"   ❌ {issue}")
        
        print(f"\n🎯 REVIEW REQUEST VERIFICATION:")
        print("=" * 60)
        print("1. PRICING DATA: Verified number types vs strings")
        print("2. PRODUCT VARIANTS: Checked OnlyFans, Netflix, Spotify variants")
        print("3. ADULT CONTENT: Verified not in featured/bestsellers")
        print("4. FEATURED PRODUCTS: Confirmed non-adult only")
        print("5. BESTSELLER PRODUCTS: Confirmed non-adult only")
        print("6. PRODUCT DESCRIPTIONS: Checked shopallpremium.com match")
        
        return passed, failed, critical_issues

if __name__ == "__main__":
    tester = FocusedBackendTester()
    passed, failed, issues = tester.run_focused_tests()
    sys.exit(0 if failed == 0 else 1)