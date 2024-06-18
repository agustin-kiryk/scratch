from flask import Blueprint, request
from src.controllers.FinancialInfo_controller import FinancialController
from src.utils.Api_response import ApiResponse
from datetime import datetime
from src.repositories.Financial_Info_repository import FinancialInfoRepository

financial_bp = Blueprint('financial', __name__)
financial_view =FinancialController.as_view('financialInfo_api')
financial_bp.add_url_rule('/financialInfo', defaults={'entity_id': None}, view_func=financial_view, methods=['GET'])
financial_bp.add_url_rule('/financialInfo/<entity_id>', view_func=financial_view, methods=['GET', 'PUT', 'DELETE'])

