from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
from models import *

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
        self.db = self.client[os.environ.get('DB_NAME', 'premium_shop')]
        
    async def close(self):
        self.client.close()
    
    # Product operations
    async def create_product(self, product: ProductCreate) -> Product:
        product_dict = product.dict()
        # Generate slug from name
        product_dict['slug'] = product_dict['name'].lower().replace(' ', '-').replace('/', '-')
        # Calculate discount percentage
        discount_percentage = int(((product_dict['original_price'] - product_dict['discounted_price']) / product_dict['original_price']) * 100)
        product_dict['discount_percentage'] = discount_percentage
        
        product_obj = Product(**product_dict)
        await self.db.products.insert_one(product_obj.dict())
        return product_obj
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        product = await self.db.products.find_one({"id": product_id})
        return Product(**product) if product else None
    
    async def get_product_by_slug(self, slug: str) -> Optional[Product]:
        product = await self.db.products.find_one({"slug": slug})
        return Product(**product) if product else None
    
    async def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[Product]:
        update_data = {k: v for k, v in product_update.dict().items() if v is not None}
        update_data['updated_at'] = datetime.utcnow()
        
        # Recalculate discount percentage if prices are updated
        if 'original_price' in update_data or 'discounted_price' in update_data:
            product = await self.get_product(product_id)
            if product:
                original_price = update_data.get('original_price', product.original_price)
                discounted_price = update_data.get('discounted_price', product.discounted_price)
                update_data['discount_percentage'] = int(((original_price - discounted_price) / original_price) * 100)
        
        result = await self.db.products.update_one(
            {"id": product_id},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        result = await self.db.products.delete_one({"id": product_id})
        return result.deleted_count > 0
    
    async def get_products(self, filters: SearchFilters) -> List[Product]:
        query = {"status": "active"}
        
        if filters.category:
            query["category"] = filters.category
        
        if filters.min_price is not None:
            query["discounted_price"] = {"$gte": filters.min_price}
        
        if filters.max_price is not None:
            if "discounted_price" in query:
                query["discounted_price"]["$lte"] = filters.max_price
            else:
                query["discounted_price"] = {"$lte": filters.max_price}
        
        if filters.rating:
            query["rating"] = {"$gte": filters.rating}
        
        # Add search functionality
        if filters.search:
            search_query = {
                "$or": [
                    {"name": {"$regex": filters.search, "$options": "i"}},
                    {"description": {"$regex": filters.search, "$options": "i"}},
                    {"short_description": {"$regex": filters.search, "$options": "i"}},
                    {"seo_keywords": {"$in": [filters.search]}},
                    {"category": {"$regex": filters.search, "$options": "i"}},
                    {"subcategory": {"$regex": filters.search, "$options": "i"}}
                ]
            }
            query = {"$and": [query, search_query]}
        
        # Sort
        sort_order = -1 if filters.sort_order == "desc" else 1
        sort_field = filters.sort_by
        
        # Pagination
        skip = (filters.page - 1) * filters.per_page
        
        cursor = self.db.products.find(query).sort(sort_field, sort_order).skip(skip).limit(filters.per_page)
        products = await cursor.to_list(length=filters.per_page)
        
        return [Product(**product) for product in products]
    
    async def get_products_count(self, filters: SearchFilters) -> int:
        query = {"status": "active"}
        
        if filters.category:
            query["category"] = filters.category
        
        if filters.min_price is not None:
            query["discounted_price"] = {"$gte": filters.min_price}
        
        if filters.max_price is not None:
            if "discounted_price" in query:
                query["discounted_price"]["$lte"] = filters.max_price
            else:
                query["discounted_price"] = {"$lte": filters.max_price}
        
        if filters.rating:
            query["rating"] = {"$gte": filters.rating}
        
        # Add search functionality
        if filters.search:
            search_query = {
                "$or": [
                    {"name": {"$regex": filters.search, "$options": "i"}},
                    {"description": {"$regex": filters.search, "$options": "i"}},
                    {"short_description": {"$regex": filters.search, "$options": "i"}},
                    {"seo_keywords": {"$in": [filters.search]}},
                    {"category": {"$regex": filters.search, "$options": "i"}},
                    {"subcategory": {"$regex": filters.search, "$options": "i"}}
                ]
            }
            query = {"$and": [query, search_query]}
        
        return await self.db.products.count_documents(query)
    
    async def get_featured_products(self, limit: int = 8) -> List[Product]:
        cursor = self.db.products.find({"is_featured": True, "status": "active"}).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]
    
    async def get_bestseller_products(self, limit: int = 8) -> List[Product]:
        cursor = self.db.products.find({"is_bestseller": True, "status": "active"}).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]
    
    async def search_products(self, query: str, limit: int = 10) -> List[Product]:
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"seo_keywords": {"$in": [query]}}
            ],
            "status": "active"
        }
        
        cursor = self.db.products.find(search_query).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]
    
    # User operations
    async def create_user(self, user: User) -> User:
        user_dict = user.dict()
        await self.db.users.insert_one(user_dict)
        return user
    
    async def get_user(self, user_id: str) -> Optional[User]:
        user = await self.db.users.find_one({"id": user_id})
        return User(**user) if user else None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        user = await self.db.users.find_one({"id": user_id})
        return User(**user) if user else None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.db.users.find_one({"email": email})
        return User(**user) if user else None
    
    # Order operations
    async def create_order(self, order: OrderCreate) -> Order:
        order_dict = order.dict()
        order_dict['final_amount'] = order_dict['total_amount'] - order_dict['discount_amount']
        order_obj = Order(**order_dict)
        await self.db.orders.insert_one(order_obj.dict())
        return order_obj
    
    async def get_order(self, order_id: str) -> Optional[Order]:
        order = await self.db.orders.find_one({"id": order_id})
        if order:
            # Remove MongoDB _id field before creating Pydantic model
            order.pop('_id', None)
            return Order(**order)
        return None
    
    async def get_user_orders(self, user_id: str) -> List[Order]:
        cursor = self.db.orders.find({"user_id": user_id}).sort("created_at", -1)
        orders = await cursor.to_list(length=100)
        for order in orders:
            order.pop('_id', None)
        return [Order(**order) for order in orders]
    
    async def get_orders(self, user_id: Optional[str] = None, limit: int = 50) -> List[Order]:
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        cursor = self.db.orders.find(query).sort("created_at", -1).limit(limit)
        orders = await cursor.to_list(length=limit)
        for order in orders:
            order.pop('_id', None)
        return [Order(**order) for order in orders]
    
    async def update_order_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        await self.db.orders.update_one(
            {"id": order_id},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        return await self.get_order(order_id)
    
    async def update_order_payment_status(self, order_id: str, payment_status: PaymentStatus) -> Optional[Order]:
        await self.db.orders.update_one(
            {"id": order_id},
            {"$set": {"payment_status": payment_status, "updated_at": datetime.utcnow()}}
        )
        return await self.get_order(order_id)
    
    # Review operations
    async def create_review(self, review: ReviewCreate) -> Review:
        review_obj = Review(**review.dict())
        await self.db.reviews.insert_one(review_obj.dict())
        
        # Update product rating
        await self.update_product_rating(review.product_id)
        
        return review_obj
    
    async def get_product_reviews(self, product_id: str, limit: int = 10) -> List[Review]:
        cursor = self.db.reviews.find({"product_id": product_id, "is_approved": True}).sort("created_at", -1).limit(limit)
        reviews = await cursor.to_list(length=limit)
        return [Review(**review) for review in reviews]
    
    async def update_product_rating(self, product_id: str):
        pipeline = [
            {"$match": {"product_id": product_id, "is_approved": True}},
            {"$group": {
                "_id": None,
                "average_rating": {"$avg": "$rating"},
                "total_reviews": {"$sum": 1}
            }}
        ]
        
        result = await self.db.reviews.aggregate(pipeline).to_list(length=1)
        
        if result:
            avg_rating = round(result[0]['average_rating'], 1)
            total_reviews = result[0]['total_reviews']
            
            await self.db.products.update_one(
                {"id": product_id},
                {"$set": {"rating": avg_rating, "total_reviews": total_reviews}}
            )
    
    # Blog operations
    async def create_blog_post(self, blog_post: BlogPostCreate) -> BlogPost:
        blog_dict = blog_post.dict()
        blog_dict['slug'] = blog_dict['title'].lower().replace(' ', '-').replace('/', '-')
        blog_obj = BlogPost(**blog_dict)
        await self.db.blog_posts.insert_one(blog_obj.dict())
        return blog_obj
    
    async def get_blog_post(self, post_id: str) -> Optional[BlogPost]:
        post = await self.db.blog_posts.find_one({"id": post_id})
        return BlogPost(**post) if post else None
    
    async def get_blog_post_by_slug(self, slug: str) -> Optional[BlogPost]:
        post = await self.db.blog_posts.find_one({"slug": slug})
        return BlogPost(**post) if post else None
    
    async def get_blog_posts(self, limit: int = 10, skip: int = 0) -> List[BlogPost]:
        cursor = self.db.blog_posts.find({"is_published": True}).sort("created_at", -1).skip(skip).limit(limit)
        posts = await cursor.to_list(length=limit)
        return [BlogPost(**post) for post in posts]
    
    async def get_featured_blog_posts(self, limit: int = 3) -> List[BlogPost]:
        cursor = self.db.blog_posts.find({"is_featured": True, "is_published": True}).sort("created_at", -1).limit(limit)
        posts = await cursor.to_list(length=limit)
        return [BlogPost(**post) for post in posts]
    
    # Category operations
    async def create_category(self, category: CategoryCreate) -> Category:
        category_dict = category.dict()
        category_dict['slug'] = category_dict['name'].lower().replace(' ', '-').replace('/', '-')
        category_obj = Category(**category_dict)
        await self.db.categories.insert_one(category_obj.dict())
        return category_obj
    
    async def get_categories(self) -> List[Category]:
        cursor = self.db.categories.find({"is_active": True}).sort("sort_order", 1)
        categories = await cursor.to_list(length=100)
        return [Category(**category) for category in categories]
    
    # Newsletter operations
    async def subscribe_newsletter(self, newsletter: NewsletterCreate) -> Newsletter:
        # Check if email already exists
        existing = await self.db.newsletter.find_one({"email": newsletter.email})
        if existing:
            return Newsletter(**existing)
        
        newsletter_obj = Newsletter(**newsletter.dict())
        await self.db.newsletter.insert_one(newsletter_obj.dict())
        return newsletter_obj
    
    # Contact operations
    async def create_contact(self, contact: ContactCreate) -> Contact:
        contact_obj = Contact(**contact.dict())
        await self.db.contacts.insert_one(contact_obj.dict())
        return contact_obj
    
    # Analytics operations
    async def log_analytics(self, analytics: AnalyticsCreate) -> Analytics:
        analytics_obj = Analytics(**analytics.dict())
        await self.db.analytics.insert_one(analytics_obj.dict())
        return analytics_obj
    
    async def get_analytics_stats(self) -> Dict[str, Any]:
        # Get today's stats
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        total_products = await self.db.products.count_documents({"status": "active"})
        total_orders = await self.db.orders.count_documents({})
        total_users = await self.db.users.count_documents({})
        today_visitors = await self.db.analytics.count_documents({"timestamp": {"$gte": today}})
        
        return {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_users": total_users,
            "today_visitors": today_visitors
        }
    
    # Payment operations
    async def create_payment_transaction(self, payment: PaymentCreate) -> PaymentTransaction:
        payment_obj = PaymentTransaction(**payment.dict())
        await self.db.payment_transactions.insert_one(payment_obj.dict())
        return payment_obj
    
    async def get_payment_transaction(self, payment_id: str) -> Optional[PaymentTransaction]:
        payment = await self.db.payment_transactions.find_one({"payment_id": payment_id})
        return PaymentTransaction(**payment) if payment else None
    
    async def get_payment_by_order(self, order_id: str) -> Optional[PaymentTransaction]:
        payment = await self.db.payment_transactions.find_one({"order_id": order_id})
        return PaymentTransaction(**payment) if payment else None
    
    async def update_payment_status(self, payment_id: str, status: PaymentStatus, gateway_response: Optional[Dict] = None) -> Optional[PaymentTransaction]:
        update_data = {"status": status, "updated_at": datetime.utcnow()}
        if gateway_response:
            update_data["gateway_response"] = gateway_response
        
        # Try to find by payment_id first, then by order_id if payment_id is not set yet
        payment = await self.db.payment_transactions.find_one({"payment_id": payment_id})
        if not payment:
            # If not found by payment_id, try to find by order_id and update payment_id
            payment = await self.db.payment_transactions.find_one({"order_id": payment_id})
            if payment:
                update_data["payment_id"] = payment_id
        
        if payment:
            await self.db.payment_transactions.update_one(
                {"id": payment["id"]},
                {"$set": update_data}
            )
            return await self.get_payment_transaction(payment_id)
        
        return None

    async def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """Get a single product by ID"""
        product = await self.db.products.find_one({"id": product_id})
        if product and "_id" in product:
            product.pop("_id")
        return product
    async def get_orders(self, page: int = 1, per_page: int = 20, status_filter: Optional[str] = None) -> List[Dict]:
        """Get orders with pagination and filtering"""
        skip = (page - 1) * per_page
        query = {}
        if status_filter:
            query["status"] = status_filter
        
        cursor = self.db.orders.find(query).sort("created_at", -1).skip(skip).limit(per_page)
        orders = await cursor.to_list(length=per_page)
        
        # Remove _id field and format for frontend
        for order in orders:
            if "_id" in order:
                order.pop("_id")
        
        return orders
    
    async def get_users(self, page: int = 1, per_page: int = 50) -> List[Dict]:
        """Get users with pagination"""
        skip = (page - 1) * per_page
        cursor = self.db.users.find({}, {"password": 0}).sort("created_at", -1).skip(skip).limit(per_page)
        users = await cursor.to_list(length=per_page)
        
        # Remove _id field
        for user in users:
            if "_id" in user:
                user.pop("_id")
        
        return users
    
    async def update_product_stock(self, product_id: str, stock_quantity: int) -> Optional[Dict]:
        """Update product stock quantity"""
        result = await self.db.products.update_one(
            {"id": product_id},
            {"$set": {"stock_quantity": stock_quantity, "updated_at": datetime.utcnow()}}
        )
        if result.modified_count > 0:
            product = await self.db.products.find_one({"id": product_id})
            if product and "_id" in product:
                product.pop("_id")
            return product
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        result = await self.db.products.delete_one({"id": product_id})
        return result.deleted_count > 0
    
    async def bulk_update_stock(self, update_data: Dict) -> int:
        """Bulk update stock for all products"""
        update_data["updated_at"] = datetime.utcnow()
        result = await self.db.products.update_many({}, {"$set": update_data})
        return result.modified_count
    
    async def get_stock_overview(self) -> Dict:
        """Get comprehensive stock overview"""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_products": {"$sum": 1},
                    "in_stock": {"$sum": {"$cond": [{"$gt": ["$stock_quantity", 0]}, 1, 0]}},
                    "out_of_stock": {"$sum": {"$cond": [{"$eq": ["$stock_quantity", 0]}, 1, 0]}},
                    "low_stock_count": {"$sum": {"$cond": [{"$and": [{"$gt": ["$stock_quantity", 0]}, {"$lte": ["$stock_quantity", 10]}]}, 1, 0]}},
                    "total_stock_units": {"$sum": "$stock_quantity"}
                }
            }
        ]
        
        result = await self.db.products.aggregate(pipeline).to_list(1)
        if result:
            data = result[0]
            data.pop("_id", None)
            return data
        
        return {
            "total_products": 0,
            "in_stock": 0,
            "out_of_stock": 0,
            "low_stock_count": 0,
            "total_stock_units": 0
        }
    
    async def get_low_stock_products(self, threshold: int = 10) -> List[Dict]:
        """Get products with low stock"""
        cursor = self.db.products.find(
            {"stock_quantity": {"$lte": threshold, "$gt": 0}},
            {"id": 1, "name": 1, "stock_quantity": 1, "category": 1, "discounted_price": 1, "image_url": 1}
        )
        products = await cursor.to_list(length=100)
        
        # Remove _id field
        for product in products:
            if "_id" in product:
                product.pop("_id")
        
        return products
    
    async def get_dashboard_stats(self) -> Dict:
        """Get comprehensive dashboard statistics"""
        # Get product stats
        total_products = await self.db.products.count_documents({})
        
        # Get order stats
        total_orders = await self.db.orders.count_documents({})
        
        # Get user stats
        total_users = await self.db.users.count_documents({})
        
        # Calculate total revenue (sum of all completed orders)
        revenue_pipeline = [
            {"$match": {"status": {"$in": ["completed", "confirmed"]}}},
            {"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}
        ]
        revenue_result = await self.db.orders.aggregate(revenue_pipeline).to_list(1)
        total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
        
        # Get recent orders (last 5)
        recent_orders_cursor = self.db.orders.find({}).sort("created_at", -1).limit(5)
        recent_orders = await recent_orders_cursor.to_list(5)
        
        # Remove _id field from recent orders
        for order in recent_orders:
            if "_id" in order:
                order.pop("_id")
        
        return {
            "totalRevenue": total_revenue,
            "totalOrders": total_orders,
            "totalProducts": total_products,
            "totalUsers": total_users,
            "recentOrders": recent_orders
        }

    async def save_content_data(self, content_data):
        """Save content management data"""
        try:
            content_data["updated_at"] = datetime.utcnow()
            await self.db.content_management.replace_one(
                {"type": "site_content"}, 
                {**content_data, "type": "site_content"}, 
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving content data: {e}")
            return False

    async def get_content_data(self):
        """Get content management data"""
        try:
            content = await self.db.content_management.find_one({"type": "site_content"})
            if content and "_id" in content:
                content.pop("_id")
            return content
        except Exception as e:
            print(f"Error getting content data: {e}")
            return None

# Global database instance
db = Database()