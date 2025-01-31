from faker import Faker
from django.test import TestCase
from .models import CustomUser, BankAccount, AccountType, LogEntry

faker = Faker()

class BankAccountTest(TestCase):
    def setUp(self):
        self.user_1 = CustomUser.objects.create_user(
            email=faker.email(),
            username=faker.user_name(),
            password=faker.password(length=20),
        )
        self.user_2 = CustomUser.objects.create_user(
            email=faker.email(),
            username=faker.user_name(),
            password=faker.password(length=20),
        )


    def test_transfer_and_logs(self):
        bank_account_1 = BankAccount.objects.create(
            account_number="".join(str(faker.random_digit()) for _ in range(20)),
            account_holder=self.user_1,
            account_type=AccountType.CREDIT_CARD,
            bank_name=faker.company(),
            balance=2000.0,
        )
        bank_account_2 = BankAccount.objects.create(
            account_number="".join(str(faker.random_digit()) for _ in range(20)),
            account_holder=self.user_2,
            account_type=AccountType.BUSINESS,
            bank_name=faker.company(),
            balance=20,
        )
        bank_account_1.transfer(bank_account_2, 1000.0)
        logs = LogEntry.objects.all()
        self.assertGreater(len(logs), 0)
        for log in logs: print(log)

