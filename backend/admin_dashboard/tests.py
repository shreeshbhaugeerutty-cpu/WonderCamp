from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import EmergencyAlert

User = get_user_model()


class AdminDashboardTestCase(TestCase):
    def setUp(self):
        self.admin_user, _ = User.objects.get_or_create(
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
        self.admin_user.set_password('1234')
        self.admin_user.save()

        self.regular_user, _ = User.objects.get_or_create(
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
        self.regular_user.set_password('1234')
        self.regular_user.save()

        # Baseline seed alert
        self.seed_alert = EmergencyAlert.objects.create(
            camper_name='Mark Taylor',
            location='Tamarind Falls - Pitch B2',
            message='Lost hiking gear near waterfall route.',
            contact_number='+230 5777 1122',
            status='ACTIVE'
        )

    def test_admin_dashboard_rbac_access(self):
        """Verifies security access control against non-staff accounts."""
        # Non-staff user (camper1) blocked
        self.client.login(email='camper1@gmail.com', password='1234')
        response = self.client.get(reverse('admin_dashboard:overview'))
        self.assertNotEqual(response.status_code, 200)

        # Admin superuser (angelinajolie@gmail.com) granted access
        self.client.login(email='angelinajolie@gmail.com', password='1234')
        response = self.client.get(reverse('admin_dashboard:overview'))
        self.assertEqual(response.status_code, 200)

    def test_dynamic_sos_creation_and_ranger_dispatch(self):
        """Proves dynamic database insertion and status transition with fresh UI data."""
        # 1. Dynamically create a brand-new emergency call
        new_sos = EmergencyAlert.objects.create(
            camper_name='Sarah Jenkins',
            location='Le Pouce Mountain Trail',
            message='Severe ankle sprain; emergency evacuation requested.',
            contact_number='+230 5999 4433',
            status='ACTIVE'
        )

        # Assert total active alerts dynamically changed from 1 to 2
        active_count = EmergencyAlert.objects.filter(status='ACTIVE').count()
        self.assertEqual(active_count, 2)

        # 2. Simulate Admin dispatching ranger (State Mutation: ACTIVE -> RESOLVED)
        new_sos.status = 'RESOLVED'
        new_sos.save()

        # Assert database record updated successfully
        refreshed_sos = EmergencyAlert.objects.get(pk=new_sos.pk)
        self.assertEqual(refreshed_sos.status, 'RESOLVED')
        self.assertEqual(EmergencyAlert.objects.filter(status='ACTIVE').count(), 1)