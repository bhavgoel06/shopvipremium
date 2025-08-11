#!/usr/bin/env python3
"""
Test script to verify frontend can connect to backend
"""
import requests
import time
import json

def test_backend_connection():
    print("🔄 Testing Backend Connection...")
    
    # Test backend directly
    try:
        response = requests.get("http://localhost:8001/api/products", timeout=10)
        print(f"✅ Backend API Status: {response.status_code}")
        data = response.json()
        print(f"✅ Backend API Response: {data.get('total', 0)} products available")
        return True
    except Exception as e:
        print(f"❌ Backend API Error: {str(e)}")
        return False

def test_frontend_loading():
    print("🔄 Testing Frontend Loading...")
    
    # Test if frontend loads
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        print(f"✅ Frontend Status: {response.status_code}")
        if "Shop VIP Premium" in response.text:
            print("✅ Frontend loaded with correct branding")
            return True
        else:
            print("❌ Frontend loaded but missing expected content")
            return False
    except Exception as e:
        print(f"❌ Frontend Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🚀 FRONTEND-BACKEND CONNECTION TEST")
    print("=" * 60)
    
    backend_ok = test_backend_connection()
    frontend_ok = test_frontend_loading()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"Backend API: {'✅ WORKING' if backend_ok else '❌ FAILED'}")
    print(f"Frontend: {'✅ WORKING' if frontend_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 BOTH SERVICES WORKING - Products should be visible!")
        print("💡 If products still not visible, check browser console for CORS/API errors")
    else:
        print("\n🚨 SERVICE ISSUES DETECTED - Products will not be visible")
    
    print("=" * 60)

if __name__ == "__main__":
    main()