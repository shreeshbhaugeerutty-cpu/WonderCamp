from django.contrib import messages
from .models import Notification


def create_notification(
    user,
    title,
    message,
    request=None,
    notification_type=Notification.NotificationType.GENERAL_ALERT,
):
    """
    Save a notification to the database and optionally trigger a UI toast message.

    notification_type controls the icon and category (e.g. EMERGENCY_ALERT for SOS).
    Existing callers that pass only (user, title, message[, request]) keep working.
    """
    notification = Notification.objects.create(
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )

    if request:
        messages.info(request, f"New notification: {title}")

    return notification
