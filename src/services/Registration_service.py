import json
from flask import Response
from src.client.Twilio_client import send_verification_sms, verify_sms
from src.client.Flask_mail_client import send_verification_email, verify_email_code
from src.client.Paycaddy_client import create_user
from src.enums.Kyc_enum import CardOrderKycStatus
from src.models.card_order import CardOrder
from src.models.User_model import User
from src.models.Temp_user_model import TempUser
from src.repositories.User_repository import UserRepository
from src.repositories.User_temp_repository import TempUserRepository
import bcrypt
import secrets
from src.config.mongodb import mongo

class RegistrationService:

    @staticmethod
    def handle_step_1(data):
        user_email = data.get('email')
        user_repo = UserRepository()
        temp_user_repo = TempUserRepository()

        existing_user = user_repo.find_by_email(user_email)
        existing_temp_user = temp_user_repo.find_by_email(user_email)

        if existing_user or existing_temp_user:
            response_data = {'error': 'User already exists' if existing_user else 'A user is trying to register with that email'}
            return Response(json.dumps(response_data), status=409, mimetype='application/json')

        phone_number = data.get('phone_number')
        send_verification_sms(phone_number)

        temp_user = TempUser(
            email=user_email,
            phone_number=phone_number,
            verification_code=secrets.token_hex(4)
        )

        temp_user_repo.insert(temp_user)

        response_data = {'message': 'SMS verification code sent'}
        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    @staticmethod
    def handle_step_2(data):
        phone_number = data.get('phone_number')
        sms_code = data.get('sms_code')
        email = data.get('email')

        if not phone_number or not sms_code:
            response_data = {'error': 'Phone number and SMS code are required'}
            return Response(json.dumps(response_data), status=400, mimetype='application/json')

        temp_user_repo = TempUserRepository()
        temp_user = temp_user_repo.find_by_email(email)

        if temp_user:
            if temp_user.phone_verified:
                # Si el teléfono ya está verificado, solo envía el código de verificación por email
                email_verification_code = RegistrationService.generate_pin()
                try:
                    send_verification_email(email, email_verification_code)
                    temp_user.email_verification_code = email_verification_code
                    temp_user_repo.update(temp_user)
                    response_data = {'message': 'Email verification code sent'}
                    return Response(json.dumps(response_data), status=200, mimetype='application/json')
                except Exception as e:
                    response_data = {'error': f'Failed to send verification email: {str(e)}'}
                    return Response(json.dumps(response_data), status=500, mimetype='application/json')
            else:
                # Verifica el estado de la verificación del SMS
                verification_status = verify_sms(phone_number, sms_code)
                if verification_status == 'approved':
                    temp_user.phone_verified = True
                    email_verification_code = RegistrationService.generate_pin()
                    try:
                        send_verification_email(email, email_verification_code)
                        temp_user.email_verification_code = email_verification_code
                        temp_user_repo.update(temp_user)
                        response_data = {'message': 'SMS verified and email verification code sent'}
                        return Response(json.dumps(response_data), status=200, mimetype='application/json')
                    except Exception as e:
                        response_data = {'error': f'Failed to send verification email: {str(e)}'}
                        return Response(json.dumps(response_data), status=500, mimetype='application/json')
                else:
                    response_data = {'error': 'Invalid SMS code or verification not approved'}
                    return Response(json.dumps(response_data), status=400, mimetype='application/json')
        else:
            response_data = {'error': 'Temporary user not found'}
            return Response(json.dumps(response_data), status=404, mimetype='application/json')

    @staticmethod
    def handle_step_3(data):
        user_email = data.get('email')
        email_code = data.get('email_code')

        temp_user_repo = TempUserRepository()
        user_repo = UserRepository()

        temp_user = temp_user_repo.find_by_email(user_email)

        if temp_user and verify_email_code(email_code, temp_user.email_verification_code) and temp_user.phone_verified:
            hashed_password = RegistrationService.hash_password(temp_user.password)
            new_user = RegistrationService.build_new_user(temp_user, hashed_password)

            result = user_repo.insert(new_user)

            if result:
                user_data = RegistrationService.build_response(new_user, result)
                temp_user_repo.delete_by_email(user_email)
                response_data = {'user': user_data}
                return Response(json.dumps(response_data), status=200, mimetype='application/json')
            else:
                response_data = {'error': 'Failed to register user'}
                return Response(json.dumps(response_data), status=500, mimetype='application/json')
        else:
            response_data = {'error': 'Invalid email code or phone not verified'}
            return Response(json.dumps(response_data), status=400, mimetype='application/json')

    @staticmethod
    def handle_step_4(data):
        required_fields = ["email", "firstName", "lastName", "occupation", "placeOfWork", "pep", "salary", "telephone", "address"]
        if not all(field in data for field in required_fields):
            response_data = {'error': 'Missing required fields'}
            return Response(json.dumps(response_data), status=400, mimetype='application/json')

        user_response = create_user(data)

        if 'id' not in user_response:
            response_data = {"error": "Failed to create user in PayCaddy", 'detail': user_response.get('title')}
            return Response(json.dumps(response_data), status=400, mimetype='application/json')

        user_id = str(user_response['id'])

        card_order = CardOrder(user_id=user_id, data=data)
        card_order.walletId = user_response.get('walletId', '')
        card_order.user_id_paycaddy = user_response.get('id', '')
        card_order.kycUrl = user_response.get('kycUrl', '')
        card_order.creationDate = user_response.get('creationDate', '')
        card_order.status = CardOrderKycStatus.PENDING.value

        mongo.db.card_orders.insert_one(card_order.to_dict())
        response_data = RegistrationService.build_response_info_user_and_paycaddy(data, user_response)

        return Response(json.dumps(response_data), status=200, mimetype='application/json')

    @staticmethod
    def generate_pin():
        return ''.join(secrets.choice('0123456789') for _ in range(4))

    @staticmethod
    def hash_password(password):
        hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password_bytes.decode('utf-8')

    @staticmethod
    def build_new_user(temp_user, hashed_password):
        new_user = User(
            name=temp_user.name,
            lastName=temp_user.lastName,
            document=temp_user.document,
            email=temp_user.email,
            points=0,
            status=1,
            pin=None,
            password=hashed_password
        )
        return new_user

    @staticmethod
    def build_response(new_user, result):
        user_id = str(result)
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

    @staticmethod
    def build_response_info_user_and_paycaddy(data, user_response):
        return json.dumps({
            "id": user_response['id'],
            "firstName": data['firstName'],
            "lastName": data['lastName'],
            "email": data['email'],
            "telephone": data['telephone'],
            "placeOfWork": data['placeOfWork'],
            "pep": data['pep'],
            "salary": data['salary'],
            "address": data['address'],
            "isActive": False,
            "walletId": user_response.get('walletId', ''),
            "kycUrl": user_response.get('kycUrl', ''),
            "creationDate": user_response.get('creationDate', '')
        })