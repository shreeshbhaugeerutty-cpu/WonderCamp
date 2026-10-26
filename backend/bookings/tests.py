from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking
from backend.campsites.data import CAMPSITES


class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='camper@example.com', password='test-password')
        self.client.force_login(self.user)
        arrival = timezone.localdate() + timedelta(days=30)
        self.data = {
            'arrival_date': arrival.isoformat(),
            'departure_date': (arrival + timedelta(days=3)).isoformat(),
            'campers': 4, 'vehicles': 0, 'pets': 0, 'tents': 1,
        }
        self.create_url = reverse('bookings:create_booking', kwargs={'campsite_slug': 'bois-cheri'})
        self.save_url = reverse('bookings:save_booking', args=['bois-cheri'])

    def test_create_review_save_modify_and_cancel(self):
        response = self.client.get(self.create_url)
        self.assertContains(response, 'class="create-booking-body"')
        response = self.client.post(self.create_url, self.data)
        self.assertTemplateUsed(response, 'bookings/confirmation.html')
        self.assertContains(response, 'class="booking-summary-body"')
        self.assertEqual(self.client.get(reverse('bookings:confirmation')).status_code, 200)
        response = self.client.post(self.save_url, self.data, follow=True)
        self.assertTemplateUsed(response, 'payments/payment.html')
        booking = Booking.objects.get(customer=self.user)
        self.assertEqual(booking.bookingline_set.count(), 6)
        self.assertContains(response, booking.reference_no)
        self.assertEqual(self.client.get(reverse('bookings:booking_detail', args=[booking.pk])).status_code, 200)
        modify_url = reverse('bookings:modify_booking', args=[booking.pk])
        self.assertEqual(self.client.get(modify_url).status_code, 200)
        changed = {**self.data, 'campers': 5}
        self.assertTemplateUsed(self.client.post(modify_url, changed), 'bookings/confirmation.html')
        self.client.post(reverse('bookings:update_booking', args=[booking.pk]), changed)
        booking.refresh_from_db()
        self.assertEqual(booking.no_of_adults, 5)
        self.client.post(reverse('bookings:cancel_booking', args=[booking.pk]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_overlap_rejected_and_other_users_cannot_access_booking(self):
        self.client.post(self.save_url, self.data)
        booking = Booking.objects.get()
        response = self.client.post(self.save_url, self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('This campsite is already booked', response.context['error'])
        self.assertNotContains(response, 'This campsite is already booked')
        self.assertEqual(Booking.objects.count(), 1)
        other = get_user_model().objects.create_user(email='other@example.com', password='test-password')
        self.client.force_login(other)
        for name in ('booking_detail', 'modify_booking'):
            self.assertEqual(self.client.get(reverse('bookings:' + name, args=[booking.pk])).status_code, 404)
        for name in ('update_booking', 'cancel_booking'):
            self.assertEqual(self.client.post(reverse('bookings:' + name, args=[booking.pk]), self.data).status_code, 404)

    def test_all_campsite_detail_booking_and_review_pages(self):
        for site in CAMPSITES:
            with self.subTest(campsite=site['slug']):
                self.assertEqual(self.client.get(reverse('campsites:detail', args=[site['slug']])).status_code, 200)
                url = reverse('bookings:create_booking', kwargs={'campsite_slug': site['slug']})
                self.assertEqual(self.client.get(url).status_code, 200)
                data = {**self.data, 'campers': site['min_campers']}
                self.assertTemplateUsed(self.client.post(url, data), 'bookings/confirmation.html')

    def test_checkout_date_allows_another_checkin(self):
        self.client.post(self.save_url, self.data)
        arrival = timezone.localdate() + timedelta(days=33)
        next_stay = {
            **self.data,
            'arrival_date': arrival.isoformat(),
            'departure_date': (arrival + timedelta(days=3)).isoformat(),
        }
        self.assertEqual(self.client.post(self.save_url, next_stay).status_code, 302)
        self.assertEqual(Booking.objects.count(), 2)
