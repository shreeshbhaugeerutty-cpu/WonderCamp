from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # FR 6.3: Operational Dashboard
    path('', views.operational_dashboard, name='dashboard'),

    # FR 6.1: Master Data
    path('master-data/', views.master_data_list, name='master_data'),

    # FR 6.2: Business Policies
    path('policies/', views.business_policies, name='business_policies'),

    # FR 6.4: Camping Catalogue Content
    path('catalogue/', views.manage_catalogue, name='manage_catalogue'),

    # FR 6.5: Audit Logs
    path('audit-logs/', views.audit_logs, name='audit_logs'),

    # FR 6.6: Operational Health Monitoring (named 'health' to match template)
    path('health/', views.system_health, name='health'),
]