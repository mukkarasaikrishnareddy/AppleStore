from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "apple_store"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

JWT_SECRET_KEY = "super_secret_key"
