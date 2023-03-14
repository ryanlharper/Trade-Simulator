from django.db import models
from django.contrib.auth.models import User
from user_accounts.models import UserAccount

class Transaction(models.Model):
    user_account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    CHOICES = (
        ('buy', 'Buy to Open'),
        ('sell', 'Sell to Close'),
    )
    type = models.CharField(choices=CHOICES, max_length=100)
    symbol = models.CharField(max_length=8)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    notes = models.CharField(max_length=100, null=True)
    

