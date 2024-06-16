from datetime import datetime
from flask import request
from src.models.Financial_info import FinancialInfo
from src.repositories.Financial_Info_repository import FinancialInfoRepository
from src.services.Base_serice import BaseService
from src.utils.Api_response import ApiResponse
from src.errorHandler.error_codes import codes


class FinancialInfoService(BaseService[FinancialInfo]):
    def __init__(self):
        super().__init__(FinancialInfoRepository())

    def update_fputinancial_info(user_id):
        data = request.json

        # Filtrar solo los campos proporcionados en la solicitud
        update_fields = {k: v for k, v in data.items() if v is not None}

        # Añadir la fecha de actualización
        update_fields['updated_at'] = datetime.utcnow()

        financial_info_repo = FinancialInfoRepository()
        financial_info_repo.update_by_user_id(user_id, update_fields)

        return ApiResponse(message='Financial information updated successfully', code=codes.SUCCESS).to_response()

    def update_financial_info_by_user_id(self, user_id: str):
        data = request.json

        # Filtrar solo los campos proporcionados en la solicitud
        update_fields = {k: v for k, v in data.items() if v is not None}

        # Añadir la fecha de actualización
        update_fields['updated_at'] = datetime.utcnow()

        # Llama al método del repositorio para actualizar la información financiera
        self.repository.update_by_user_id(user_id, update_fields)

        return ApiResponse(message='Financial information updated successfully', code=codes.SUCCESS).to_response()
