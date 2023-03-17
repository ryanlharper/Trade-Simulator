from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from positions.models import Position
from decimal import Decimal

@receiver(post_save, sender=get_user_model())
def create_user_positions(sender, instance, created, **kwargs):
    if created:
        cash_position = Position.objects.create(
            user=instance,
            symbol='cash',
            quantity=Decimal('100000'),
            price=Decimal('1.00'),
            cost=Decimal('1.00'),
        )

