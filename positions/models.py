from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=8)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    
    def price_return(self):
        return ((self.price - self.cost) / self.price) * 100
    
    def market_value(self):
        return self.quantity * self.price

    def percent_portfolio(self):
        user_positions = Position.objects.filter(user=self.user)
        total_portfolio_value = sum(position.market_value() for position in user_positions)
        return (self.market_value() / total_portfolio_value) * 100

