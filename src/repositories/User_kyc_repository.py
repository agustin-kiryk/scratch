from src.config.mongodb import mongo


class UserKYCRepository:
    def __init__(self):
        self.collection = mongo.db.user_kyc

    def insert(self, user_kyc_data):
        return self.collection.insert_one(user_kyc_data).inserted_id

    def find_by_user_id(self, user_id):
        return self.collection.find_one({"user_id": user_id})

    def update(self, user_id, update_data):
        self.collection.update_one({"user_id": user_id}, {"$set": update_data})

    def insert(self, user_kyc_data):
        return self.collection.insert_one(user_kyc_data).inserted_id
