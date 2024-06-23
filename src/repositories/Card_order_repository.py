from src.models.card_order import CardOrder
from src.repositories.Base_mongo_repository import BaseRepository
from src.config.mongodb import mongo
from typing import Optional


class CardOrderRepository(BaseRepository[CardOrder]):
    def __init__(self):
        super().__init__(CardOrder)

    def find_by_user_id(self, user_id: str) -> Optional[CardOrder]:
        data = self.collection.find_one({'user_id': user_id})
        return self.model.from_mongo_dict(data) if data else None

    def find_by_user_id_paycaddy(self, user_id: str) -> Optional[CardOrder]:
        data = self.collection.find_one({'user_id_paycaddy': user_id})
        return self.model.from_mongo_dict(data) if data else None

