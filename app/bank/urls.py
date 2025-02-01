from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bank.views import (
    CustomUserViewSet, BankAccountViewSet, LogEntryViewSet,
    home, register, login_view, profile, account
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'accounts', BankAccountViewSet)
router.register(r'logs', LogEntryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('account/', account, name='account'),
]