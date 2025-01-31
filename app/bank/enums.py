from enum import Enum


class Action(Enum):
    def __str__(self):
        return self.name.replace("_", "").capitalize()


class ActionType(Action):
    USER_CREATED = 1
    DEPOSIT = 2
    WITHDRAWAL = 3
    TRANSFER = 4
    ACCOUNT_CREATED = 5
    ACCOUNT_UPDATED = 6
    ACCOUNT_DELETED = 7

class ActionStatus(Action):
    SUCCESS = 1
    FAILURE = 2
    PENDING = 3


class AccountType(Action):
    SAVINGS = 'SAV'
    CHECKING = 'CHK'
    BUSINESS = 'BUS'
    CREDIT_CARD = 'CC'
