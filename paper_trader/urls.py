"""paper_trader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from .views import SignUpView, LeaderboardView
from transactions.views import update_position_and_transaction, success_view, user_transactions_view, recent_transactions_view
from positions.views import positions_view, user_positions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', LeaderboardView.as_view(), name='home'),
    path('register/', SignUpView.as_view(), name='register'),
    path('transactions/', update_position_and_transaction, name='transactions'),
    path('user_transactions/', user_transactions_view, name='user_transactions'),
    path('recent_transactions/', recent_transactions_view, name='recent_transactions'),
    path('positions/', positions_view, name='positions'),
    path('positions/<int:user_id>/', user_positions, name='user_positions'),
    path('success/', success_view, name='success'),
]


