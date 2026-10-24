from django.db import models

# Create your models here.
class Campsite(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="campsites/", blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name