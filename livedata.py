# --- 1. SEED NOTIFICATION (Flash Flood Advisory) ---
from backend.notifications.models import Notification; from django.contrib.auth import get_user_model; Notification.objects.create(recipient=get_user_model().objects.get(email='angelinajolie@gmail.com'), title='Flash Flood Advisory', message='River levels rising rapidly near Black River Gorges trail. Evacuate low zones.', notification_type='WEATHER_ALERT', is_read=False)


# --- 2. SEED EMERGENCY ALERT (David Miller SOS) ---
from backend.admin_dashboard.models import EmergencyAlert; EmergencyAlert.objects.create(client_name='David Miller', campsite='Chamarel Trail - Sector 4', details='Severe ankle injury after trail fall; urgent medical transport required.', contact='+230 5888 9911', status='ACTIVE')