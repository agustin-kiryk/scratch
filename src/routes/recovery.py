from flask import Blueprint, request
from src.services.Recovery_service import RecoveryService
from src.Api_response import ApiResponse

recovery_bp = Blueprint('recovery', __name__)

@recovery_bp.route('/request_password_recovery', methods=['POST'])
def request_password_recovery():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return ApiResponse(message='Email is required', code=400).to_response()
    return RecoveryService.request_password_recovery(email)

@recovery_bp.route('/verify_recovery_code', methods=['POST'])
def verify_recovery_code():
    data = request.get_json()
    email = data.get('email')
    recovery_code = data.get('recovery_code')
    if not email or not recovery_code:
        return ApiResponse(message='Email and recovery code are required', code=400).to_response()
    return RecoveryService.verify_recovery_code(email, recovery_code)

@recovery_bp.route('/set_new_password', methods=['POST'])
def set_new_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    if not email or not new_password:
        return ApiResponse(message='Email and new password are required', code=400).to_response()
    return RecoveryService.set_new_password(email, new_password)