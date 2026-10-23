from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    # Fetch all notifications belonging to the logged-in user, newest first
    notifications = Notification.objects.filter(recipient=request.user)
    
    return render(request, 'notifications/notif.html', {
        'notifications': notifications
})
