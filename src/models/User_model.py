from pydantic import BaseModel, EmailStr, Field, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional
import bcrypt

from src.enums.Kyc_enum import CardOrderKycStatus


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    lastName: str
    livePanama: bool
    birthDate: str
    nationality: str
    phoneNumber: str
    email: EmailStr
    points: int = 0
    status: int = 1
    password: str
    phoneVerified: bool
    email_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    financial_info_id: Optional[str] = None  # Referencia a la información financiera
    role: str = "user"
    kycStatus: Optional[CardOrderKycStatus] = CardOrderKycStatus.NOT_REGISTER.value

    collection_name: str = 'users'

    @validator("name", "lastName", "email", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

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
        # Convert ObjectId to string
        if '_id' in data and isinstance(data['_id'], ObjectId):
            data['_id'] = str(data['_id'])
        if 'financial_info_id' in data and isinstance(data['financial_info_id'], ObjectId):
            data['financial_info_id'] = str(data['financial_info_id'])
        user = User(**data)
        return user