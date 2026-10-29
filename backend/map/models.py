from django.conf import settings
from django.db import models


class Spot(models.Model):
    CATEGORY_CHOICES = [
        ('sightseeing', 'Sightseeing'),
        ('nature', 'Nature'),
        ('beaches', 'Beaches'),
        ('adventure', 'Adventure'),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    blurb = models.TextField()
    image_filename = models.CharField(
        max_length=255,
        help_text="File name only, stored in frontend/static/images/ (e.g. black-river.jpg)",
    )

    def __str__(self):
        return self.name


class SOSAlert(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sos_alerts',
        help_text="Empty when the alert was sent by someone who was not logged in.",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True, help_text="GPS accuracy in metres")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, help_text="Last time the location was refreshed")
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='resolved_sos_alerts',
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"SOS at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    @property
    def has_location(self):
        return self.latitude is not None and self.longitude is not None

    @property
    def map_url(self):
        if not self.has_location:
            return ''
        lat, lng = self.latitude, self.longitude
        return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=17/{lat}/{lng}"

    @property
    def client_name(self):
        user = self.user
        if user is None:
            return 'Anonymous camper'
        name = ''
        if hasattr(user, 'get_full_name'):
            name = (user.get_full_name() or '').strip()
        return name or getattr(user, 'email', '') or 'Registered camper'