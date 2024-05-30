import json

from flask import Blueprint, request, jsonify, Response
from src.services.registration_service import RegistrationService

register_bp = Blueprint('registerUser', __name__)


@register_bp.route('/registerUser', methods=['POST'])
def register_user():
    data = request.get_json()
    step = data.get('step')
    if step == 1:
        return RegistrationService.handle_step_1(data)
    elif step == 2:
        return RegistrationService.handle_step_2(data)
    elif step == 3:
        return RegistrationService.handle_step_3(data)
    elif step == 4:
        return RegistrationService.handle_step_4(data)
    else:
        response_data = {'error': 'Invalid step'}
        return Response(json.dumps(response_data), status=400, mimetype='application/json')
