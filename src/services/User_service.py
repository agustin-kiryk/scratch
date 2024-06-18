from typing import Optional
from src.models.User_model import User
from src.repositories.User_repository import UserRepository
from src.services.Base_serice import BaseService
from src.utils.utilities import to_dict

class UserService(BaseService[User]):
    def __init__(self):
        super().__init__(UserRepository())

    def find_by_email(self, email: str) -> Optional[User]:
        return self.repository.find_by_email(email)
    
    def find_by_email_dict(self, email: str) -> Optional[dict]:
        user = self.repository.find_by_email(email)
        return to_dict(user) if user else None