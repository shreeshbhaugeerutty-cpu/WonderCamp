#helper function
#Whenever you process a booking or cancellation in your app, just call create_notification(user, title, message, request) from my notifications.utils file!
from .models import Notification
from django.contrib import messages

def create_notification(user, title, message, request=None):
    # 1. Save to database
    Notification.objects.create(
        recipient=user,
        title=title,
        message=message
    )
  
    if request:
        messages.info(request, f"New notification: {title}")