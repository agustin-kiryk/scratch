from src.models.User_model import User
from src.repositories.Base_mongo_repository import BaseRepository
from typing import  Optional


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

