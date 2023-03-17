from .models import AccountValue, UserAccount
from positions.models import Position
from datetime import date

def update_values():
    for user_account in UserAccount.objects.all():
        positions = Position.objects.filter(user=user_account.user)
        value = sum(p.market_value() for p in positions)
        accountvalue = AccountValue(user_account=user_account, date=date.today(), value=value)
        accountvalue.save()
