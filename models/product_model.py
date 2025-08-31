from typing import List, Optional
from bson.objectid import ObjectId
from config import products_collection

def serialize_product(doc: Optional[dict]) -> Optional[dict]:
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "brand": doc.get("brand"),
        "price": float(doc.get("price", 0.0)),
        "stock": int(doc.get("stock", 0)),
        "category": doc.get("category"),
        "description": doc.get("description", "")
    }

def list_products(skip=0, limit=20, q: str | None = None) -> List[dict]:
    query = {}
    if q:
        query = {"name": {"$regex": q, "$options": "i"}}
    cursor = products_collection.find(query).skip(skip).limit(limit).sort("name", 1)
    return [serialize_product(p) for p in cursor]

def get_product(product_id: str) -> Optional[dict]:
    try:
        doc = products_collection.find_one({"_id": ObjectId(product_id)})
    except Exception:
        return None
    return serialize_product(doc)

def create_product(data: dict) -> dict:
    doc = {
        "name": data["name"],
        "brand": data.get("brand", "Apple"),
        "price": float(data["price"]),
        "stock": int(data.get("stock", 0)),
        "category": data.get("category", "device"),
        "description": data.get("description", "")
    }
    res = products_collection.insert_one(doc)
    doc["_id"] = res.inserted_id
    return serialize_product(doc)

def update_product(product_id: str, data: dict) -> Optional[dict]:
    update = {}
    for field in ["name", "brand", "price", "stock", "category", "description"]:
        if field in data:
            update[field] = data[field]
    try:
        from pymongo import ReturnDocument
        res = products_collection.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$set": update},
            return_document=ReturnDocument.AFTER
        )
    except Exception:
        return None
    return serialize_product(res) if res else None

def delete_product(product_id: str) -> bool:
    try:
        res = products_collection.delete_one({"_id": ObjectId(product_id)})
        return res.deleted_count == 1
    except Exception:
        return False
