import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RV(models.Model):
    name = models.CharField(max_length=200)
    rv_class = models.CharField(max_length=100, help_text="e.g. Class A Motorhome, Class B Motorhome")
    luxury_level = models.CharField(max_length=100, help_text="e.g. High luxury RV, Medium luxury RV")
    price_per_day = models.CharField(max_length=50, help_text="e.g. Rs 9,990")
    capacity = models.CharField(max_length=100, help_text="e.g. 6 - 7 persons")
    amenities = models.TextField(help_text="Comma separated list of amenities")
    image = models.ImageField(upload_to='rv_images/', blank=True, null=True)
    fallback_image = models.URLField(
        default="https://images.unsplash.com/photo-1523987355523-c7b5b0dd90a7?w=1000&auto=format&fit=crop"
    )
    overall_rating = models.FloatField(
        default=4.5,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # 1. Automatically generate 30 days of price history if none exists
        if is_new and not self.price_history.exists():
            digits_only = ''.join(c for c in self.price_per_day if c.isdigit())
            base_price = int(digits_only) if digits_only else 9990
            
            for day_idx in range(1, 31, 5):
                price_var = base_price + random.choice([-500, -200, 0, 200, 400])
                RVPriceHistory.objects.create(
                    rv=self,
                    day=day_idx,
                    price=max(1000, price_var)  # Ensure price stays positive
                )

        # 2. Automatically generate default reviews matching your design mockup
        if is_new and not self.reviews.exists():
            sample_reviews = [
                {
                    "author": "Thor Odinson",
                    "comment": "Comfortable living while still being connected to mother nature. I loved everything about the experience, would definitely recommend!",
                    "rating": 4.5
                },
                {
                    "author": "Tony Stark",
                    "comment": "Incredible amenity setup, smooth ride, and high quality comfort. Everything exceeded expectations throughout the entire trip.",
                    "rating": 5.0
                }
            ]
            for rev in sample_reviews:
                RVReview.objects.create(
                    rv=self,
                    author=rev["author"],
                    comment=rev["comment"],
                    rating=rev["rating"]
                )


class RVRatingBreakdown(models.Model):
    rv = models.OneToOneField(RV, on_delete=models.CASCADE, related_name='ratings_breakdown')
    location = models.FloatField(default=5.0)
    rooms = models.FloatField(default=4.5)
    value = models.FloatField(default=4.1)
    cleanliness = models.FloatField(default=4.5)
    service = models.FloatField(default=4.9)
    sleep_quality = models.FloatField(default=5.0)

    def __str__(self):
        return f"Ratings for {self.rv.name}"


class RVReview(models.Model):
    rv = models.ForeignKey(RV, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.FloatField(default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.author} for {self.rv.name}"


class RVPriceHistory(models.Model):
    rv = models.ForeignKey(RV, on_delete=models.CASCADE, related_name='price_history')
    day = models.IntegerField(help_text="Day index (1 to 30)")
    price = models.IntegerField(help_text="Price for this day")

    class Meta:
        ordering = ['day']

    def __str__(self):
        return f"{self.rv.name} - Day {self.day}: Rs {self.price}"