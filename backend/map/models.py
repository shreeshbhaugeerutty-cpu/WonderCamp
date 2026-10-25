from django.db import models

# Create your models here.


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
    image_filename = models.CharField(max_length=255, help_text="Filename in wondercamp/img/")

    def __str__(self):
        return self.name

class SOSAlert(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"SOS at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"