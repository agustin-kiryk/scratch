from typing import Optional

from src.repositories.Base_mongo_repository import BaseRepository
from src.models.Wallet_pc_model import Wallet


class WalletRepository(BaseRepository[Wallet]):
    def __init__(self):
        super().__init__(Wallet)

    def find_by_user_id(self, user_id: str) -> Optional[Wallet]:
        data = self.collection.find_one({'user_id': user_id})
        return self.model.from_mongo_dict(data) if data else None

    def find_by_user_id_and_type(self, user_id: str, wallet_type: str) -> Optional[Wallet]:
        data = self.collection.find_one({'user_id': user_id, 'type': wallet_type})
        return self.model.from_mongo_dict(data) if data else None
