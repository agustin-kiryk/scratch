from enum import Enum


class WalletsTypesE(Enum):
    CREDIT = "credit"
    DEBIT = "debit"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, WalletsTypesE))
