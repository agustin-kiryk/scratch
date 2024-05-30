from src.models.User_model import User
from src.repositories.Base_mongo_repository import BaseRepository
from src.config.mongodb import mongo


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.users)

    def find_by_email(self, email):
        user_data = self.collection.find_one({'email': email})
        return User.from_mongo_dict(user_data) if user_data else None

    def insert(self, user):
        result = self.insert_one(user.to_mongo_dict())
        return str(result.inserted_id)

    def update(self, user):
        self.update_by_id(user.id, user.to_mongo_dict())

    def delete_by_email(self, email):
        self.delete_one({'email': email})
