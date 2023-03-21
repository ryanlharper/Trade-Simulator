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
    

       