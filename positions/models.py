from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=8)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    price_return = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    market_value = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    percent_portfolio = models.DecimalField(max_digits=10, decimal_places=2, default=None)

    def update_position(self, transaction):
        if transaction.symbol == self.symbol:
            if transaction.type == 'buy':
                total_cost = self.quantity * self.cost_basis + transaction.quantity * transaction.price
                total_quantity = self.quantity + transaction.quantity
                self.cost_basis = total_cost / total_quantity
                self.quantity = total_quantity
            elif transaction.type == 'sell':
                self.quantity -= transaction.quantity

            self.save()

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