import bcrypt
import json
import secrets

from flask import request, Response, jsonify, current_app
from flask_jwt_extended import create_access_token

from src.client.Twilio_client import send_verification_sms, verify_sms
from src.config_proyect.mongodb import mongo
from src.models.User_model import User
from src.client.Flask_mail_client import send_verification_email, verify_email_code
from datetime import datetime


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
        stored_password = existing_user.get('password')
        if stored_password and verify_password(data.get('password'), stored_password):
            access_token = create_access_token(identity=str(existing_user['_id']))
            return jsonify(access_token=access_token), 200
        return Response(json.dumps({'error': 'Invalid credentials'}), status=401, mimetype='application/json')

    return Response(json.dumps({'error': 'User not found'}), status=404, mimetype='application/json')


def register_new_user2():
    data = request.get_json()
    step = data.get('step')

    if step == 1:
        return handle_step_1(data)
    elif step == 2:
        return handle_step_2(data)
    elif step == 3:
        return handle_step_3(data)
    else:
        response_data = json.dumps({'error': 'Invalid step'})
        return Response(response_data, status=400, mimetype='application/json')


def handle_step_1(data):
    user_email = data.get('email')
    existing_user = mongo.db.users.find_one({'email': user_email})

    if existing_user:
        response_data = json.dumps({'error': 'User already exists'})
        return Response(response_data, status=409, mimetype='application/json')

    phone_number = data.get('phone_number')
    print(phone_number)
    send_verification_sms(phone_number)

    temp_user = {
        'name': data.get('name'),
        'lastName': data.get('lastName'),
        'document': data.get('document'),
        'email': user_email,
        'password': data.get('password'),
        'phone_number': phone_number,
        'phone_verified': False,
        'created_at': datetime.utcnow()
    }
    mongo.db.temp_users.insert_one(temp_user)

    response_data = json.dumps({'message': 'SMS verification code sent'})
    return Response(response_data, status=200, mimetype='application/json')


def handle_step_2(data):
    phone_number = data.get('phone_number')
    sms_code = data.get('sms_code')

    if not phone_number or not sms_code:
        response_data = json.dumps({'error': 'Phone number and SMS code are required'})
        return Response(response_data, status=400, mimetype='application/json')

    if verify_sms(phone_number, str(sms_code)):
        email_verification_code = generate_pin()  # Genera un código de verificación para el email
        send_verification_email(data['email'], email_verification_code)
        mongo.db.temp_users.update_one(
            {'phone_number': phone_number},
            {'$set': {'phone_verified': True, 'email_verification_code': email_verification_code}}
        )

        response_data = json.dumps({'message': 'SMS verified and email verification code sent'})
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response_data = json.dumps({'error': 'Invalid SMS code'})
        return Response(response_data, status=400, mimetype='application/json')


def handle_step_3(data):
    user_email = data.get('email')
    email_code = data.get('email_code')

    temp_user = mongo.db.temp_users.find_one({'email': user_email})

    if temp_user and verify_email_code(email_code, temp_user['email_verification_code']) and temp_user['phone_verified']:
        hashed_password = hash_password(temp_user['password'])
        new_user = build_new_user(temp_user, hashed_password)

        result = mongo.db.users.insert_one(new_user.to_dict())

        if result.inserted_id:
            user_data = build_response(new_user, result)
            mongo.db.temp_users.delete_one({'email': user_email})
            response_data = json.dumps({'user': user_data})
            return Response(response_data, status=200, mimetype='application/json')
        else:
            response_data = json.dumps({'error': 'Failed to register user'})
            return Response(response_data, status=500, mimetype='application/json')
    else:
        response_data = json.dumps({'error': 'Invalid email code or phone not verified'})
        return Response(response_data, status=400, mimetype='application/json')


def hash_password(password):
    hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password_bytes.decode('utf-8')


def build_new_user(temp_user, hashed_password):
    new_user = User(
        id=None,
        name=temp_user['name'],
        lastName=temp_user['lastName'],
        document=temp_user['document'],
        email=temp_user['email'],
        points=0,
        status=1,
        pin=None,
        password=hashed_password
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
        'status': new_user.status
    }
    return user_data


def verify_password(provided_password, stored_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))
