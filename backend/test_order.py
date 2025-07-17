import asyncio
from database import db
from models import OrderCreate, ProductResponse

async def test_order_creation():
    """Test order creation"""
    
    # Create a test order
    order_data = OrderCreate(
        user_id="test_user",
        user_email="test@example.com",
        user_name="Test User",
        user_phone="1234567890",
        items=[{
            "product_id": "test_product",
            "product_name": "Test Product",
            "duration": "1 month",
            "quantity": 1,
            "unit_price": 699.0,
            "total_price": 699.0
        }],
        total_amount=699.0,
        payment_method="crypto",
        currency="USD",
        notes="Test order"
    )
    
    try:
        # Create order
        new_order = await db.create_order(order_data)
        print(f"✓ Order created successfully: {new_order.id}")
        print(f"  Total amount: ₹{new_order.total_amount}")
        print(f"  Payment method: {new_order.payment_method}")
        print(f"  Status: {new_order.status}")
        
        return new_order.id
        
    except Exception as e:
        print(f"✗ Error creating order: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_order_creation())