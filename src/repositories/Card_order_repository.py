from src.models.card_order import CardOrder
from src.repositories.Base_mongo_repository import BaseRepository
from src.config.mongodb import mongo


class CardOrderRepository(BaseRepository[CardOrder]):
    def __init__(self):
        super().__init__(CardOrder)

   