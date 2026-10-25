from django.db import models
 
 
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
 
 
class Comment(models.Model):
    """A guest review left on a campsite detail page.
 
    The campsites themselves are hard-coded in data.py, so each comment
    stores the campsite's slug (e.g. "le-morne") to know where it belongs.
    """
 
    RATING_CHOICES = [
        (5, "5 - Excellent"),
        (4, "4 - Very good"),
        (3, "3 - Average"),
        (2, "2 - Poor"),
        (1, "1 - Terrible"),
    ]
 
    campsite_slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=60)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    @property
    def star_pct(self):
        """How much of the 5-star row to colour in (e.g. 4 stars = 80)."""
        return self.rating * 20
 
    def __str__(self):
        return f"{self.name} on {self.campsite_slug} ({self.rating}/5)"