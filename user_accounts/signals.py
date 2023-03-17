from datetime import date
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from user_accounts.models import UserAccount, AccountValue

@receiver(post_save, sender=get_user_model())
def create_user_account(sender, instance, created, **kwargs):
    if created:
        user_account = UserAccount.objects.create(user=instance)
        today = date.today()
        AccountValue.objects.create(user_account=user_account, date=today, value=100000)


