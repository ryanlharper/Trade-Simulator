from django.shortcuts import render, redirect
from django.urls import reverse
from positions.models import Position
from paper_trader.forms import TransactionForm
import yfinance as yf
from datetime import datetime
import pandas as pd
import pandas_market_calendars as mcal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal

# need updates considering accountvalues model addition

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.timestamp = datetime.now()
            transaction.quantity = form.cleaned_data['quantity']
            transaction.price = yf.Ticker(transaction.symbol).history(period='1d')['Close'].iloc[-1]
            
            # Check if funds are available for the transaction
            cash_position = Position.objects.filter(user=request.user, symbol='cash').first()  
            if not cash_position:
                cash_position = Position(user=request.user, symbol='cash')
                cash_position.price = 1
                cash_position.cost = 1
                cash_position.market_value = 0
                cash_position.percent_portfolio = 0
                cash_position.quantity = 0
                cash_position.save()
            if transaction.type == 'buy':
                total_cost = transaction.quantity * transaction.price
                if cash_position.market_value < total_cost:
                    return render(request, 'transactions.html', {'form': form})
                else:
                    cash_position.market_value -= Decimal(total_cost)
                    cash_position.save()
            elif transaction.type == 'sell':
                position = Position.objects.filter(user=request.user, symbol=transaction.symbol).first()
                if not position:
                    form.add_error('symbol', 'Position not found')
                    return render(request, 'transactions.html', {'form': form})
                if position.quantity < transaction.quantity:
                    form.add_error('quantity', 'Not enough shares to sell')
                    return render(request, 'transactions.html', {'form': form})
                else:
                    cash_position.market_value += transaction.quantity * transaction.price
                    cash_position.save()
                    if position.quantity == transaction.quantity:  # Full sell
                        position.delete()
                    else:  # Partial sell
                        position.quantity -= transaction.quantity
                        position.save()
            nyse = mcal.get_calendar('NYSE')
            schedule = nyse.schedule(start_date=transaction.timestamp.date(), end_date=transaction.timestamp.date())

            if len(schedule) == 0:
                form.add_error(None, 'Market is closed')
                return render(request, 'transactions.html', {'form': form})
            else:
                market_open = pd.Timestamp(schedule.iloc[0]['market_open'].strftime('%Y-%m-%d %H:%M:%S'))
                market_close = pd.Timestamp(schedule.iloc[0]['market_close'].strftime('%Y-%m-%d %H:%M:%S'))
                timestamp = pd.Timestamp(transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
                if timestamp < market_open or timestamp > market_close:
                    form.add_error(None, 'Market is closed')
                    return render(request, 'transactions.html', {'form': form})

            position = Position.objects.filter(user=request.user, symbol=transaction.symbol).first()
            if not position:
                position = Position(user=request.user, symbol=transaction.symbol)
            position.price = transaction.price
            position.cost = transaction.price
            position.price_return = (position.price - position.cost) / position.cost * 100
            if position.quantity is None:
                position.quantity = transaction.quantity
            else:
                position.quantity += transaction.quantity
            position.market_value = position.price * position.quantity
            position.percent_portfolio = position.market_value / (Position.objects.filter(user=request.user).aggregate(Sum('market_value'))['market_value__sum'] + cash_position.market_value) * 100
            position.save()
            cash_position.market_value -= transaction.price * transaction.quantity if transaction.type == 'buy' else -transaction.price * transaction.quantity
            cash_position.save()
            transaction.save()

            return redirect(reverse('transaction_success'))

    else:
        form = TransactionForm()
    return render(request, 'transactions.html', {'form': form, 'title': 'Create Transaction'})

def success_view(request):
    return render(request, 'transaction_success.html')