from enum import Enum


class BaseLedgerOperation(str, Enum):
    def dummy(self):
        pass


SHARED_OPERATION_CONFIG = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
}

SHARED_OPERATION_VALUES = {
    "DAILY_REWARD": "DAILY_REWARD",
    "SIGNUP_CREDIT": "SIGNUP_CREDIT",
    "CREDIT_SPEND": "CREDIT_SPEND",
    "CREDIT_ADD": "CREDIT_ADD"
}
