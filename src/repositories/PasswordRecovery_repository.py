from datetime import datetime, timedelta
from typing import Optional
from src.models.PasswordRecovery_model import PasswordRecovery
from src.repositories.Base_mongo_repository import BaseRepository


class PasswordRecoveryRepository(BaseRepository[PasswordRecovery]):
    def __init__(self):
        super().__init__(PasswordRecovery)

    def find_by_email(self, email: str) -> Optional[PasswordRecovery]:
        data = self.collection.find_one({'email': email})
        return self.model.from_mongo_dict(data) if data else None

    def delete_by_email(self, email: str) -> None:
        self.collection.delete_one({'email': email})

    def delete_expired_entries(self):
        expiration_time = datetime.utcnow() - timedelta(minutes=15)
        self.collection.delete_many({'created_at': {'$lt': expiration_time}})

    def update_by_valid_code(self, user_id: str, update_data: dict) -> None:
        self.collection.update_one({'user_id': user_id}, {'$set': update_data})
