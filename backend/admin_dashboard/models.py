from django.db import models
from django.conf import settings

# FR 6.1: Master Data Management
class MasterData(models.Model):
    CATEGORY_CHOICES = [
        ('REGION', 'Camping Region'),
        ('ACTIVITY_TYPE', 'Activity Type'),
        ('EQUIPMENT', 'Camping Gear / Equipment'),
        ('AMENITY', 'Campsite Amenity'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"

# FR 6.2: Business Policies
class BusinessPolicy(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# FR 6.5: System Audit Log
class SystemAuditLog(models.Model):
    ACTION_TYPES = [
        ('PRICING_CHANGE', 'Pricing Change'),
        ('REFUND_ISSUED', 'Refund Issued'),
        ('ROLE_CHANGE', 'User Role Modified'),
        ('CATALOGUE_UPDATE', 'Catalogue Updated'),
        ('POLICY_CHANGE', 'Business Policy Modified'),
    ]
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    target_object = models.CharField(max_length=200)
    details = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action_type} - {self.timestamp}"

# FR 6.6: Operational Health Log
class SystemHealthLog(models.Model):
    STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('WARNING', 'Warning'),
        ('FAILED', 'Failed / Error'),
    ]
    COMPONENT_CHOICES = [
        ('PAYMENT_GATEWAY', 'Payment Gateway Integration'),
        ('NOTIFICATION_SERVICE', 'Notification Delivery (Email/SMS)'),
        ('BACKGROUND_JOBS', 'Scheduled / Failed Jobs'),
        ('DATABASE_BACKUP', 'Database Backups'),
        ('DATA_RETENTION', 'Data Retention Tasks'),
    ]
    component = models.CharField(max_length=50, choices=COMPONENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='HEALTHY')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.component} ({self.status})"