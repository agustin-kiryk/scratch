from flask import Blueprint
from src.services.User_service import UserService
from src.models.User_model import User
from src.controllers.Base_controller import BaseController
from src.Api_response import ApiResponse

class UserController(BaseController[User]):
    def __init__(self):
        super().__init__(UserService(), User)

    def post(self):
        return ApiResponse(message='Method Not Allowed', code=405).to_response()
