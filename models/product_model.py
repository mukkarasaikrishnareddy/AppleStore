from config import db

products = db.products

def add_product(name, description, price, stock):
    product = {
        "name": name,
        "description": description,
        "price": price,
        "stock": stock
    }
    products.insert_one(product)
    return str(product["_id"])

def get_all_products():
    return list(products.find({}))
