from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class FinancialDocument(BaseModel):
    document_name: str
    document_content: str  # PDF en base64

class FinancialInfo(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    user_id: str  # Referencia al usuario
    place_of_work: Optional[str] = None
    salary: Optional[float] = None
    type_of_work: Optional[str] = None
    name_of_company: Optional[str] = None
    position: Optional[str] = None
    seniority: Optional[float] = None  # Antiguedad laboral
    social_security: Optional[str] = None  # Base 64
    movements: Optional[str] = None  # Base 64
    website: Optional[str] = None
    social_networks: Optional[str] = None  # Redes sociales
    tax_return: Optional[str] = None  # Declaración de renta
    operation_notice: Optional[str] = None  # Aviso de operación BASE 64
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    
    def to_mongo_dict(self, include_all_fields=True):
        data = self.dict(by_alias=True)
        if not include_all_fields:
            data = {k: v for k, v in data.items() if v is not None}
        return data

    @staticmethod
    def from_mongo_dict(data):
        data["id"] = str(data.pop("_id", None))
        return FinancialInfo(**data)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
