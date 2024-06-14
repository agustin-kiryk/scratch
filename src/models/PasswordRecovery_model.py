from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

class PasswordRecovery(BaseModel):
    id: Optional[str] = Field(None, alias='_id')
    email: EmailStr
    recovery_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

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
        return PasswordRecovery(**data)