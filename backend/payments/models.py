

# Create your models here.

from django.db import models
# Import your Booking model here, e.g., 
# from bookings.models import Booking

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mcb_juice', 'MCB Juice'),
        ('credit_card', 'Credit/Debit Card'),
    ]
    
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mcb_juice')
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_method_label(self):
        return dict(self.PAYMENT_METHODS).get(self.method, self.method)