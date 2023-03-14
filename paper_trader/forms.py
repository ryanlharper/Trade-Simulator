from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from transactions.models import Transaction
from user_accounts.models import UserAccount


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'symbol', 'quantity', 'notes']

