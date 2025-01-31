from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.conf import settings
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


class LogEntry(models.Model):
    action = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in ActionType])
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in ActionStatus])
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} at {self.timestamp}"

    @classmethod
    def log(cls, action: ActionType, status: ActionStatus, details: str = "") -> None:
        cls.objects.create(action=action, status=ActionStatus, details=details)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        if not username:
            raise ValueError("The user field must be set")
        if not password:
            raise ValueError("The password field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Adding a custom related_name to avoid clashes
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Adding a custom related_name to avoid clashes
        blank=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    def __str__(self):
        return self.username


class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    account_holder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bank_accounts')
    account_type = models.CharField(
        max_length=3,
        choices=[(tag.value, str(tag)) for tag in AccountType],
    )
    bank_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_holder.username} - {self.account_number} ({self.account_type})"

    def deposit(self, amount: float):
        log = f"{amount:%.2f} -> {self.account_number}"
        if amount <= 0:
            error = "Deposit should be positive!"
            LogEntry.log(ActionType.DEPOSIT, ActionStatus.FAILURE, ' '.join((log, f"error: {error}")))
            raise ValueError(error)

        self.balance += amount
        self.save()
        LogEntry.log(ActionType.DEPOSIT, ActionStatus.FAILURE, log)
        return self

    def withdraw(self, amount: float):
        log = f"{self.account_number} -> {amount:%.2f}"
        if amount <= 0:
            error = "Withdrawal amount should be positive!"
            LogEntry.log(ActionType.WITHDRAWAL, ActionStatus.FAILURE, ' '.join((log, f"error: {error}")))
            raise ValueError(error)
        if amount > self.balance:
            error = "Insufficient funds!"
            LogEntry.log(ActionType.WITHDRAWAL, ActionStatus.FAILURE, ' '.join((log, f"error: {error}")))
            raise ValueError(error)

        self.balance -= amount
        self.save()
        LogEntry.log(ActionType.WITHDRAWAL, ActionStatus.FAILURE, log)
        return self

    def transfer(self, to_account, amount: float) -> None:
        log = f"{self.account_number} -> {amount:%.2f} -> {to_account.account_number}"
        LogEntry.log(ActionType.TRANSFER, ActionStatus.PENDING, log)
        try: self.withdraw(amount)
        except ValueError as e:
            LogEntry.log(ActionType.TRANSFER, ActionStatus.FAILURE, log)
            raise e
        else:
            to_account.deposit(amount)
            LogEntry.log(ActionType.TRANSFER, ActionStatus.SUCCESS, log)
 