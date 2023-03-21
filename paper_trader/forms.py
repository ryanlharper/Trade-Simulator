from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from transactions.models import Transaction
import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
from django.core.exceptions import ValidationError
from positions.models import Position, Comment
from django.shortcuts import get_object_or_404
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
        type = cleaned_data.get('type')
        symbol = cleaned_data.get('symbol').upper()
        quantity = cleaned_data.get('quantity')

        # check if symbol is valid
        try:
            stock_info = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        except:
            raise ValidationError("Invalid symbol")
        
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
        
        # check if funds are available for buy transaction
        if type == 'buy':
            cash_position = get_object_or_404(Position.objects.get(user=self.request.user, symbol='cash'))
            if cash_position.quantity < yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1] * quantity:
                raise ValidationError("Not enough cash")

        # chack if shares are available for sell transaction
        else:
            try:
                position = get_object_or_404(Position.objects.get(user=self.request.user, symbol=symbol))
            except Position.DoesNotExist:
                raise ValidationError("No shares to sell")
            if position is not None:
                if quantity > position.quantity:
                    raise ValidationError("Not enough shares to sell")

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Add a comment',
        'rows': 3
    }))
    
    class Meta:
        model = Comment
        fields = ('text',)