from config import db

products_collection = db["products"]

def add_product(name, price, stock):
    product = {"name": name, "price": price, "stock": stock}
    products_collection.insert_one(product)
    return product

def get_all_products():
    return list(products_collection.find({}, {"_id": 0}))
