from typing import Optional
from config import users_collection
import bcrypt
from bson import ObjectId

def hash_password(plain: str) -> bytes:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())

def check_password(plain: str, hashed: bytes) -> bool:
    try:
        if isinstance(hashed, str):
            hashed = hashed.encode("utf-8")
        return bcrypt.checkpw(plain.encode("utf-8"), hashed)
    except Exception:
        return False

def find_user_by_email(email: str) -> Optional[dict]:
    if not email:
        return None
    return users_collection.find_one({"email": email.lower()})
def create_user(name: str, email: str, password: str) -> dict:
    doc = {
        "name": name,
        "email": email.lower(),
        "password": hash_password(password),
        "role": "customer"
    }
    result = users_collection.insert_one(doc)

    # Attach inserted ID and make sure it is JSON serializable
    doc_copy = {
        "id": str(result.inserted_id),  # convert ObjectId -> string
        "name": name,
        "email": email.lower(),
        "role": "customer"
    }
    return doc_copy