from django.shortcuts import render, redirect
from positions.models import Position
from paper_trader.forms import TransactionForm
import yfinance as yf
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Transaction
from user_accounts.models import AccountValue, UserAccount
from django.shortcuts import get_object_or_404
from decimal import Decimal

@login_required
def update_position_and_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            transaction_type = form.cleaned_data['type']
            symbol = form.cleaned_data['symbol']
            quantity = form.cleaned_data['quantity']
            notes = form.cleaned_data['notes']
            user_account = get_object_or_404(UserAccount, user=request.user)
            user = request.user
            price = Decimal(yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1])
            cost = price
            market_value = price * quantity
            
            # Get the position for this symbol if exists
            try:
                position = Position.objects.get(user=request.user, symbol=symbol)
            except Position.DoesNotExist:
                position = None

            # Create or update position
            if transaction_type == 'buy':
                if position is None:
                    position = Position.objects.create(
                    user=user,
                    symbol=symbol,                
                    quantity=quantity,
                    price=price,
                    cost = price,
                    price_return = ((price - cost) / price) * 100,
                    market_value = market_value,
                    percent_portfolio = market_value / (float(Position.objects.filter(user=request.user).aggregate(Sum('market_value'))['market_value__sum'])) * 100

                )
                    position.save()
                    cash_position = Position.objects.get(user=user, symbol='cash')
                    cash_position.quantity -= Decimal(price) * quantity
                    cash_position.market_value = cash_position.quantity * 1
                    cash_position.save()
                else:
                    new_quantity = position.quantity + quantity
                    new_cost = ((position.cost * position.quantity) + (price * quantity)) / new_quantity
                    position.quantity = new_quantity
                    position.cost = new_cost
                    position.save()
                    cash_position = Position.objects.get(user=user, symbol='cash')
                    cash_position.quantity -= price * quantity
                    cash_position.market_value = cash_position.quantity * 1
                    cash_position.save()
            elif transaction_type == 'sell':
                if position.quantity < quantity:
                    messages.error(request, "Not enough shares to sell")
                    return redirect('update_position_and_transaction')
                elif position.quantity == quantity:
                    #delete from positions
                    position_to_delete = Position.objects.get(user=user, symbol=symbol)
                    position_to_delete.delete()
                    # update cash quantity
                    cash_position = Position.objects.get(user=user, symbol='cash')
                    cash_position.quantity += price * quantity
                    cash_position.market_value = cash_position.quantity * 1
                    cash_position.save()
                else:
                    #update position for partial sell
                    position = Position.objects.get(user=user, symbol=symbol)
                    position.quantity -= quantity,
                    position.price = price,
                    position.price_return = ((price - cost) / price) * 100,
                    position.market_value = market_value,
                    position.percent_portoflio = market_value / (Position.objects.filter(user=request.user).aggregate(Sum('market_value'))['market_value__sum']) * 100
                    position.save()
                    cash_position = Position.objects.get(user=user, symbol='cash')
                    cash_position.quantity += price * quantity
                    cash_position.market_value = cash_position.quantity * 1
                    cash_position.save()
            

            # Create a new transaction
            transaction = Transaction.objects.create(
                user_account=user_account,
                user=user,
                type=transaction_type,
                symbol=symbol,
                quantity=quantity,
                price=price,
                notes=notes
            )
            transaction.save()

            # Update the account value
            get_positions = Position.objects.filter(user=request.user)
            account_value = AccountValue.objects.create(
                user_account = user_account,
                date=date.today(),
                value = sum([p.market_value for p in get_positions]),
                mtd_return = sum([p.market_value for p in get_positions]), #add last month value to calc
                ytd_return = sum([p.market_value for p in get_positions])  #add value earliest in current year to calc
            )
            account_value.save()

            # Redirect to the success page
            messages.success(request, "Transaction successful")
            return redirect('success.html') 

    else:
        form = TransactionForm()

    context = {
        'form': form
    }
    return render(request, 'transactions.html', context)

