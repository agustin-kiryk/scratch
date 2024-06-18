from flask import request, jsonify
from src.config.mongodb import mongo
from src.enums.Kyc_enum import CardOrderKycStatus
from src.repositories.Card_order_repository import CardOrderRepository


def process_webhook_data():
    try:
        payload_body = request.get_json()

        if not payload_body or 'metadata' not in payload_body:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data, missing metadata"}), 400

        metadata = payload_body['metadata']
        if 'userId' not in metadata:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data Metadata, missing userId"}), 400

        user_id = metadata['userId']
        kyc_status = payload_body.get('status')
        description = payload_body.get('description')
        full_name = payload_body.get('fullName')
        age = payload_body.get('age')
        timestamp = payload_body.get('timeStamp')

        card_order_repository = CardOrderRepository(mongo.db)
        card_order = card_order_repository.find_by_user_id(user_id)

        if not card_order:
            return jsonify({"error": "Card order not found"}), 404

        if kyc_status not in CardOrderKycStatus.list():
            return jsonify({"error": "Invalid KYC status"}), 400

        new_status = CardOrderKycStatus[kyc_status]

        if new_status == CardOrderKycStatus.VERIFIED:
            create_wallet_for_user(user_id)

        card_order_repository.update_status(user_id, new_status)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_wallet_for_user(user_id):

    #  hacer una llamada a Paycaddy para crear la wallet
    pass
