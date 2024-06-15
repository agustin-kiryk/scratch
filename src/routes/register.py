import json

from flask import Blueprint, request, jsonify, Response
from src.services.Registration_service import RegistrationService
from src.utils.Api_response import ApiResponse

register_bp = Blueprint('registerUser', __name__)


@register_bp.route('/registerUser', methods=['POST'])
def register_user():
    app.logger.info('Received request for /registerUser')
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
        return ApiResponse(message='Invalid step',code=400).to_response()
    
    
@register_bp.route('/resendSms', methods=['POST'])
def resend_sms():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return ApiResponse(message='Email is required', code=400).to_response()
    return RegistrationService.resend_sms_verification(email)

@register_bp.route('/resendEmailCode', methods=['POST'])
def resend_email_code():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return ApiResponse(message='Email is required', code=400).to_response()
    return RegistrationService.resend_email_verification(email)
