import os
import hmac
import hashlib
import json
import requests
from typing import Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NowPaymentsService:
    """Service for integrating with NOWPayments API"""
    
    def __init__(self):
        self.base_url = "https://api.nowpayments.io/v1"
        self.private_key = os.getenv("NOWPAYMENTS_PRIVATE_KEY")
        self.ipn_secret = os.getenv("NOWPAYMENTS_IPN_SECRET")
        self.public_key = os.getenv("NOWPAYMENTS_PUBLIC_KEY")
        
        if not all([self.private_key, self.ipn_secret, self.public_key]):
            raise ValueError("Missing NOWPayments API credentials")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "x-api-key": self.private_key,
            "Content-Type": "application/json"
        }
    
    async def get_available_currencies(self) -> Dict[str, Any]:
        """Get list of available cryptocurrencies"""
        try:
            response = requests.get(f"{self.base_url}/currencies", headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching currencies: {e}")
            raise
    
    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between currencies"""
        try:
            url = f"{self.base_url}/exchange-amount/{from_currency}/{to_currency}?amount=1"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            data = response.json()
            return float(data.get("estimated_amount", 0))
        except Exception as e:
            logger.error(f"Error fetching exchange rate: {e}")
            raise
    
    async def create_payment(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new payment"""
        try:
            payload = {
                "price_amount": order_data["amount"],
                "price_currency": order_data.get("price_currency", "USD"),
                "pay_currency": order_data["crypto_currency"],
                "order_id": order_data["order_id"],
                "order_description": order_data.get("description", "Premium subscription order"),
                "ipn_callback_url": f"{os.getenv('BACKEND_URL', 'https://4e692b72-c7d7-48a0-bbf9-32a02d788f50.preview.emergentagent.com')}/api/payments/nowpayments/ipn",
                "success_url": f"{os.getenv('FRONTEND_URL', 'https://4e692b72-c7d7-48a0-bbf9-32a02d788f50.preview.emergentagent.com')}/order-success",
                "cancel_url": f"{os.getenv('FRONTEND_URL', 'https://4e692b72-c7d7-48a0-bbf9-32a02d788f50.preview.emergentagent.com')}/order-cancelled"
            }
            
            response = requests.post(
                f"{self.base_url}/payment",
                json=payload,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise
    
    async def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status"""
        try:
            response = requests.get(
                f"{self.base_url}/payment/{payment_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting payment status: {e}")
            raise
    
    def validate_ipn_signature(self, payload: Dict[str, Any], signature: str) -> bool:
        """Validate IPN signature using HMAC-SHA512"""
        try:
            # Sort payload keys for consistent signature
            sorted_payload = json.dumps(payload, sort_keys=True)
            computed_signature = hmac.new(
                self.ipn_secret.encode(),
                sorted_payload.encode(),
                hashlib.sha512
            ).hexdigest()
            
            return hmac.compare_digest(computed_signature, signature)
        except Exception as e:
            logger.error(f"Error validating IPN signature: {e}")
            return False
    
    async def process_ipn_callback(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process IPN callback and return order update info"""
        try:
            payment_id = payload.get("payment_id")
            payment_status = payload.get("payment_status")
            order_id = payload.get("order_id")
            
            return {
                "payment_id": payment_id,
                "order_id": order_id,
                "status": payment_status,
                "amount": payload.get("price_amount"),
                "currency": payload.get("price_currency"),
                "crypto_amount": payload.get("pay_amount"),
                "crypto_currency": payload.get("pay_currency"),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing IPN callback: {e}")
            raise

# Global instance
nowpayments_service = NowPaymentsService()