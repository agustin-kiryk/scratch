from flask import request, jsonify
from src.config.mongodb import mongo

def process_webhook_data():
    try:
        payload_body = request.get_json()

        if not payload_body or 'metadata' not in payload_body:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data, missing metadata"}), 400
        
        metadata = payload_body['metadata']
        if 'userId' not in metadata:
            return jsonify({"error": "Invalid WebHook Paycaddy KYC Data Metadata, missing userId"}), 400
        
        user_id = metadata['userId']
        
        # Aquí debes verificar el estado del KYC
        kyc_status = payload_body.get('status')
        if kyc_status != 'VERIFIED':
            return jsonify({"error": "KYC not verified"}), 400
        
        # Busca el pedido de tarjeta correspondiente al user_id
        card_order = mongo.db.card_orders.find_one({"user_id": user_id})
        if not card_order:
            return jsonify({"error": "Card order not found"}), 404

        # Aquí puedes crear la wallet para el usuario y actualizar el estado del pedido de tarjeta
        create_wallet_for_user(user_id)

        mongo.db.card_orders.update_one(
            {"_id": card_order["_id"]},
            {"$set": {"status": "wallet_created"}}
        )

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_wallet_for_user(user_id):
    # Implementa la lógica para crear una wallet para el usuario
    #  hacer una llamada a Paycaddy para crear la wallet
    pass
