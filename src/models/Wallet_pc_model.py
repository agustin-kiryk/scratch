from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class Wallet(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str  # Internal user ID
    user_pc_id: str  # Paycaddy user ID
    wallet_pc_id: str  # Paycaddy wallet ID
    card_pc_id: Optional[str] = None  # Paycaddy card ID
    currency: str
    description: str
    limit: int
    creation_date: datetime
    type: str = "credit"

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
        if '_id' in data:
            data['id'] = str(data.pop('_id'))
        else:
            data['id'] = None
        return Wallet(**data)
