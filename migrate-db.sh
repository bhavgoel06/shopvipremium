#!/bin/bash

# Database Migration Script for Shop VIP Premium
# Run this on your VPS after the app is set up

echo "🗄️ Setting up Shop VIP Premium database..."

# Create database and basic admin user
mongosh shopvippremium_prod --eval '
// Create admin user for the app
db.createUser({
  user: "shopvippremium",
  pwd: "VIP@dm1n2025!Shop",
  roles: [
    { role: "readWrite", db: "shopvippremium_prod" }
  ]
});

// Create indexes for better performance
db.products.createIndex({ "name": "text", "description": "text", "tags": "text" });
db.products.createIndex({ "category": 1 });
db.products.createIndex({ "created_at": -1 });
db.orders.createIndex({ "user_email": 1 });
db.orders.createIndex({ "created_at": -1 });
db.payments.createIndex({ "order_id": 1 });
db.users.createIndex({ "email": 1 }, { unique: true });

print("✅ Database setup complete!");
'

echo "✅ Database migration complete!"
echo ""
echo "📝 Next steps if you have existing data:"
echo "1. Export from old database: mongodump --db test_database --out /tmp/backup"
echo "2. Import to new database: mongorestore --db shopvippremium_prod /tmp/backup/test_database"