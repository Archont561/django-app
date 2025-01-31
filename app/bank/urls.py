from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bank.views import CustomUserViewSet, BankAccountViewSet, LogEntryViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'accounts', BankAccountViewSet)
router.register(r'logs', LogEntryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]