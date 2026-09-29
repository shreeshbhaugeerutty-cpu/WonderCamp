from django.conf import settings
from django.db import models

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    reference_no = models.CharField(max_length=50, unique=True)
    campsite_name = models.CharField(max_length=100, blank=True)
    campsite_location = models.CharField(max_length=150, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, blank=True)
    arrival_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    no_of_adults = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_children = models.PositiveIntegerField(default=0)
    no_of_vehicles = models.PositiveIntegerField(default=0)
    departure_date = models.DateField()
    cancellation_policy_snapshot = models.CharField(max_length=200)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.reference_no


class BookingLine(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    line_type = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.booking.reference_no} - {self.line_type}"