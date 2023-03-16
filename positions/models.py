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

class Comment(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('user_positions')
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('user_positions')