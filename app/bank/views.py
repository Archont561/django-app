from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import CustomUser, BankAccount, LogEntry, ActionType, ActionStatus
from .serializers import CustomUserSerializer, BankAccountSerializer, LogEntrySerializer


# API dla użytkowników
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# API dla kont bankowych
class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        """ Obsługa wpłaty na konto """
        account = self.get_object()
        amount = request.data.get('amount')
        if not amount or float(amount) <= 0:
            return Response({'error': 'Invalid deposit amount'}, status=status.HTTP_400_BAD_REQUEST)

        account.deposit(float(amount))
        return Response({'message': 'Deposit successful', 'new_balance': account.balance})

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        """ Obsługa wypłaty z konta """
        account = self.get_object()
        amount = request.data.get('amount')
        if not amount or float(amount) <= 0:
            return Response({'error': 'Invalid withdrawal amount'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account.withdraw(float(amount))
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Withdrawal successful', 'new_balance': account.balance})

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        """ Obsługa przelewu między kontami """
        account = self.get_object()
        to_account_id = request.data.get('to_account')
        amount = request.data.get('amount')

        if not to_account_id or not amount or float(amount) <= 0:
            return Response({'error': 'Invalid transfer request'}, status=status.HTTP_400_BAD_REQUEST)

        to_account = get_object_or_404(BankAccount, id=to_account_id)

        try:
            account.transfer(to_account, float(amount))
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Transfer successful', 'new_balance': account.balance})


# API dla logów operacji bankowych
class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
