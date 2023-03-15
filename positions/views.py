from django.shortcuts import render
from .models import Position
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import User, Position, Comment, Reply

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
    comments = Comment.objects.filter(position__in=positions)
    replies = Reply.objects.filter(comment__position__in=positions)
    context = {
        'user': user,
        'positions': positions,
        'comments': comments,
        'replies': replies,
    }
    return render(request, 'user_positions.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Position, Comment, Reply

@login_required
def add_comment(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('user_positions', user_id=position.user.id)
        comment = Comment.objects.create(
            text=text,
            author=request.user,
            position=position
        )
        messages.success(request, 'Comment added.')
        return redirect('user_positions', user_id=position.user.id)

@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    position = comment.position
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            messages.error(request, 'Reply cannot be empty.')
            return redirect('user_positions', user_id=position.user.id)
        reply = Reply.objects.create(
            text=text,
            author=request.user,
            comment=comment
        )
        messages.success(request, 'Reply added.')
        return redirect('user_positions', user_id=position.user.id)

