from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from src.enums.Kyc_enum import CardOrderKycStatus
from src.models.PaycaddyUser import PayCaddyAddress


class CardOrder(BaseModel):
    collection_name: str = 'card_orders'

    id: Optional[str] = Field(None, alias='_id')
    user_id: str
    user_id_paycaddy: str
    email: str
    firstName: str
    lastName: str
    occupation: str
    placeOfWork: str
    pep: bool
    salary: int
    telephone: str
    address:PayCaddyAddress
    status: str
    walletId: str
    kycUrl: str
    creationDate: str
    pdfDocument: Optional[str] = None  # Campo PDF en base64

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_mongo_dict(self, include_all_fields=True):
        data = self.dict(by_alias=True)
        if not include_all_fields:
            data = {k: v for k, v in data.items() if v is not None}
        return data

    @staticmethod
    def from_mongo_dict(data):
        data["id"] = str(data.pop("_id", ""))
        return CardOrder(**data)
