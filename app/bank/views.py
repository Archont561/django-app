from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.decorators import login_required
from .models import CustomUser, BankAccount, LogEntry
from .serializers import CustomUserSerializer, BankAccountSerializer, LogEntrySerializer
from .forms import CustomUserCreationForm

# API dla użytkowników (tylko administratorzy mogą zarządzać użytkownikami)
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]  # Tylko administratorzy mają dostęp


# API dla kont bankowych (zwykli użytkownicy widzą swoje konta, admini - wszystko)
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


# API dla logów (tylko administratorzy mogą przeglądać logi)
class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = [permissions.IsAdminUser]  # Tylko administratorzy widzą logi


# frontend
def home(request):
    return render(request, 'bank/home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Handle file uploads like profile pictures
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'bank/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # invalid login
            return render(request, 'bank/login.html', {'error': 'Invalid credentials'})

    return render(request, 'bank/login.html')


@login_required
def profile(request):
    return render(request, 'bank/profile.html', {'user': request.user})

@login_required
def account(request):
    user_accounts = request.user.bank_accounts.all()
    return render(request, 'bank/account.html', {'accounts': user_accounts})