from flask import Blueprint
from src.controllers.User_controller import UserController

user_blueprint = Blueprint('user', __name__)

user_view = UserController.as_view('user_api')
user_blueprint.add_url_rule('/users', defaults={'entity_id': None}, view_func=user_view, methods=['GET'])
user_blueprint.add_url_rule('/users/<entity_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])