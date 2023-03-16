from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from transactions.models import Transaction
import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from django.core.exceptions import ValidationError
from user_accounts.models import UserAccount
from django.shortcuts import get_object_or_404
from datetime import datetime, timezone

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'symbol', 'quantity', 'notes']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        symbol = cleaned_data.get('symbol')
        quantity = cleaned_data.get('quantity')
        
        # Check if symbol is valid using yfinance
        try:
            stock_info = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        except:
            raise ValidationError("Invalid symbol")
        
        if self.request and self.request.user.is_authenticated:
            # Check if there is enough cash
            user_account = get_object_or_404(UserAccount, user=self.request.user)
            cash_position = user_account.position_set.get(symbol='cash')
            if cash_position.market_value < yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1] * quantity:
                raise ValidationError("Not enough cash")
            else:
                # check if transaction is during market open
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

