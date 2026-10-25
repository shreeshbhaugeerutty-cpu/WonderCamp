from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import SystemAuditLog, SystemHealthLog

def is_admin(user):
    """
    Check if the user is authenticated and has administrative permissions.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_formatted_admin_name(user):
    """
    Helper function to dynamically resolve and format the admin's full name.
    1. Checks first_name + last_name (e.g., set via Google Sign-In or Django Admin).
    2. Falls back to extracting and capitalizing the email prefix (e.g., angelinajolie@gmail.com -> Angelina Jolie).
    3. Falls back to formatting the username.
    4. Defaults to "Admin" if all else fails.
    """
    # 1. Try full name (First + Last)
    full_name = user.get_full_name().strip()
    if full_name:
        return full_name
    
    # 2. Fall back to email prefix formatting
    if user.email:
        email_prefix = user.email.split('@')[0]
        # Handles dots, underscores, and hyphens (e.g., angelina.jolie -> Angelina Jolie)
        formatted_email_name = email_prefix.replace('.', ' ').replace('_', ' ').replace('-', ' ').title()
        if formatted_email_name:
            return formatted_email_name

    # 3. Fall back to username
    if user.username:
        formatted_username = user.username.replace('.', ' ').replace('_', ' ').replace('-', ' ').title()
        if formatted_username:
            return formatted_username

    # 4. Ultimate fallback
    return "Admin"


@user_passes_test(is_admin, login_url='/login/')
def operational_dashboard(request):
    """
    Main Operational Admin Dashboard overview displaying system metrics,
    health bars, and audit logs on a single page.
    """
    audit_logs = SystemAuditLog.objects.all().order_by('-timestamp')[:10]
    health_logs = SystemHealthLog.objects.all().order_by('-timestamp')[:5]
    admin_name = get_formatted_admin_name(request.user)

    context = {
        'admin_name': admin_name,
        'audit_logs': audit_logs,
        'health_logs': health_logs,
    }
    return render(request, 'admin_dashboard/operational_dashboard.html', context)


@user_passes_test(is_admin, login_url='/login/')
def master_data(request):
    """
    Client Profile & Master Data Management sub-view (FR 6.1).
    """
    admin_name = get_formatted_admin_name(request.user)
    context = {
        'admin_name': admin_name,
    }
    return render(request, 'admin_dashboard/master_data.html', context)


@user_passes_test(is_admin, login_url='/login/')
def business_policies(request):
    """
    Business Policies & Operational Rules sub-view (FR 6.2).
    """
    admin_name = get_formatted_admin_name(request.user)
    context = {
        'admin_name': admin_name,
    }
    return render(request, 'admin_dashboard/business_policies.html', context)


@user_passes_test(is_admin, login_url='/login/')
def manage_catalogue(request):
    """
    Camping Catalogue Content Management sub-view (FR 6.4).
    """
    admin_name = get_formatted_admin_name(request.user)
    context = {
        'admin_name': admin_name,
    }
    return render(request, 'admin_dashboard/manage_catalogue.html', context)


@user_passes_test(is_admin, login_url='/login/')
def audit_logs(request):
    """
    System Audit Records & Compliance Logs sub-view (FR 6.5).
    """
    audit_logs_list = SystemAuditLog.objects.all().order_by('-timestamp')
    admin_name = get_formatted_admin_name(request.user)
    context = {
        'admin_name': admin_name,
        'audit_logs': audit_logs_list,
    }
    return render(request, 'admin_dashboard/audit_logs.html', context)


@user_passes_test(is_admin, login_url='/login/')
def health(request):
    """
    Operational System Health Monitoring sub-view (FR 6.6).
    """
    health_logs_list = SystemHealthLog.objects.all().order_by('-timestamp')
    admin_name = get_formatted_admin_name(request.user)
    context = {
        'admin_name': admin_name,
        'health_logs': health_logs_list,
    }
    return render(request, 'admin_dashboard/system_health.html', context)