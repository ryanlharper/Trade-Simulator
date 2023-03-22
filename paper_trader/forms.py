from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from transactions.models import Transaction
import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from django.core.exceptions import ValidationError
from datetime import datetime, timezone

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'symbol', 'quantity', 'notes']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        symbol = cleaned_data.get('symbol').upper()
        quantity = cleaned_data.get('quantity')

        # check if symbol is valid
        try:
            stock_info = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        except:
            raise ValidationError("Invalid symbol")
        
        # check for positive quantity
        if quantity <=0:
            raise ValidationError("Quantity must be greater than zero.")
        
        # check if market open
        timestamp = datetime.now(timezone.utc)
        nyse = mcal.get_calendar('NYSE')
        schedule = nyse.schedule(start_date=timestamp.date(), end_date=timestamp.date())
        if len(schedule) == 0:
                raise ValidationError('Market is closed')
        else:
            market_open = pd.Timestamp(schedule.iloc[0]['market_open'].strftime('%Y-%m-%d %H:%M:%S'))
            market_close = pd.Timestamp(schedule.iloc[0]['market_close'].strftime('%Y-%m-%d %H:%M:%S'))
            timestamp = pd.Timestamp(timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            if timestamp < market_open or timestamp > market_close:
                raise ValidationError('Market is closed')
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email address.")
        return email