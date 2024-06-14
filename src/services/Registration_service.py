import json
from datetime import datetime

from flask import Response
from src.Api_response import ApiResponse
from src.client.Twilio_client import send_verification_sms, verify_sms
from src.client.Flask_mail_client import send_verification_email, verify_email_code
from src.client.Paycaddy_client import create_user_paycaddy
from src.enums.Kyc_enum import CardOrderKycStatus
from src.models.PaycaddyUser import PayCaddyAddress, PayCaddyUser
from src.models.card_order import CardOrder
from src.models.User_model import User
from src.models.Temp_user_model import TempUser
from src.repositories.User_repository import UserRepository
from src.repositories.User_temp_repository import TempUserRepository
import bcrypt
import secrets
from src.config.mongodb import mongo
from pydantic import Field, ValidationError
from src.models.Financial_info import FinancialInfo
from src.repositories.Financial_Info_repository import FinancialInfoRepository


class RegistrationService:

    @staticmethod
    def handle_step_1(data):
        required_fields = ['name', 'lastName', 'livePanama', 'birthDate', 'email', 'phone_number', 'password', 'nationality']

        # Verificar que todos los campos requeridos están presentes en los datos enviados
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            response_data = {'error': f'Missing required fields: {", ".join(missing_fields)}'}
            return ApiResponse(message='Missing required fields', code=409, data=missing_fields).to_response()

        user_email = data.get('email')
        user_repo = UserRepository()
        temp_user_repo = TempUserRepository()

        existing_user = user_repo.find_by_email(user_email)
        existing_temp_user = temp_user_repo.find_by_email(user_email)

        if existing_user or existing_temp_user:
            response_data = {'error': 'User already exists' if existing_user else 'A user is trying to register with that email'}
            return ApiResponse(message='User already exists' if existing_user else 'A user is trying to register with that email', code=409, data=existing_user).to_response()

        phone_number = data.get('phone_number')
        hashed_password = RegistrationService.hash_password(data.get('password'))
        try:
            temp_user = TempUser(
                name=data.get('name'),
                lastName=data.get('lastName'),
                livePanama=data.get('livePanama'),
                birthDate=data.get('birthDate'),
                email=user_email,
                phoneNumber=phone_number,
                password=hashed_password,
                verification_code=secrets.token_hex(4),
                nationality=data.get('nationality')
            )
        except ValidationError as e:
            response_data = {'error': 'Invalid data', 'detail': e.errors()}
            return ApiResponse(message= response_data,code=400).to_response()
        
        temp_user_repo.insert(temp_user)
        new_temp_user= temp_user_repo.find_by_email(user_email)
        

        sms_result = send_verification_sms(phone_number)
        
        if isinstance(sms_result, dict) and 'error' in sms_result:
            response_data = {
                'error': 'Failed to send verification SMS.',
                'detail': sms_result
            }
            return ApiResponse(message='Failed to send verification SMS.', code=409, data=sms_result).to_response()

        response_data = {'message': 'SMS verification code sent'}
       # return Response(json.dumps(response_data), status=200, mimetype='application/json')
        return ApiResponse(data=new_temp_user.to_mongo_dict(), code=200,message='SMS verification code sent').to_response()

    @staticmethod
    def handle_step_2(data):
        sms_code = data.get('sms_code')
        phone_number = data.get('phone_number')
        email = data.get('email')

        if not phone_number or not sms_code:
            return ApiResponse(code=400, message='Phone number and SMS code are required', data={'step': 2}).to_response()

        temp_user_repo = TempUserRepository()
        temp_user = temp_user_repo.find_by_email(email)

        if temp_user:
            if temp_user.phoneVerified and temp_user.email_verified:
                return ApiResponse(code=400, message= "User is verified phone and email" , data= {'step': 2, 'tempUser':temp_user.to_mongo_dict()}).to_response()
            
            if temp_user.phoneVerified and not temp_user.email_verified:
                # Si el teléfono ya está verificado, solo envía el código de verificación por email
                email_verification_code = RegistrationService.generate_pin()
                try:
                    send_verification_email(email, email_verification_code)
                    temp_user.email_verification_code = email_verification_code
                    temp_user_repo.update(temp_user)
                    return ApiResponse(message='Email verification code sent', code=200, data={'step': 2}).to_response()
                except Exception as e:
                    return ApiResponse(message='Failed to send verification email', code=500, data={'step': 2, 'error': str(e)}).to_response()
            else:
                # Verifica el estado de la verificación del SMS
                verification_status = verify_sms(phone_number, sms_code)
                if verification_status == 'approved':
                    temp_user.phoneVerified = True
                    email_verification_code = RegistrationService.generate_pin()
                    try:
                        send_verification_email(email, email_verification_code)
                        temp_user.email_verification_code = email_verification_code
                        temp_user_repo.update(temp_user)
                        updated_temp_user = temp_user_repo.find_by_email(email)

                        return ApiResponse(message='SMS verified and email verification code sent', code=200, data={'step': 2}).to_response()
                    except Exception as e:
                        return ApiResponse(message='Failed to send verification email', code=500, data={'step': 2, 'error': str(e)}).to_response()
                else:
                    return ApiResponse(message='Invalid SMS code or verification not approved', code=400, data={'step': 2}).to_response()
        else:
            return ApiResponse(message='Temporary user not found', code=404, data={'step': 2}).to_response()
    
    
    @staticmethod
    def handle_step_3(data):
        user_email = data.get('email')
        email_code = data.get('email_code')

        temp_user_repo = TempUserRepository()
        user_repo = UserRepository()

        temp_user = temp_user_repo.find_by_email(user_email)

        if temp_user and verify_email_code(email_code, temp_user.email_verification_code) and temp_user.phoneVerified:
            temp_user.email_verified = True
            temp_user_repo.update(temp_user)

            new_user = RegistrationService.build_new_user(temp_user, temp_user.password)

            result = user_repo.insert(new_user)
            new_user_id = str(result)

            # Crear la información financiera básica para el usuario
            financial_info_user = RegistrationService.build_financial_info_user(new_user_id)
            financial_info_repo = FinancialInfoRepository()
            financial_info_id = financial_info_repo.insert(financial_info_user)

            # Actualizar el usuario con la referencia a la información financiera
            user_repo.update_by_id(new_user_id, {'financial_info_id': financial_info_id})

            if result:
                user_data = RegistrationService.build_response(new_user, result)
                response_data = {'user': user_data, 'step': 3}
                return ApiResponse(data=response_data, code=200, message='User registered successfully').to_response()
            else:
                response_data = {'step': 3, 'error': 'Failed to register user'}
                return ApiResponse(data=response_data, code=500, message='Failed to register user').to_response()
        else:
            response_data = {'step': 3, 'error': 'Invalid email code or phone not verified'}
            return ApiResponse(data=response_data, code=400, message='Invalid email code or phone not verified').to_response()


    
    @staticmethod
    def handle_step_4(data):
        required_fields = ["email", "firstName", "lastName", "occupation", "placeOfWork", "pep", "salary", "telephone", "address"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            response_data = {'step': 4, 'error': f'Missing required fields: {", ".join(missing_fields)}'}
            return ApiResponse(data=response_data, code=400, message='Missing required fields').to_response()

        try:
            # Validar y filtrar los datos recibidos utilizando el modelo de Pydantic
            address_data = data.get('address')
            address = PayCaddyAddress(
                addressLine1=address_data['addressLine1'],
                addressLine2=address_data.get('addressLine2'),
                homeNumber=address_data.get('homeNumber'),
                city=address_data['city'],
                region=address_data['region'],
                postalCode=address_data['postalCode'],
                country=address_data['country']
            )
            user_data = PayCaddyUser(
                email=data['email'],
                firstName=data['firstName'],
                lastName=data['lastName'],
                occupation=data['occupation'],
                placeOfWork=data['placeOfWork'],
                pep=data['pep'],
                salary=data['salary'],
                telephone=data['telephone'],
                address=address
            )
        except ValidationError as e:
            response_data = {'step': 4, 'error': 'Invalid data', 'detail': e.errors()}
            return ApiResponse(data=response_data, code=400, message='Invalid data').to_response()

        try:
            user_response = create_user_paycaddy(user_data.dict())
        except Exception as e:
            response_data = {'step': 4, 'error': 'Failed to create user in PayCaddy', 'detail': str(e)}
            return ApiResponse(data=response_data, code=500, message='Failed to create user in PayCaddy').to_response()

        if 'error' in user_response:
            response_data = {'step': 4, 'error': 'Failed to create user in PayCaddy', 'detail': user_response.get('error')}
            return ApiResponse(data=response_data, code=400, message='Failed to create user in PayCaddy').to_response()

        user_id = str(user_response['id'])

        card_order = CardOrder(
            user_id=user_id,
            user_id_paycaddy=user_response.get('id', ''),
            email=data['email'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            occupation=data['occupation'],
            placeOfWork=data['placeOfWork'],
            pep=data['pep'],
            salary=int(data['salary']),
            telephone=data['telephone'],
            address=data['address'],
            status=CardOrderKycStatus.PENDING.value,
            walletId=user_response.get('walletId', ''),
            kycUrl=user_response.get('kycUrl', ''),
            creationDate=user_response.get('creationDate', ''),
            pdfDocument=data.get('pdfDocument')
        )

        mongo.db.card_orders.insert_one(card_order.to_mongo_dict())
        response_data = RegistrationService.build_response_info_user_and_paycaddy(data, user_response)
        response_data['step'] = 4

        return ApiResponse(data=response_data, code=200, message='User registered successfully pending kyc').to_response()

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
            nationality=temp_user.nationality,
            birthDate=temp_user.birthDate,
            email_verified=temp_user.email_verified,
            phoneNumber=temp_user.phoneNumber,
            phoneVerified=temp_user.phoneVerified,
            livePanama=temp_user.livePanama,
            created_at=temp_user.created_at,
            update_at=datetime.utcnow(),
            email=temp_user.email,
            points=0,
            status=1,
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
            'email': new_user.email,
            'points': new_user.points,
            'status': new_user.status,
            'phoneVerified': new_user.phoneVerified,
            'emailVerified': new_user.email_verified
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
        
    @staticmethod
    def build_financial_info_user(user_id: str) -> FinancialInfo:
        return FinancialInfo(
        user_id=user_id
    )
        
    @staticmethod
    def resend_sms_verification(email):
        temp_user_repo = TempUserRepository()
        temp_user = temp_user_repo.find_by_email(email)
        if not temp_user:
            return ApiResponse(message='Temporary user not found', code=404).to_response()

        phone_number = temp_user.phoneNumber
        sms_result = send_verification_sms(phone_number)
        if isinstance(sms_result, dict) and 'error' in sms_result:
            return ApiResponse(message='Failed to send verification SMS', code=500, data=sms_result).to_response()

        return ApiResponse(message= 'Verification SMS sent successfully', code=200).to_response()
    
    @staticmethod
    def resend_email_verification(email):
        temp_user_repo = TempUserRepository()
        temp_user = temp_user_repo.find_by_email(email)
        if not temp_user:
            return ApiResponse(message='Temporary user not found', code=404).to_response()

        email_verification_code = RegistrationService.generate_pin()
        try:
            send_verification_email(email, email_verification_code)
            temp_user.email_verification_code = email_verification_code
            temp_user_repo.update(temp_user)
            return ApiResponse(message='Email verification code sent', code=200, data={'step': 2}).to_response()
        except Exception as e:
                return ApiResponse(message='Failed to send verification email', code=500, data={'step': 2, 'error': str(e)}).to_response()
         
