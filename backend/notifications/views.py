from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    return render(request, 'notifications/notif.html', {
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count(),
    })

@login_required
def mark_as_read(request, pk):
    """Marks a single notification as read and redirects back to the notifications list."""
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    messages.success(request, "Notification marked as read.")
    return redirect('notifications:list')