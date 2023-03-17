from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from user_accounts.models import AccountValue, UserAccount
from django.views.generic import ListView
from user_accounts.models import AccountValue, UserAccount
from django.contrib.auth import get_user_model
from django.db.models import Max


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
        ).select_related('user_account')
        print("latest account values: ", latest_account_values) #test
        return latest_account_values.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_account_values = (
            UserAccount.objects
            .annotate(latest_account_value=Max('accountvalue__date'))
            .values('user__username', 'user_id', 'latest_account_value', 'accountvalue__value')
        )
        context['user_account_values'] = user_account_values
        return context




    