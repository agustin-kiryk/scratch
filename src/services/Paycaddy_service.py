import logging

from flask import request, jsonify
from src.config.mongodb import mongo
from src.enums.Kyc_enum import CardOrderKycStatus
from src.repositories.Card_order_repository import CardOrderRepository
from src.repositories.User_kyc_repository import UserKYCRepository
from src.repositories.User_repository import UserRepository


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
            create_wallet_for_user(user_id_paycaddy)

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


def create_wallet_for_user(user_id):
    #  hacer una llamada a Paycaddy para crear la wallet
    pass
