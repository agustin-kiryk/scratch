from src.controllers.Base_controller import BaseController
from src.models.Financial_info import FinancialInfo
from src.services.FinancialInfo_service import FinancialInfoService

class FinancialController(BaseController[FinancialInfo]):
    def __init__(self):
        super().__init__(FinancialInfoService(), FinancialInfo)
        
    def put(self, entity_id):
        return self.service.update_financial_info_by_user_id(entity_id)