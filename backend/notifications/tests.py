from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationTestCase(TestCase):
    def setUp(self):
        # Authenticated Superuser matching all CustomUser required fields
        self.user, _ = User.objects.get_or_create(
            email='angelinajolie@gmail.com',
            defaults={
                'first_name': 'Angelina',
                'last_name': 'Jolie',
                'phone': '+230 5123 4567',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        self.user.set_password('1234')
        self.user.save()

        # Non-staff user for RBAC & user isolation testing
        self.other_user, _ = User.objects.get_or_create(
            email='camper1@gmail.com',
            defaults={
                'first_name': 'Camper',
                'last_name': 'One',
                'phone': '+230 5987 6543',
                'is_staff': False,
                'is_superuser': False,
                'is_active': True
            }
        )
        self.other_user.set_password('1234')
        self.other_user.save()

        # Baseline seed notifications
        Notification.objects.create(
            recipient=self.user,
            title='New Booking Confirmation',
            message='Client requested custom gear package for Black River campsite.',
            notification_type=Notification.NotificationType.BOOKING_CONFIRMATION
        )

        Notification.objects.create(
            recipient=self.user,
            title='System Health Alert',
            message='Database latency spiked by 12% during automated backup.',
            notification_type=Notification.NotificationType.GENERAL_ALERT
        )

    def test_dynamic_notification_creation_and_isolation(self):
        """Proves dynamic database insertion and user isolation with fresh data."""
        initial_count = Notification.objects.filter(recipient=self.user).count()
        self.assertEqual(initial_count, 2)

        # Dynamically inject a brand-new cyclone emergency notification
        new_alert = Notification.objects.create(
            recipient=self.user,
            title='Cyclone Warning Class 3',
            message='Torrential rain expected in Northern region. Seek shelter immediately.',
            notification_type=Notification.NotificationType.WEATHER_ALERT
        )

        # 1. Verify dynamic state change (Count increases from 2 to 3)
        updated_count = Notification.objects.filter(recipient=self.user).count()
        self.assertEqual(updated_count, 3)

        # 2. Verify recipient specificity and unread status
        self.assertEqual(new_alert.recipient.email, 'angelinajolie@gmail.com')
        self.assertFalse(new_alert.is_read)

        # 3. Verify camper1 remains completely isolated with 0 alerts
        self.assertEqual(Notification.objects.filter(recipient=self.other_user).count(), 0)

    def test_notification_state_mutation(self):
        """Verifies marking a notification as read dynamically mutates database state."""
        notif = Notification.objects.filter(recipient=self.user).first()
        self.assertFalse(notif.is_read)

        # Mutate notification state
        notif.is_read = True
        notif.save()

        # Assert database state changed
        refreshed_notif = Notification.objects.get(pk=notif.pk)
        self.assertTrue(refreshed_notif.is_read)