from flask import Blueprint, request
from src.ApiResponse import ApiResponse
from datetime import datetime
from src.repositories.Financial_Info_repository import FinancialInfoRepository



financial_bp = Blueprint('financial', __name__)

@financial_bp.route('/financial_info/<user_id>', methods=['PUT'])
def update_financial_info(user_id):
    data = request.json
    
    # Filtrar solo los campos proporcionados en la solicitud
    update_fields = {k: v for k, v in data.items() if v is not None}
    
    # Añadir la fecha de actualización
    update_fields['updated_at'] = datetime.utcnow()

    financial_info_repo = FinancialInfoRepository()
    financial_info_repo.update_by_user_id(user_id, update_fields)

    return ApiResponse(message='Financial information updated successfully', code=200).to_response()


