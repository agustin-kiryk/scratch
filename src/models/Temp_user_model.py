from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime
from typing import Optional
import bcrypt


class TempUser(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    lastName: str
    livePanama: bool
    birthDate: str
    email: EmailStr
    phoneNumber: str
    password: str  # Contraseña hasheada
    verification_code: str
    nationality: str
    email_verification_code: Optional[str] = None
    phoneVerified: Optional[bool] = Field(default=False)
    email_verified: Optional[bool] = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at:Optional[datetime] = Field(default_factory=datetime.utcnow)

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
        data["_id"] = str(data.get("_id", ""))
        return TempUser(**data)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
