from django.test import TestCase
from django.contrib.auth import get_user_model
from backend.notifications.models import Notification
from backend.notifications.utils import create_notification

User = get_user_model()

class NotificationTestCase(TestCase):
    def setUp(self):
        # Create a test superuser
        self.admin_user = User.objects.create_superuser(
            username="admin_test",
            email="admin@test.com",
            password="testpassword123"
        )

    def test_create_notification_utility(self):
        """Test that create_notification creates a valid DB entry."""
        notif = create_notification(
            user=self.admin_user,
            title="Test Alert",
            message="This is a test notification."
        )
        self.assertEqual(Notification.objects.count(), 1)
        self.assertFalse(notif.is_read)
        self.assertEqual(notif.user, self.admin_user)

    def test_mark_as_read(self):
        """Test marking a notification as read."""
        notif = create_notification(
            user=self.admin_user,
            title="Test Read",
            message="Testing read status update."
        )
        notif.is_read = True
        notif.save()
        
        updated_notif = Notification.objects.get(pk=notif.pk)
        self.assertTrue(updated_notif.is_read)
