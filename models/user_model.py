from config import db
import bcrypt
from datetime import datetime

users = db.users

def create_user(full_name, email, password):
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {
        "full_name": full_name,
        "email": email,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    }
    users.insert_one(user)
    return str(user["_id"])

def find_user_by_email(email):
    return users.find_one({"email": email})
