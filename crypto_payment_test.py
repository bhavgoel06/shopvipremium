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

class CryptoPaymentTester:
    def __init__(self):
        self.base_url = get_backend_url()
        if not self.base_url:
            print("❌ Could not get backend URL from frontend/.env")
            sys.exit(1)
        
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_data = {
            "first_name": "Test",
            "last_name": "User", 
            "email": "testuser@cryptotest.com",
            "password": "TestPass123!"
        }
        self.login_data = {
            "email": "testuser@cryptotest.com",
            "password": "TestPass123!"
        }
        
        print(f"🔗 Testing crypto payment system at: {self.api_url}")
        print("=" * 60)

    def setup_authentication(self):
        """Setup authentication for testing"""
        print("🔐 Setting up authentication...")
        
        # Try to register user first
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
                    print("✅ User registered and authenticated")
                    return True
            elif response.status_code == 400:
                # User exists, try login
                print("⚠️  User exists, trying login...")
                return self.login_user()
        except Exception as e:
            print(f"Registration failed: {e}")
            
        return self.login_user()
    
    def login_user(self):
        """Login existing user"""
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
                    print("✅ User logged in successfully")
                    return True
            
            print(f"❌ Login failed: {response.status_code}")
            return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def test_nowpayments_api_keys(self):
        """Test if NOWPayments API keys are loaded correctly"""
        print("🔑 Testing NOWPayments API keys configuration...")
        
        # Check backend .env file for NOWPayments keys
        try:
            with open('/app/backend/.env', 'r') as f:
                env_content = f.read()
                
            has_private_key = 'NOWPAYMENTS_PRIVATE_KEY' in env_content
            has_public_key = 'NOWPAYMENTS_PUBLIC_KEY' in env_content
            has_ipn_secret = 'NOWPAYMENTS_IPN_SECRET' in env_content
            
            print(f"   Private Key: {'✅ Found' if has_private_key else '❌ Missing'}")
            print(f"   Public Key: {'✅ Found' if has_public_key else '❌ Missing'}")
            print(f"   IPN Secret: {'✅ Found' if has_ipn_secret else '❌ Missing'}")
            
            if has_private_key and has_public_key and has_ipn_secret:
                print("✅ All NOWPayments API keys are configured")
                return True
            else:
                print("❌ Some NOWPayments API keys are missing")
                return False
                
        except Exception as e:
            print(f"❌ Error checking NOWPayments configuration: {e}")
            return False

    def test_crypto_currencies_endpoint(self):
        """Test crypto currencies endpoint"""
        print("💰 Testing crypto currencies endpoint...")
        try:
            response = self.session.get(f"{self.api_url}/payments/crypto/currencies", timeout=15)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Response Data: {json.dumps(data, indent=2)}")
                
                if data.get('success'):
                    currencies = data.get('data', [])
                    print(f"✅ Crypto currencies retrieved: {len(currencies)} currencies available")
                    if currencies:
                        print(f"   Sample currencies: {currencies[:5] if len(currencies) >= 5 else currencies}")
                    return True
                else:
                    print(f"❌ Crypto currencies: Response not successful")
                    return False
            else:
                print(f"❌ Crypto currencies failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Crypto currencies error: {e}")
            return False

    def create_test_order(self):
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
            print(f"   Using product: {product['name']} (${product['discounted_price']})")
            
            order_data = {
                "user_id": "test-user-id",
                "user_email": "testuser@cryptotest.com",
                "user_name": "Test User",
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
                "notes": "Test order for crypto payment testing"
            }
            
            print(f"   Order data: {json.dumps(order_data, indent=2)}")
            
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            response = self.session.post(
                f"{self.api_url}/orders",
                json=order_data,
                headers=headers,
                timeout=10
            )
            
            print(f"   Order creation status: {response.status_code}")
            print(f"   Order creation response: {response.text}")
            
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
                    print(f"   Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Raw response: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Order creation error: {e}")
            return None

    def test_crypto_payment_creation(self, order_id):
        """Test crypto payment creation with detailed analysis"""
        print("💳 Testing crypto payment creation...")
        
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
            
            print(f"   Payment request data: {json.dumps(payment_data, indent=2)}")
            
            response = self.session.post(
                f"{self.api_url}/payments/crypto/create",
                json=payment_data,
                timeout=15
            )
            
            print(f"   Payment creation status: {response.status_code}")
            print(f"   Payment creation headers: {dict(response.headers)}")
            print(f"   Payment creation response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Parsed response: {json.dumps(data, indent=2)}")
                
                if data.get('success'):
                    payment_info = data['data']
                    payment_id = payment_info.get('payment_id')
                    
                    print(f"✅ Crypto payment created successfully")
                    print(f"   Payment ID: {payment_id}")
                    print(f"   Pay Address: {payment_info.get('pay_address', 'N/A')}")
                    print(f"   Pay Amount: {payment_info.get('pay_amount', 'N/A')}")
                    print(f"   Pay Currency: {payment_info.get('pay_currency', 'N/A')}")
                    print(f"   Payment URL: {payment_info.get('payment_url', 'N/A')}")
                    
                    # Verify required fields are present
                    required_fields = ['payment_id', 'pay_address', 'pay_amount', 'pay_currency']
                    missing_fields = [field for field in required_fields if not payment_info.get(field)]
                    
                    if missing_fields:
                        print(f"⚠️  Missing required fields: {missing_fields}")
                        print("❌ Payment response structure incomplete")
                        return False
                    else:
                        print("✅ All required payment fields present")
                        return payment_id if payment_id else f"mock_payment_{order_id}"
                else:
                    print(f"❌ Crypto payment creation: Response not successful")
                    print(f"   Message: {data.get('message', 'No message')}")
                    return False
            else:
                print(f"❌ Crypto payment creation failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error details: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Raw error response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Crypto payment creation error: {e}")
            return False

    def test_payment_status(self, payment_id):
        """Test payment status endpoint"""
        print("📊 Testing payment status endpoint...")
        
        if not payment_id:
            print("❌ Cannot test payment status without payment ID")
            return False
            
        try:
            response = self.session.get(f"{self.api_url}/payments/{payment_id}/status", timeout=10)
            
            print(f"   Payment status request: GET {self.api_url}/payments/{payment_id}/status")
            print(f"   Payment status response code: {response.status_code}")
            print(f"   Payment status response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    status_info = data['data']
                    print(f"✅ Payment status retrieved successfully")
                    print(f"   Status: {status_info.get('payment_status', 'N/A')}")
                    print(f"   Full status info: {json.dumps(status_info, indent=2)}")
                    return True
                else:
                    print(f"❌ Payment status: Response not successful")
                    return False
            else:
                print(f"❌ Payment status failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Payment status error: {e}")
            return False

    def check_nowpayments_service_file(self):
        """Check if nowpayments_service.py exists and is properly configured"""
        print("🔧 Checking NOWPayments service file...")
        
        try:
            service_path = '/app/backend/nowpayments_service.py'
            if os.path.exists(service_path):
                print("✅ nowpayments_service.py file exists")
                
                with open(service_path, 'r') as f:
                    content = f.read()
                    
                # Check for key components
                has_class = 'class' in content and 'NOWPayments' in content
                has_create_payment = 'create_payment' in content
                has_get_currencies = 'get_available_currencies' in content
                has_api_key = 'api_key' in content or 'NOWPAYMENTS_PRIVATE_KEY' in content
                
                print(f"   Has NOWPayments class: {'✅' if has_class else '❌'}")
                print(f"   Has create_payment method: {'✅' if has_create_payment else '❌'}")
                print(f"   Has get_currencies method: {'✅' if has_get_currencies else '❌'}")
                print(f"   Has API key configuration: {'✅' if has_api_key else '❌'}")
                
                return has_class and has_create_payment and has_get_currencies and has_api_key
            else:
                print("❌ nowpayments_service.py file does not exist")
                return False
                
        except Exception as e:
            print(f"❌ Error checking NOWPayments service file: {e}")
            return False

    def run_comprehensive_crypto_test(self):
        """Run comprehensive crypto payment system test"""
        print("🚀 Starting Comprehensive Crypto Payment System Test")
        print("=" * 60)
        
        # Step 1: Setup authentication
        if not self.setup_authentication():
            print("❌ Authentication setup failed - cannot proceed")
            return False
        
        # Step 2: Test NOWPayments configuration
        print("\n" + "=" * 60)
        nowpayments_config_ok = self.test_nowpayments_api_keys()
        
        # Step 3: Check NOWPayments service file
        print("\n" + "=" * 60)
        service_file_ok = self.check_nowpayments_service_file()
        
        # Step 4: Test crypto currencies endpoint
        print("\n" + "=" * 60)
        currencies_ok = self.test_crypto_currencies_endpoint()
        
        # Step 5: Create test order
        print("\n" + "=" * 60)
        order_id = self.create_test_order()
        
        # Step 6: Test crypto payment creation
        print("\n" + "=" * 60)
        payment_id = self.test_crypto_payment_creation(order_id)
        
        # Step 7: Test payment status
        print("\n" + "=" * 60)
        status_ok = self.test_payment_status(payment_id)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 CRYPTO PAYMENT SYSTEM TEST RESULTS")
        print("=" * 60)
        print(f"🔑 NOWPayments Config: {'✅ OK' if nowpayments_config_ok else '❌ FAILED'}")
        print(f"🔧 Service File: {'✅ OK' if service_file_ok else '❌ FAILED'}")
        print(f"💰 Currencies Endpoint: {'✅ OK' if currencies_ok else '❌ FAILED'}")
        print(f"📦 Order Creation: {'✅ OK' if order_id else '❌ FAILED'}")
        print(f"💳 Payment Creation: {'✅ OK' if payment_id else '❌ FAILED'}")
        print(f"📊 Payment Status: {'✅ OK' if status_ok else '❌ FAILED'}")
        
        # Identify the issue
        print("\n🔍 ISSUE ANALYSIS:")
        print("=" * 60)
        
        if not nowpayments_config_ok:
            print("❌ CRITICAL: NOWPayments API keys are not properly configured")
            print("   Check /app/backend/.env for NOWPAYMENTS_PRIVATE_KEY, NOWPAYMENTS_PUBLIC_KEY, NOWPAYMENTS_IPN_SECRET")
        
        if not service_file_ok:
            print("❌ CRITICAL: NOWPayments service file is missing or incomplete")
            print("   The nowpayments_service.py file needs to be properly implemented")
        
        if not currencies_ok:
            print("❌ CRITICAL: Crypto currencies endpoint is failing")
            print("   This suggests NOWPayments service is not working properly")
            print("   Frontend would not be able to get available cryptocurrencies")
        
        if not payment_id:
            print("❌ CRITICAL: Payment creation is failing")
            print("   This is likely why users are being redirected to failed page")
            print("   Frontend expects payment_id, pay_address, pay_amount, pay_currency")
        
        if order_id and not payment_id:
            print("❌ CRITICAL: Order creation works but payment creation fails")
            print("   This indicates the issue is specifically in the payment creation logic")
        
        # Overall result
        all_passed = nowpayments_config_ok and service_file_ok and currencies_ok and order_id and payment_id and status_ok
        
        if all_passed:
            print("\n🎉 All crypto payment tests passed!")
            print("   The crypto payment system should be working correctly")
        else:
            print("\n⚠️  Crypto payment system has issues that need to be fixed")
            print("   This explains why users are being redirected to the failed page")
        
        return all_passed

if __name__ == "__main__":
    tester = CryptoPaymentTester()
    success = tester.run_comprehensive_crypto_test()
    sys.exit(0 if success else 1)