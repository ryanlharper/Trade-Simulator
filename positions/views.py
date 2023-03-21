from django.shortcuts import render, get_object_or_404, redirect
from .models import Position
from django.contrib.auth.decorators import login_required
from .models import User, Position, Comment, Reply
from django.contrib import messages
from paper_trader.forms import CommentForm

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
    comments = Comment.objects.filter(author=user)
    replies = Reply.objects.filter(comment__author=user)
    context = {
        'user': user,
        'positions': positions,
        'comments': comments,
        'replies': replies,
    }
    return render(request, 'user_positions.html', context)

@login_required
def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


@login_required
def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    position = comment.position
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text:
            messages.error(request, 'Reply cannot be empty.')
            return redirect('positions')  
        reply = Reply.objects.create(
            text=text,
            author=request.user,
            comment=comment
        )
        messages.success(request, 'Reply added.')
        return redirect('positions')  