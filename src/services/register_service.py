import bcrypt
import json
import secrets

from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token

from src.config.mongodb import mongo
from src.models.User_model import User


def register_new_user():
    data = request.get_json()

    #Verificar si el usuario ya existe
    user_email = data.get('email', None)
    existing_user = mongo.db.users.find_one({'email': user_email})

    if existing_user:
        response_data = json.dumps({'error': 'User already exists'})
        return Response(response_data, status=409, mimetype='application/json')

    # Crear un objeto de usuario
    gen_pin = generate_pin()
    print('PIN GENERATED:', gen_pin)
    encode_pin = hash_pin(gen_pin)
    new_user = build_new_user(data, encode_pin)

    # Insertar el nuevo usuario en la base de datos
    result = mongo.db.users.insert_one(new_user.to_dict())

    if result.inserted_id:
        user_data = build_response(new_user, result)
        response_data = json.dumps({'user': user_data})
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response_data = json.dumps({'error': 'Failed to register user'})
        return Response(response_data, status=500, mimetype='application/json')


def build_new_user(data, pin):
    new_user = User(
        id=None,
        name=data.get('name', None),
        lastName=data.get('lastName', None),
        document=data.get('document', None),
        email=data.get('email', None),
        points=data.get('points', 0),
        status=1,  # Opcional: asignar un estado por defecto
        pin=pin
    )
    return new_user


def build_response(new_user, result):
    user_id = str(result.inserted_id)
    user_data = {
        'id': user_id,
        'name': new_user.name,
        'lastName': new_user.lastName,
        'document': new_user.document,
        'email': new_user.email,
        'points': new_user.points,
        'status': new_user.status,
        'pin': new_user.pin
    }
    return user_data


def generate_pin():
    return ''.join(secrets.choice('0123456789') for _ in range(4))


def hash_pin(pin):
    hashed_pin_bytes = bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt())
    hashed_pin_str = hashed_pin_bytes.decode('utf-8')  # Convertir bytes a str
    return hashed_pin_str


def verify_pin(provided_pin, stored_pin):
    # Comparar el PIN almacenado decodificado con el PIN proporcionado
    test = bcrypt.checkpw(provided_pin.encode('utf-8'), stored_pin.encode('utf-8'))
    return test


def test_login():
    data = request.get_json()
    existing_user = mongo.db.users.find_one({'email': data.get('email')})

    if existing_user:
        stored_pin = existing_user.get('pin')
        if stored_pin and verify_pin(data.get('pin'), stored_pin):
            access_token = create_access_token(identity=str(existing_user['_id']))
            return jsonify(access_token=access_token), 200
        return Response(json.dumps({'error': 'Invalid credentials'}), status=401, mimetype='application/json')

    return Response(json.dumps({'error': 'User not found'}), status=404, mimetype='application/json')
