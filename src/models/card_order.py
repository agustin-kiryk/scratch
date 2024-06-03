from datetime import datetime

from src.enums.Kyc_enum import CardOrderKycStatus


class CardOrder:
    collection_name: str = 'card_order'

    def __init__(self, user_id, data, status=CardOrderKycStatus):
        self.user_id = user_id
        self.user_id_paycaddy = ''
        self.email = data['email']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.occupation = data['occupation']
        self.placeOfWork = data['placeOfWork']
        self.pep = data['pep']
        self.salary = data['salary']
        self.telephone = data['telephone']
        self.address = data['address']
        self.status = status
        self.walletId = ''
        self.kycUrl = ''
        self.creationDate = datetime.utcnow()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_id_paycaddy': self.user_id_paycaddy,
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'occupation': self.occupation,
            'placeOfWork': self.placeOfWork,
            'pep': self.pep,
            'salary': self.salary,
            'telephone': self.telephone,
            'address': self.address,
            'status': self.status,
            'walletId': self.walletId,
            'kycUrl': self.kycUrl,
            'creationDate': self.creationDate
        }

    def to_mongo_dict(self, include_all_fields=True):
        data = self.dict(by_alias=True)
        if not include_all_fields:
            data = {k: v for k, v in data.items() if v is not None}
        if not data.get("_id"):
            data.pop("_id", None)
        return data

    @staticmethod
    def from_mongo_dict(data):
        data["id"] = str(data.pop("_id", None))
        return CardOrder(**data)
