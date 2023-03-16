import yfinance as yf
from .models import Position
from decimal import Decimal

def update_positions():
    for position in Position.objects.exclude(symbol='cash'):
        price = Decimal(yf.Ticker(position.symbol).history(period='4d')['Close'].iloc[-1])
        position.price = price
        position.save()