def serialize_user(user):
    """Convert MongoDB user to safe JSON serializable dict"""
    return {
        "id": str(user["_id"]),   # convert ObjectId -> string
        "name": user["name"],
        "email": user["email"]
    }