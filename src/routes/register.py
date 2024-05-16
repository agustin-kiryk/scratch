from flask import Blueprint, jsonify
from src.services.register_service import register_new_user, test_login

register_blueprint = Blueprint('register', __name__)


@register_blueprint.route('/', methods=['GET'])
def get_users():
    # Aquí deberías implementar la lógica para obtener todos los usuarios
    return 'get all users'


@register_blueprint.route('/', methods=['POST'])
def register_user_app():
    response = register_new_user()
    return response, 200


@register_blueprint.route('/login', methods=['POST'])
def login_user_app():
    response = test_login()
    return response, 200
