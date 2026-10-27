from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class RV(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, help_text="e.g. High luxury RV")
    price = models.CharField(max_length=50, help_text="e.g. Rs 9,990")
    capacity = models.CharField(max_length=100, help_text="e.g. 6 - 7 persons")
    amenities = models.TextField(help_text="Comma separated list of amenities")
    image = models.ImageField(upload_to='rv_images/', blank=True, null=True)
    fallback_image = models.URLField(default="https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=1000&auto=format&fit=crop")
    overall_rating = models.FloatField(
        default=4.5,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return self.title


class RVRatingBreakdown(models.Model):
    rv = models.OneToOneField(RV, on_delete=models.CASCADE, related_name='ratings_breakdown')
    location = models.FloatField(default=5.0)
    rooms = models.FloatField(default=4.5)
    value = models.FloatField(default=4.1)
    cleanliness = models.FloatField(default=4.5)
    service = models.FloatField(default=4.9)
    sleep_quality = models.FloatField(default=5.0)

    def __str__(self):
        return f"Ratings for {self.rv.title}"


class RVReview(models.Model):
    rv = models.ForeignKey(RV, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.FloatField(default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author} for {self.rv.title}"


class RVPriceHistory(models.Model):
    rv = models.ForeignKey(RV, on_delete=models.CASCADE, related_name='price_history')
    day = models.IntegerField(help_text="Day index (1 to 30)")
    price = models.IntegerField(help_text="Price for this day")

    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"{self.rv.title} - Day {self.day}: Rs {self.price}"