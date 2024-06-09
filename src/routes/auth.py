from flask import Blueprint, jsonify
from src.services.Register_service import test_login, register_new_user2
from flask_jwt_extended import jwt_required, get_jwt_identity

register_blueprint = Blueprint('register', __name__)
auth_blueprint = Blueprint('auth', __name__)


@register_blueprint.route('/', methods=['GET'])
def get_users():
    return 'get all users'


@register_blueprint.route('/', methods=['POST'])
def register_user_app():
    response = register_new_user2()
    return response, 200


@auth_blueprint.route('/login', methods=['POST'])
def login_user_app():
    return test_login()


@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
