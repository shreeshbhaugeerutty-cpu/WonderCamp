from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from backend.bookings.models import Booking
from .models import Payment


class PaymentFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='pay@example.com', password='test')
        self.client.force_login(self.user)
        arrival = timezone.localdate() + timedelta(days=30)
        self.booking = Booking.objects.create(
            customer=self.user, reference_no='WC-TEST', campsite_name='Bois Cheri',
            total_cost=Decimal('2500.00'), arrival_date=arrival,
            departure_date=arrival + timedelta(days=3), cancellation_policy_snapshot='Test',
        )
        self.url = reverse('secure_checkout', args=[self.booking.pk])
        self.data = {'method': 'mcb_juice', 'mobile': '+230 55555555',
                     'email': self.user.email, 'country': 'Mauritius'}

    def test_checkout_completes_booking_and_duplicate_post_is_safe(self):
        self.assertContains(self.client.get(self.url), 'Rs 2500')
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'pending')
        response = self.client.post(self.url, {**self.data, 'amount': '1'}, follow=True)
        self.assertContains(response, 'Demo Payment Successful')
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'completed')
        self.assertEqual(self.booking.amount_paid, self.booking.total_cost)
        self.assertEqual(self.booking.payment_method, 'MCB Juice')
        self.client.post(self.url, self.data)
        self.assertEqual(Payment.objects.count(), 1)
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertContains(response, 'data-status="completed"')
        self.assertContains(response, 'Rs 2500.00')

    def test_invalid_payment_leaves_booking_pending(self):
        self.assertEqual(self.client.post(self.url, {**self.data, 'method': 'invalid'}).status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'pending')
        self.assertFalse(Payment.objects.exists())

    def test_cancelled_booking_cannot_be_paid(self):
        self.booking.status = 'cancelled'
        self.booking.save()
        self.client.post(self.url, self.data)
        self.assertFalse(Payment.objects.exists())

    def test_payment_pages_require_ownership(self):
        self.client.post(self.url, self.data)
        confirmation = reverse('payment_confirmation', args=[Payment.objects.get().pk])
        other = get_user_model().objects.create_user(email='other-pay@example.com', password='test')
        self.client.force_login(other)
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.post(self.url, self.data).status_code, 404)
        self.assertEqual(self.client.get(confirmation).status_code, 404)
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_save_booking_redirects_to_checkout_and_paid_dates_remain_reserved(self):
        self.booking.delete()
        arrival = timezone.localdate() + timedelta(days=40)
        data = {'arrival_date': arrival.isoformat(),
                'departure_date': (arrival + timedelta(days=3)).isoformat(),
                'campers': 4, 'vehicles': 0, 'pets': 0, 'tents': 1}
        url = reverse('bookings:save_booking', args=['bois-cheri'])
        response = self.client.post(url, data)
        booking = Booking.objects.get()
        self.assertRedirects(response, reverse('secure_checkout', args=[booking.pk]))
        self.client.post(reverse('secure_checkout', args=[booking.pk]), self.data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)
