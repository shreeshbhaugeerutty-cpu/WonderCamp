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
        self.assertContains(response, 'class="bookings-body"')
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

    def test_save_for_later_reserves_dates_without_payment(self):
        response = self.client.post(self.save_url, {**self.data, 'action': 'save_for_later'})
        self.assertRedirects(response, reverse('bookings:my_bookings'))
        booking = Booking.objects.get(customer=self.user)
        self.assertEqual(booking.status, 'pending')
        self.assertEqual(booking.amount_paid, 0)
        self.assertEqual(booking.bookingline_set.count(), 6)
        self.assertNotIn('booking_review', self.client.session)
        listing = self.client.get(reverse('bookings:my_bookings'))
        self.assertContains(listing, reverse('secure_checkout', args=[booking.pk]))

        other = get_user_model().objects.create_user(email='later@example.com', password='test-password')
        self.client.force_login(other)
        response = self.client.post(self.save_url, {**self.data, 'action': 'save_for_later'})
        self.assertIn('This campsite is already booked', response.context['error'])
        self.assertEqual(Booking.objects.count(), 1)

    def test_save_for_later_rejects_invalid_dates(self):
        response = self.client.post(self.save_url, {
            **self.data, 'departure_date': self.data['arrival_date'], 'action': 'save_for_later',
        })
        self.assertTemplateUsed(response, 'bookings/booking.html')
        self.assertTrue(response.context['error'])
        self.assertFalse(Booking.objects.exists())

    def test_expiry_releases_dates_and_keeps_booking_in_history(self):
        self.client.post(self.save_url, {**self.data, 'action': 'save_for_later'})
        booking = Booking.objects.get()
        Booking.objects.filter(pk=booking.pk).update(
            created_at=timezone.now() - timedelta(hours=48),
        )
        response = self.client.get(reverse('bookings:my_bookings'))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'expired')
        self.assertContains(response, 'data-status="expired"')
        self.assertContains(response, 'Your reserved dates have been released.')
        self.assertNotContains(response, 'Pay Now')
        self.assertNotContains(response, 'Modify Booking')
        self.client.post(self.save_url, self.data)
        self.assertEqual(Booking.objects.count(), 2)

    def test_availability_expires_hold_without_visiting_my_bookings(self):
        self.client.post(self.save_url, self.data)
        booking = Booking.objects.get()
        Booking.objects.filter(pk=booking.pk).update(
            created_at=timezone.now() - timedelta(hours=49),
        )
        response = self.client.get(self.create_url)
        self.assertEqual(response.context['booked_ranges'], [])
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'expired')

    def test_unexpired_and_paid_bookings_are_preserved(self):
        self.client.post(self.save_url, self.data)
        booking = Booking.objects.get()
        Booking.objects.filter(pk=booking.pk).update(
            created_at=timezone.now() - timedelta(hours=47),
        )
        self.assertEqual(Booking.expire_pending(), 0)
        Booking.objects.filter(pk=booking.pk).update(
            created_at=timezone.now() - timedelta(hours=49), status='completed',
        )
        self.assertEqual(Booking.expire_pending(), 0)

    def test_expiry_command(self):
        from django.core.management import call_command
        from io import StringIO

        self.client.post(self.save_url, self.data)
        Booking.objects.update(created_at=timezone.now() - timedelta(hours=49))
        output = StringIO()
        call_command('expire_bookings', stdout=output)
        self.assertIn('Expired 1 unpaid booking(s).', output.getvalue())


class CampingVanBookingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='van@example.com', password='test')
        self.client.force_login(self.user)
        arrival = timezone.localdate() + timedelta(days=30)
        self.data = {
            'arrival_date': arrival.isoformat(),
            'departure_date': (arrival + timedelta(days=3)).isoformat(),
            'campers': 6, 'vehicles': 1, 'pets': 0, 'tents': 0,
        }
        self.create_url = reverse('bookings:create_booking', kwargs={'campsite_slug': 'rv-class-a'})
        self.save_url = reverse('bookings:save_booking', args=['rv-class-a'])

    def test_all_vans_link_to_booking_and_review(self):
        from backend.bookings.catalogue import VANS_BY_SLUG
        for van in VANS_BY_SLUG.values():
            with self.subTest(van=van['slug']):
                url = reverse('bookings:create_booking', kwargs={'campsite_slug': van['slug']})
                detail = self.client.get(reverse('rv_detail', args=[van['rv_slug']]))
                self.assertContains(detail, f'href="{url}"')
                page = self.client.get(url)
                self.assertTemplateUsed(page, 'bookings/booking.html')
                self.assertEqual(page.context['campsite']['max_tents'], 0)
                self.assertEqual(page.context['campsite']['max_pets'], 0)
                review = self.client.post(url, {**self.data, 'campers': van['min_campers']})
                self.assertTemplateUsed(review, 'bookings/confirmation.html')
                self.assertEqual(review.context['booking_review']['accommodationFee'], van['price'] * 3)
                self.assertContains(self.client.get(reverse('bookings:confirmation')), van['name'])

    def test_save_modify_availability_cancel_and_payment(self):
        response = self.client.post(self.save_url, {**self.data, 'action': 'save_for_later'})
        self.assertRedirects(response, reverse('bookings:my_bookings'))
        booking = Booking.objects.get()
        self.assertEqual(booking.bookingline_set.get(line_type='pets').quantity, 0)
        self.assertEqual(booking.bookingline_set.get(line_type='tents').quantity, 0)
        self.assertEqual(booking.bookingline_set.get(line_type='accommodation').item_name, 'rv-class-a')
        self.assertContains(self.client.get(reverse('bookings:booking_detail', args=[booking.pk])), 'Camping van')
        self.assertTrue(self.client.get(self.create_url).context['booked_ranges'])
        self.assertIn('camping van is already booked', self.client.post(self.save_url, self.data).context['error'])
        # Another van can still be booked for the same dates.
        other_url = reverse('bookings:create_booking', kwargs={'campsite_slug': 'rv-class-c'})
        self.assertTemplateUsed(self.client.post(other_url, self.data), 'bookings/confirmation.html')
        modify_url = reverse('bookings:modify_booking', args=[booking.pk])
        self.assertEqual(self.client.get(modify_url).status_code, 200)
        changed = {**self.data, 'campers': 7}
        self.assertTemplateUsed(self.client.post(modify_url, changed), 'bookings/confirmation.html')
        self.client.post(reverse('bookings:update_booking', args=[booking.pk]), changed)
        booking.refresh_from_db()
        self.assertEqual(booking.no_of_adults, 7)
        self.client.post(reverse('bookings:cancel_booking', args=[booking.pk]))
        self.assertEqual(self.client.get(self.create_url).context['booked_ranges'], [])
        self.client.post(self.save_url, self.data)
        booking = Booking.objects.filter(status='pending').get()
        response = self.client.post(reverse('secure_checkout', args=[booking.pk]), {
            'method': 'mcb_juice', 'mobile': '+230 55555555',
            'email': self.user.email, 'country': 'Mauritius',
        }, follow=True)
        self.assertTemplateUsed(response, 'payments/payment_confirmation.html')
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'completed')
        self.assertEqual(booking.amount_paid, booking.total_cost)

    def test_nonzero_pets_and_tents_rejected_on_create_save_and_update(self):
        self.client.post(self.save_url, self.data)
        booking = Booking.objects.get()
        for field in ('pets', 'tents'):
            for url in (self.create_url, self.save_url,
                        reverse('bookings:update_booking', args=[booking.pk])):
                with self.subTest(field=field, url=url):
                    response = self.client.post(url, {**self.data, field: 1})
                    self.assertIn(f'{field.capitalize()} must be between 0 and 0', response.context['error'])
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.bookingline_set.get(line_type='tents').quantity, 0)
