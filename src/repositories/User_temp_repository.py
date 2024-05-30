from bson.objectid import ObjectId
from src.models.Temp_user_model import TempUser
from src.config.mongodb import mongo


class TempUserRepository:
    def __init__(self):
        self.collection = mongo.db.temp_users

    def find_by_id(self, user_id):
        user_data = self.collection.find_one({'_id': ObjectId(user_id)})
        return TempUser.from_mongo_dict(user_data) if user_data else None

    def find_by_email(self, email):
        user_data = self.collection.find_one({'email': email})
        return TempUser.from_mongo_dict(user_data) if user_data else None

    def insert(self, temp_user):
        result = self.collection.insert_one(temp_user.to_mongo_dict())
        return str(result.inserted_id)

    def update(self, temp_user):
        self.collection.update_one({'_id': ObjectId(temp_user.id)}, {'$set': temp_user.to_mongo_dict()})

    def delete_by_email(self, email):
        self.collection.delete_one({'email': email})
