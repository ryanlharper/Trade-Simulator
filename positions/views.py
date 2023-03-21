from django.shortcuts import render, get_object_or_404
from .models import Position
from django.contrib.auth.decorators import login_required
from .models import User, Position

@login_required
def positions_view(request):
    user = request.user
    positions = Position.objects.filter(user=user)
    context = {'positions': positions}
    return render(request, 'positions.html', context)

@login_required
def user_positions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    positions = Position.objects.filter(user=user)
    context = {
        'user': user,
        'positions': positions,
    }
    return render(request, 'user_positions.html', context)