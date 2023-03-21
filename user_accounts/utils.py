from .models import AccountValue, UserAccount
from positions.models import Position
from datetime import date

def update_values():
    for user_account in UserAccount.objects.all():
        positions = Position.objects.filter(user=user_account.user)
        value = sum(p.market_value() for p in positions)
        latest_account_value = AccountValue.objects.filter(
            user_account=user_account).order_by('-date').first()
        # If there is no existing row for the user_account, create a new one
        if not latest_account_value:
            account_value = AccountValue(user_account=user_account, date=date.today(), value=value)
            account_value.save()
        # If the latest row has a date different than today, create a new one
        elif latest_account_value.date != date.today():
            account_value = AccountValue(user_account=user_account, date=date.today(), value=value)
            account_value.save()
        # If the latest row already has today's date, update its value
        else:
            latest_account_value.value = value
            latest_account_value.save()