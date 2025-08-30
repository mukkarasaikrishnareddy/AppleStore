from config import products_col

sample = [
    {"name": "iPhone 15 Pro", "brand": "Apple", "price": 1299.0, "stock": 20, "category": "phone", "description": "Titanium, A17"},
    {"name": "MacBook Air 13\"", "brand": "Apple", "price": 1099.0, "stock": 15, "category": "laptop", "description": "M3, fanless"},
    {"name": "iPad Air", "brand": "Apple", "price": 699.0, "stock": 25, "category": "tablet", "description": "M2, 11-inch"},
    {"name": "AirPods Pro 2", "brand": "Apple", "price": 249.0, "stock": 50, "category": "audio", "description": "ANC, MagSafe"},
]

if products_col.count_documents({}) == 0:
    products_col.insert_many(sample)
    print("✅ Seed data added!")
else:
    print("Products already exist.")
