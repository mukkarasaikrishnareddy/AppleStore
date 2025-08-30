from config import db
import bcrypt

users_collection = db["users"]

def create_user(name, email, password):
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {"name": name, "email": email, "password": hashed_pw}
    users_collection.insert_one(user)
    return user

def find_user_by_email(email):
    return users_collection.find_one({"email": email})
