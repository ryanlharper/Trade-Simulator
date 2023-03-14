from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.views.generic import ListView
from user_accounts.models import AccountValue, UserAccount
from django.contrib.auth import get_user_model

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'register.html'

class LeaderboardView(ListView):
    model = AccountValue
    template_name = 'home.html'

    def get_queryset(self):
        latest_account_values = AccountValue.objects.filter(
            id__in=AccountValue.objects.order_by('user_account', '-date').distinct('user_account')
        )
        return latest_account_values.order_by('-ytd_return')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        users = User.objects.filter(is_superuser=False)
        user_accounts = {}
        for user in users:
            try:
                user_account = UserAccount.objects.get(user=user)
                account_value = AccountValue.objects.filter(user_account=user_account).latest('date')
                mtd_return = account_value.mtd_return
                ytd_return = account_value.ytd_return
                user_accounts[user] = [mtd_return, ytd_return]
            except (UserAccount.DoesNotExist, AccountValue.DoesNotExist):
                pass
        context['user_accounts'] = user_accounts
        return context