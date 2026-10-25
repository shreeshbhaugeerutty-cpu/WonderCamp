from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.operational_dashboard, name='dashboard'),
    path('master-data/', views.master_data, name='master_data'),
    path('business-policies/', views.business_policies, name='business_policies'),
    path('manage-catalogue/', views.manage_catalogue, name='manage_catalogue'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('health/', views.health, name='health'),
    path('emergency-alerts/', views.emergency_alerts, name='emergency_alerts'),
    path('profile/', views.admin_profile, name='profile'),
]