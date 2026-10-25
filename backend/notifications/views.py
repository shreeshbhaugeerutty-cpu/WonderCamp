from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    
    # Send a quick test message to trigger the pop-up
    messages.info(request, "You have a new notification!")
    
    return render(request, 'notifications/notif.html', {
        'notifications': notifications
    })
