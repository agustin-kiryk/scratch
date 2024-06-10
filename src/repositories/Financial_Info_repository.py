from src.models.FinancialInfo import FinancialInfo
from src.repositories.Base_mongo_repository import BaseRepository


class FinancialInfoRepository(BaseRepository[FinancialInfo]):
    def __init__(self):
        super().__init__(FinancialInfo)
        
def update_by_user_id(self, user_id: str, update_data: dict) -> None:
     self.collection.update_one({'user_id': user_id}, {'$set': update_data})
