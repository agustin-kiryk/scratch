from enum import Enum


class CardOrderKycStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REVIEW_NEEDED = "reviewNeeded"
    VERIFICATION_INPUTS_COMPLETED = "verification_inputs_completed"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, CardOrderKycStatus))
