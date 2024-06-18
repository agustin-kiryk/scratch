from flask import Blueprint
from src.services.User_service import UserService
from src.models.User_model import User
from src.controllers.Base_controller import BaseController
from src.utils.Api_response import ApiResponse
from src.errorHandler.error_codes import codes


class UserController(BaseController[User]):
    def __init__(self):
        super().__init__(UserService(), User)

    def post(self):
        return ApiResponse(message='Method Not Allowed', code=codes.METHOD_NOT_ALLOWED).to_response()
