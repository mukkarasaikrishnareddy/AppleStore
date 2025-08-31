import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "apple_store")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections used in Compass
users_collection = db["users"]
products_collection = db["products"]
carts_collection = db["carts"]
orders_collection = db["orders"]
logins_collection = db["logins"]
register_collection = db["register"]
payments_collection = db["payments"]

# Razorpay keys
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
