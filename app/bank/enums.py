from enum import Enum


class ActionType(Enum):
    USER_CREATED = "User Created"
    DEPOSIT = "Deposit Made"
    WITHDRAWAL = "Withdrawal Made"
    TRANSFER = "Transfer Made"
    ACCOUNT_CREATED = "Bank Account Created"
    ACCOUNT_UPDATED = "Bank Account Updated"
    ACCOUNT_DELETED = "Bank Account Deleted"

    def __str__(self):
        return self.value


class ActionStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    PENDING = 3

    def __str__(self):
        return self.value


class AccountType(Enum):
    SAVINGS = 'SAV'
    CHECKING = 'CHK'
    BUSINESS = 'BUS'
    CREDIT_CARD = 'CC'

    def __str__(self):
        return self.name.replace("_", "").capitalize()

