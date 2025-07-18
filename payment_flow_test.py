#!/usr/bin/env python3

import requests
import json
import sys
import os

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

def test_payment_flow():
    """Test the complete payment flow to identify the exact issue"""
    base_url = get_backend_url()
    if not base_url:
        print("❌ Could not get backend URL")
        return
    
    api_url = f"{base_url}/api"
    session = requests.Session()
    
    print("🔍 DETAILED CRYPTO PAYMENT FLOW ANALYSIS")
    print("=" * 60)
    
    # Step 1: Create order
    print("\n📦 STEP 1: Creating test order...")
    try:
        # Get a product first
        response = session.get(f"{api_url}/products?per_page=1", timeout=10)
        if response.status_code != 200:
            print("❌ Failed to get products")
            return
        
        products_data = response.json()
        product = products_data['data'][0]
        
        order_data = {
            "user_id": "test-user-payment-flow",
            "user_email": "test@paymentflow.com",
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
            "notes": "Payment flow test order"
        }
        
        response = session.post(f"{api_url}/orders", json=order_data, timeout=10)
        
        if response.status_code == 200:
            order = response.json()['data']
            order_id = order['id']
            print(f"✅ Order created: {order_id}")
            print(f"   Amount: ${order['final_amount']}")
        else:
            print(f"❌ Order creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Order creation error: {e}")
        return
    
    # Step 2: Create crypto payment
    print(f"\n💳 STEP 2: Creating crypto payment for order {order_id}...")
    try:
        payment_data = {
            "order_id": order_id,
            "crypto_currency": "btc",
            "amount": 10.0,
            "currency": "USD"
        }
        
        print(f"   Request: POST {api_url}/payments/crypto/create")
        print(f"   Data: {json.dumps(payment_data, indent=2)}")
        
        response = session.post(f"{api_url}/payments/crypto/create", json=payment_data, timeout=15)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200:
            payment_response = response.json()
            if payment_response.get('success'):
                payment_data = payment_response['data']
                payment_id = payment_data.get('payment_id')
                
                print(f"✅ Payment created successfully")
                print(f"   Payment ID: {payment_id}")
                print(f"   Pay Address: {payment_data.get('pay_address')}")
                print(f"   Pay Amount: {payment_data.get('pay_amount')}")
                print(f"   Pay Currency: {payment_data.get('pay_currency')}")
                print(f"   Payment URL: {payment_data.get('payment_url')}")
                
                # Check if this is a mock payment
                if payment_id and payment_id.startswith('mock_payment_'):
                    print(f"⚠️  ISSUE IDENTIFIED: Payment ID is mock: {payment_id}")
                    print("   This suggests the NOWPayments API is not being called properly")
                    print("   or the system is falling back to mock mode")
                
            else:
                print(f"❌ Payment creation failed: Invalid response format")
                return
        else:
            print(f"❌ Payment creation failed: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Payment creation error: {e}")
        return
    
    # Step 3: Test payment status (this is where it fails)
    print(f"\n📊 STEP 3: Testing payment status for {payment_id}...")
    try:
        print(f"   Request: GET {api_url}/payments/{payment_id}/status")
        
        response = session.get(f"{api_url}/payments/{payment_id}/status", timeout=10)
        
        print(f"   Response Status: {response.status_code}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200:
            status_response = response.json()
            print(f"✅ Payment status retrieved successfully")
            print(f"   Status: {status_response.get('data', {}).get('payment_status')}")
        else:
            print(f"❌ Payment status failed: {response.status_code}")
            print("🚨 THIS IS THE ISSUE CAUSING FRONTEND REDIRECT TO FAILED PAGE")
            
            if response.status_code == 500:
                print("   The backend is throwing a 500 error when checking payment status")
                print("   This happens because it's trying to query NOWPayments API with mock payment ID")
                
    except Exception as e:
        print(f"❌ Payment status error: {e}")
    
    # Step 4: Analysis and recommendations
    print(f"\n🔍 ANALYSIS & RECOMMENDATIONS")
    print("=" * 60)
    print("ISSUE IDENTIFIED:")
    print("1. Payment creation works and returns mock payment ID")
    print("2. Payment status check fails with 500 error")
    print("3. This causes frontend to redirect to failed page")
    print("")
    print("ROOT CAUSE:")
    print("- System creates mock payment IDs (mock_payment_xxx)")
    print("- But then tries to query real NOWPayments API with mock ID")
    print("- NOWPayments API returns 400 Bad Request for mock IDs")
    print("- Backend throws 500 error instead of handling gracefully")
    print("")
    print("SOLUTION NEEDED:")
    print("- Handle mock payments properly in payment status endpoint")
    print("- OR ensure real NOWPayments API is called for payment creation")
    print("- OR implement proper error handling for mock payments")

if __name__ == "__main__":
    test_payment_flow()