from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.db.models import Max, F

class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AccountValue(models.Model):
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2, default=100000)
    
    def mtd_return(self):
        last_month = date.today().replace(day=1) - timedelta(days=1) 
        start_of_month = last_month.replace(day=1)

        previous_month_value = AccountValue.objects.filter(
            user_account=self.user_account,
            date__range=(start_of_month, last_month)
        ).aggregate(Max('date'), value=F('value'))['value__max']

        if previous_month_value is not None:
            mtd_return = (self.value / previous_month_value - 1) * 100
        else:
            mtd_return = 0
        return mtd_return

    def ytd_return(self):
        start_of_year = date.today().replace(day=1, month=1) - timedelta(days=1)
        previous_year_value = AccountValue.objects.filter(
            user_account=self.user_account,
            date__lt=start_of_year,
            date__year=start_of_year.year
        ).order_by('-date').values_list('value', flat=True).first()
        if previous_year_value is not None:
            ytd_return = (self.value / previous_year_value - 1) * 100
        else:
            ytd_return = 0
        return ytd_return
       