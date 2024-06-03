from bson.objectid import ObjectId
from src.models.Temp_user_model import TempUser
from src.config.mongodb import mongo
from src.repositories.Base_mongo_repository import BaseRepository


class TempUserRepository(BaseRepository[TempUser]):
    def __init__(self):
        super().__init__(TempUser)

    def update2(self, temp_user: TempUser) -> None:
        # Converting TempUser instance to dictionary
        update_data = temp_user.to_mongo_dict()
        # Filtering out fields with None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        # Ensuring _id is not part of the update data
        if '_id' in update_data:
            update_data.pop('_id')
        # Performing the update
        self.collection.update_one({'_id': ObjectId(temp_user.id)}, {'$set': update_data})
