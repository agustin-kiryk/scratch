from flask import Blueprint, jsonify
from services.register_service import register_new_user

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/', methods=['GET'])
def get_users():
    # Aquí deberías implementar la lógica para obtener todos los usuarios
    return 'get all users'

@register_blueprint.route('/', methods=['POST'])
def register_user_app():
    # Llama a la función del servicio para registrar un nuevo usuario
    response = register_new_user()
    return response, 200  # Devuelve la respuesta del servicio como JSON con código de estado 200


