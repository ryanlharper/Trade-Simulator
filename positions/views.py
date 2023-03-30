from django.shortcuts import render, get_object_or_404
from .models import Position
from django.contrib.auth.decorators import login_required
from .models import User, Position

@login_required
def positions_view(request):
    user = request.user
    positions = Position.objects.filter(user=user).order_by('symbol')

    position_data = []
    for position in positions:
        css_class_pct = 'positive' if position.price_return() >= 0 else 'negative_pct'
        css_class_dollar = 'positive' if position.dollar_return() >= 0 else 'negative_dollar'
        position_data.append({
            'position': position,
            'css_class_pct': css_class_pct,
            'css_class_dollar': css_class_dollar
        })

    context = {'position_data': position_data}
    return render(request, 'positions.html', context)

@login_required
def user_positions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    positions = Position.objects.filter(user=user).order_by('symbol')
    
    position_data = []
    for position in positions:
        css_class_dollar = 'positive' if position.dollar_return() >= 0 else 'negative_dollar'
        position_data.append({
            'position': position,
            'css_class_dollar': css_class_dollar
        })
    
    context = {
        'user': user,
        'position_data': position_data,
    }
    return render(request, 'user_positions.html', context)