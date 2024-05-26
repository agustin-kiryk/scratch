from datetime import datetime


class TempUser:
    def __init__(self, email, phone_number, verification_code, email_verification_code):
        self.email = email
        self.phone_number = phone_number
        self.verification_code = verification_code
        self.email_verification_code = email_verification_code
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            'email': self.email,
            'phone_number': self.phone_number,
            'verification_code': self.verification_code,
            'email_verification_code': self.email_verification_code,
            'created_at': self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return TempUser(
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            verification_code=data.get('verification_code'),
            email_verification_code=data.get('email_verification_code')
        )
