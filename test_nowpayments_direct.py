#!/usr/bin/env python3

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

def test_nowpayments_api():
    """Test NOWPayments API directly to see what's happening"""
    
    print("🔍 TESTING NOWPAYMENTS API DIRECTLY")
    print("=" * 60)
    
    # Get credentials
    private_key = os.getenv("NOWPAYMENTS_PRIVATE_KEY")
    ipn_secret = os.getenv("NOWPAYMENTS_IPN_SECRET")
    public_key = os.getenv("NOWPAYMENTS_PUBLIC_KEY")
    
    print(f"Private Key: {'✅ Found' if private_key else '❌ Missing'}")
    print(f"IPN Secret: {'✅ Found' if ipn_secret else '❌ Missing'}")
    print(f"Public Key: {'✅ Found' if public_key else '❌ Missing'}")
    
    if not all([private_key, ipn_secret, public_key]):
        print("❌ Missing API credentials")
        return
    
    base_url = "https://api.nowpayments.io/v1"
    headers = {
        "x-api-key": private_key,
        "Content-Type": "application/json"
    }
    
    # Test 1: Get currencies
    print(f"\n📋 TEST 1: Get available currencies")
    try:
        response = requests.get(f"{base_url}/currencies", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            currencies = response.json()
            print(f"   ✅ Success: {len(currencies.get('currencies', []))} currencies available")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Create payment
    print(f"\n💳 TEST 2: Create test payment")
    try:
        payload = {
            "price_amount": 10.0,
            "price_currency": "USD",
            "pay_currency": "btc",
            "order_id": "test_order_123",
            "order_description": "Test payment for debugging",
            "ipn_callback_url": "https://1ae160f8-6a16-4ede-86e1-49789e2612e0.preview.emergentagent.com/api/payments/nowpayments/ipn",
            "success_url": "https://1ae160f8-6a16-4ede-86e1-49789e2612e0.preview.emergentagent.com/order-success",
            "cancel_url": "https://1ae160f8-6a16-4ede-86e1-49789e2612e0.preview.emergentagent.com/order-cancelled"
        }
        
        print(f"   Request URL: {base_url}/payment")
        print(f"   Request Headers: {headers}")
        print(f"   Request Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(f"{base_url}/payment", json=payload, headers=headers, timeout=15)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200 or response.status_code == 201:
            payment_data = response.json()
            print(f"   ✅ Payment created successfully")
            print(f"   Payment ID: {payment_data.get('id', 'NOT FOUND')}")
            print(f"   Pay Address: {payment_data.get('pay_address', 'NOT FOUND')}")
            print(f"   Pay Amount: {payment_data.get('pay_amount', 'NOT FOUND')}")
            print(f"   Pay Currency: {payment_data.get('pay_currency', 'NOT FOUND')}")
            
            # Check if 'id' field exists
            if 'id' not in payment_data:
                print(f"   ⚠️  ISSUE: 'id' field missing from response!")
                print(f"   Available fields: {list(payment_data.keys())}")
                
        else:
            print(f"   ❌ Payment creation failed")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Raw error: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
    
    # Test 3: Check API status
    print(f"\n🏥 TEST 3: Check API status")
    try:
        response = requests.get(f"{base_url}/status", headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ API Status: {json.dumps(status_data, indent=2)}")
        else:
            print(f"   ❌ Status check failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_nowpayments_api()