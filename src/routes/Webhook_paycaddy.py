from flask import Blueprint, jsonify
from src.services.Paycaddy_service import process_webhook_data

webhook_paycaddy_blueprint = Blueprint('/paycaddy', __name__)

@webhook_paycaddy_blueprint.route('/', methods=['POST'])
def process_webhook():
    response = process_webhook_data()
    return response, 200;

# falta hacer un get al user para obtener la url de kyc nuevamente en el caso de que falle la validacion
