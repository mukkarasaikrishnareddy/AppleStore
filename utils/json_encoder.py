import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)   # convert ObjectId -> string
        return super(JSONEncoder, self).default(obj)