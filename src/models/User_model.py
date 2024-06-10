from pydantic import BaseModel, EmailStr, Field, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional
import bcrypt


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

    collection_name: str = 'users'  # Nombre de la colección

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
        data["id"] = str(data.pop("_id", ""))
        return User(**data)
