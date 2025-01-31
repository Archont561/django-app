from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CustomUser, BankAccount, LogEntry
from .serializers import CustomUserSerializer, BankAccountSerializer, LogEntrySerializer

#API dla użytkowników (tylko administratorzy mogą zarządzać użytkownikami)
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]  # Tylko administratorzy mają dostęp

#API dla kont bankowych (zwykli użytkownicy widzą swoje konta, admini - wszystko)
class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    def get_permissions(self):
        """ Administratorzy widzą wszystko, użytkownicy tylko swoje konta """
        if self.action in ['list', 'retrieve']:  # Odczyt danych dostępny dla użytkowników
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]  # Tylko administrator może edytować i tworzyć konta

    def get_queryset(self):
        """ Zwykli użytkownicy widzą tylko swoje konta, admini widzą wszystko """
        user = self.request.user
        if user.is_staff:  # Admini widzą wszystko
            return BankAccount.objects.all()
        return BankAccount.objects.filter(account_holder=user)  # Zwykli użytkownicy widzą tylko swoje konta

#API dla logów (tylko administratorzy mogą przeglądać logi)
class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAdminUser]  # Tylko administratorzy widzą logi