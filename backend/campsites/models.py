from django.db import models


class Campsite(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Pitch(models.Model):
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    price_per_night = models.PositiveIntegerField()
    max_campers = models.PositiveIntegerField()
    max_vehicles = models.PositiveIntegerField()
    max_pets = models.PositiveIntegerField()
    max_tents = models.PositiveIntegerField()

    def __str__(self):
        return self.campsite.name + ' - ' + self.name

