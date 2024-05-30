from pydantic import BaseModel, EmailStr, Field, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    lastName: str
    document: str
    email: EmailStr
    points: int = 0
    status: int = 1
    pin: Optional[str]
    password: str

    @validator("name", "lastName", "document", "email", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

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
        return User(**data)
