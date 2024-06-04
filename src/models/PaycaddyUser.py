from pydantic import BaseModel, EmailStr
from typing import Optional

class PayCaddyAddress(BaseModel):
    addressLine1: str
    addressLine2: Optional[str] = None
    homeNumber: Optional[str] = None
    city: str
    region: str
    postalCode: str
    country: str

class PayCaddyUser(BaseModel):
    email: EmailStr
    firstName: str
    lastName: str
    occupation: str
    placeOfWork: str
    pep: bool
    salary: int
    telephone: str
    address: PayCaddyAddress
