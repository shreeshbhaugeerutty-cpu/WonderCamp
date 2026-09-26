from django.db import models

# Create your models here.
class Booking(models.Model):
    reference_no = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.CharField(max_length=50)
    arrival_date = models.DateField()
    status = models.CharField(max_length=50)
    no_of_adults = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_children = models.IntegerField()
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
    quantity = models.IntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    end_date = models.DateField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.booking.reference_no} - {self.line_type}"