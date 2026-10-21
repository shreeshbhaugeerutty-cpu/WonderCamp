from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        BOOKING_CONFIRMATION = 'BOOKING_CONFIRMATION', 'Booking Confirmation'
        BOOKING_AMENDED = 'BOOKING_AMENDED', 'Booking Amended'
        BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Booking Cancelled'
        REFUND_ISSUED = 'REFUND_ISSUED', 'Refund Processed/Accepted'
        SITE_CLOSED = 'SITE_CLOSED', 'Site Closed'
        WEATHER_ALERT = 'WEATHER_ALERT', 'Torrential Rain / Cyclone Warning'
        EVACUATION_ALERT = 'EVACUATION_ALERT', 'Evacuation Alert'
        CHECKIN_REMINDER = 'CHECKIN_REMINDER', 'Check-In Reminder'
        EMERGENCY_ALERT = 'EMERGENCY_ALERT', 'Emergency Alert'
        GENERAL_ALERT = 'GENERAL_ALERT', 'General Announcement'

    # Recipient can be a Client or an Admin (User model covers both)
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    
    notification_type = models.CharField(
        max_length=50, 
        choices=NotificationType.choices,
        default=NotificationType.GENERAL_ALERT
    )
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Displays newest notifications first

    def __str__(self):
        return f"{self.recipient.username} - {self.title} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def icon_class(self):
        """
        Maps notification types to CSS / FontAwesome icon classes matching Figma.
        """
        icon_map = {
            self.NotificationType.BOOKING_CONFIRMATION: 'fa-solid fa-check-double',
            self.NotificationType.BOOKING_AMENDED: 'fa-regular fa-pen-to-square',
            self.NotificationType.BOOKING_CANCELLED: 'fa-solid fa-xmark',
            self.NotificationType.REFUND_ISSUED: 'fa-solid fa-file-invoice-dollar',
            self.NotificationType.SITE_CLOSED: 'fa-solid fa-circle-xmark',
            self.NotificationType.WEATHER_ALERT: 'fa-solid fa-cloud-showers-heavy',
            self.NotificationType.EVACUATION_ALERT: 'fa-solid fa-triangle-exclamation',
            self.NotificationType.CHECKIN_REMINDER: 'fa-regular fa-clock',
            self.NotificationType.EMERGENCY_ALERT: 'fa-solid fa-bell',
        }
        return icon_map.get(self.notification_type, 'fa-regular fa-bell')


class NotificationPreference(models.Model):
    """
    Handles FR 3.4 & FR 3.5: Channel preferences and fallbacks.
    """
    class ChannelChoice(models.TextChoices):
        IN_APP = 'IN_APP', 'In-App Only'
        EMAIL = 'EMAIL', 'Email'
        SMS = 'SMS', 'SMS'

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='notification_preferences'
    )
    primary_channel = models.CharField(
        max_length=20, 
        choices=ChannelChoice.choices, 
        default=ChannelChoice.IN_APP
    )
    fallback_channel = models.CharField(
        max_length=20, 
        choices=ChannelChoice.choices, 
        default=ChannelChoice.EMAIL
    )

    def __str__(self):
        return f"{self.user.username} Preferences ({self.primary_channel} / {self.fallback_channel})"
