import logging
from datetime import datetime

from flask import request, jsonify

from src.client import Paycaddy_client
from src.config.mongodb import mongo
from src.enums.Kyc_enum import CardOrderKycStatus
from src.enums.Wallet_types_pc_E import WalletsTypesE
from src.models.Wallet_pc_model import Wallet
from src.repositories.Card_order_repository import CardOrderRepository
from src.repositories.User_kyc_repository import UserKYCRepository
from src.repositories.User_repository import UserRepository
from src.repositories.Wallet_pc_repository import WalletRepository


def process_webhook_data():
    try:
        payload_body = request.get_json()
        logging.info(f"f: received webhook request from paycaddy {payload_body}")

        if not payload_body or 'metadata' not in payload_body:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data, missing metadata"}), 400

        metadata = payload_body['metadata']
        if 'userId' not in metadata:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data Metadata, missing userId"}), 400

        user_id_paycaddy = metadata['userId']
        kyc_status = payload_body.get('status')
        description = payload_body.get('description')
        full_name = payload_body.get('fullName')
        age = payload_body.get('age')
        timestamp = payload_body.get('timeStamp')

        card_order_repository = CardOrderRepository()
        user_kyc_repository = UserKYCRepository()
        userRepository = UserRepository()

        card_order = card_order_repository.find_by_user_id_paycaddy(user_id_paycaddy)

        if not card_order:
            return jsonify({"error": "Card order not found"}), 404

        if kyc_status not in CardOrderKycStatus.list():
            return jsonify({"error": "Invalid KYC status"}), 400

        new_status = CardOrderKycStatus[kyc_status.upper()]  # Convert the string to the Enum type
        user_real = userRepository.find_by_id(card_order.user_id)
        user_real.kycStatus = new_status.value
        userRepository.update(user_real)

        if new_status == CardOrderKycStatus.VERIFIED:
            create_credit_wallet_for_user(card_order)

        # Almacenar la referencia del KYC en la colección user_kyc
        user_kyc_data = {
            "user_id_paycaddy": user_id_paycaddy,
            "kyc_status": new_status.value,
            "description": description,
            "full_name": full_name,
            "age": age,
            "timestamp": timestamp,
            "user_id": user_real.id
        }

        existing_user_kyc = user_kyc_repository.find_by_user_id(user_real.id)
        if existing_user_kyc:
            user_kyc_repository.update(user_real.id, user_kyc_data)
        else:
            user_kyc_repository.insert(user_kyc_data)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_credit_wallet_for_user(card_order):
    """Evaluar salario y ocupación para establecer el límite de crédito y crear la wallet de crédito en Paycaddy."""
    try:
        wallet_repo = WalletRepository()
        existing_wallet = wallet_repo.find_by_user_id_and_type(card_order.user_id, WalletsTypesE.CREDIT.value)

        if existing_wallet:
            logging.info(f"User {card_order.user_id} already has a credit wallet: {existing_wallet}")
            return {"message": "User already has a credit wallet", "wallet": existing_wallet}

        salary = card_order.salary
        occupation = card_order.occupation.lower()
        logging.info(f"Creating credit wallet for user with occupation: {occupation} and salary: {salary}")

        # Establecer los límites según la ocupación
        occupation_limits = {
            'trabajador': 0.30,
            'emprendedor': 0.25,
            'papas apoyan': 0.20,
            'cryptouser': 0.30
        }

        # Validar la ocupación
        if occupation not in occupation_limits:
            logging.error(f"Invalid occupation: {occupation}")
            return {"error": "Invalid occupation"}

        # Calcular el límite de crédito
        credit_limit = int(salary * occupation_limits[occupation])  # Convertir el límite a entero
        logging.info(f"Credit limit calculated: {credit_limit}")

        # Realizar la llamada a la API de Paycaddy para crear la wallet de crédito
        wallet_data = {
            "userId": card_order.user_id_paycaddy,
            "currency": "USD",
            "description": "Credit wallet created based on KYC verification",
            "time": 0,
            "limit": credit_limit,
            'CreditProductCode': "1"
        }

        logging.info(f"Sending request to Paycaddy: {wallet_data}")
        response = Paycaddy_client.create_wallet_credit_pc(wallet_data)
        logging.info(f"response receipt to Paycaddy: {response}")
        if 'error' in response:
            logging.error(f"Error creating credit wallet: {response}")
            return {"error": "Error creating credit wallet", "details": response}

        logging.info(f"Credit wallet created successfully: {response}")
        save_wallet(card_order.user_id, response)
        return response

    except Exception as e:
        logging.error(f"Error in create_credit_wallet_for_user: {str(e)}")
        return {"error": "Exception occurred", "details": str(e)}


def save_wallet(user_id, wallet_data):
    try:
        wallet_repo = WalletRepository()
        wallet_repo.find_by_user_id(user_id)

        wallet = Wallet(
            wallet_pc_id=wallet_data['id'],
            user_id=user_id,
            user_pc_id=wallet_data['userId'],
            currency=wallet_data['currency'],
            description=wallet_data['description'],
            limit=wallet_data['limit'],
            creation_date=datetime.fromisoformat(wallet_data['creationDate']),
            type=WalletsTypesE.CREDIT.value
        )
        wallet_repo.insert(wallet)
        logging.info(f"Wallet saved to database: {wallet}")
    except Exception as e:
        logging.error(f"Error saving wallet to database: {str(e)}")


"""-Endpoint para que se verifiquen los datos de la informacion financiera para luego aumentar el limite de la wallet de credito segun el salario
-Endpoint para solicitar tarjeta Una vez que se aprueva el credito el usuario puede solicitar la tarjeta de credito
CONSULTAR SI LA MISMA WALLET DE CREDITO VA A SER USADA PARA EL CREDITO PRINCIPAL DEL APP Y PARA LA TARJETA DE CREDITO O VAN A SER 2 WALLETS DIFERENTES 
-REVISAR PUT INFORMACION FINANCIERA"""
