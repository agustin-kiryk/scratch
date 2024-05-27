from datetime import datetime

from src.enums.Kyc_enum import CardOrderKycStatus


class CardOrder:
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
