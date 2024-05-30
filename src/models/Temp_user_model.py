from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime
from typing import Optional

class TempUser(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: EmailStr
    phone_number: str
    verification_code: str
    email_verification_code: Optional[str] = None
    phone_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def to_mongo_dict(self):
        data = self.dict(by_alias=True)
        if not data.get("_id"):
            data.pop("_id", None)
        return data

    @staticmethod
    def from_mongo_dict(data):
        data["id"] = str(data.pop("_id", None))
        return TempUser(**data)
