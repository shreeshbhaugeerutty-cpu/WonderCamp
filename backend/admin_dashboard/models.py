from django.db import models
from django.conf import settings


class SystemAuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create Record'),
        ('UPDATE', 'Update Record'),
        ('DELETE', 'Delete Record'),
        ('SECURITY', 'Security Alert'),
        ('PAYMENT', 'Payment Confirmation'),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, default='UPDATE')
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class SystemHealthLog(models.Model):
    service_name = models.CharField(max_length=100)
    status_percentage = models.IntegerField(default=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.service_name}: {self.status_percentage}%"


class EmergencyAlert(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active Urgent Dispatch'),
        ('RESOLVED', 'Resolved & Safe'),
    ]

    client_name = models.CharField(max_length=150)
    campsite = models.CharField(max_length=255)
    details = models.TextField()
    contact = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_emergencies'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.client_name} - {self.campsite} ({self.status})"