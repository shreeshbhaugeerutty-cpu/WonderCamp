from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import MasterData, BusinessPolicy, SystemAuditLog, SystemHealthLog

def is_admin(user):
    return user.is_staff or user.is_superuser

# FR 6.3: Operational Dashboard
@user_passes_test(is_admin)
def operational_dashboard(request):
    audit_logs = SystemAuditLog.objects.all()[:5]
    health_logs = SystemHealthLog.objects.all()[:5]
    context = {
        'audit_logs': audit_logs,
        'health_logs': health_logs,
    }
    return render(request, 'admin_dashboard/operational_dashboard.html', context)

# FR 6.1: Master Data Management
@user_passes_test(is_admin)
def master_data_list(request):
    data = MasterData.objects.all()
    return render(request, 'admin_dashboard/master_data.html', {'master_data': data})

# FR 6.2: Business Policies & Rules
@user_passes_test(is_admin)
def business_policies(request):
    policies = BusinessPolicy.objects.all()
    return render(request, 'admin_dashboard/business_policies.html', {'policies': policies})

# FR 6.4: Public Catalogue Management (Placeholder context ready for catalogue app integration)
@user_passes_test(is_admin)
def manage_catalogue(request):
    return render(request, 'admin_dashboard/manage_catalogue.html', {})

# FR 6.5: Audit Logs
@user_passes_test(is_admin)
def audit_logs(request):
    logs = SystemAuditLog.objects.all()
    return render(request, 'admin_dashboard/audit_logs.html', {'audit_logs': logs})

# FR 6.6: Operational Health Monitoring
@user_passes_test(is_admin)
def system_health(request):
    logs = SystemHealthLog.objects.all()
    return render(request, 'admin_dashboard/system_health.html', {'health_logs': logs})