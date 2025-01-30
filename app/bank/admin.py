from django.contrib import admin
from .models import CustomUser, BankAccount

admin.site.register(CustomUser)
admin.site.register(BankAccount)
