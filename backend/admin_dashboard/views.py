from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import SystemAuditLog, SystemHealthLog

def is_admin(user):
    """
    Check if the user is authenticated and has staff or superuser privileges.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_formatted_admin_name(user):
    """
    Helper function to dynamically resolve and format the admin's greeting name.
    1. Checks first_name + last_name.
    2. Falls back to formatting email prefix (e.g. angelinajolie@gmail.com -> Angelina Jolie).
    3. Falls back to username.
    4. Defaults to "Admin".
    """
    full_name = user.get_full_name().strip()
    if full_name:
        return full_name
    
    if user.email:
        email_prefix = user.email.split('@')[0]
        return email_prefix.replace('.', ' ').replace('_', ' ').replace('-', ' ').title()

    if user.username:
        return user.username.replace('.', ' ').replace('_', ' ').replace('-', ' ').title()

    return "Admin"


@user_passes_test(is_admin, login_url='/login/')
def operational_dashboard(request):
    """
    Main Operational Admin Dashboard view.
    """
    # Pending items awaiting admin action (for header notification drawer)
    pending_notifications = [
        {
            'title': 'Awaiting Payment Confirmation',
            'details': 'Client Sarah Smith submitted receipt for Black River Gorges booking.',
            'time': '10 mins ago',
            'urgent': True
        },
        {
            'title': 'Pending Campsite Approval',
            'details': 'New listing submitted for Pieter Both site review.',
            'time': '45 mins ago',
            'urgent': False
        }
    ]

    # Historical completed logs
    audit_logs = SystemAuditLog.objects.all().order_by('-timestamp')[:10]
    health_logs = SystemHealthLog.objects.all().order_by('-timestamp')[:5]
    admin_name = get_formatted_admin_name(request.user)

    context = {
        'admin_name': admin_name,
        'notifications': pending_notifications,
        'audit_logs': audit_logs,
        'health_logs': health_logs,
    }
    return render(request, 'admin_dashboard/operational_dashboard.html', context)


@user_passes_test(is_admin, login_url='/login/')
def emergency_alerts(request):
    """
    Dedicated Emergency SOS Alerts Management View.
    """
    admin_name = get_formatted_admin_name(request.user)
    
    active_emergencies = [
        {
            'id': 1,
            'client_name': 'John Doe',
            'campsite': 'Black River Gorges - Site A4',
            'timestamp': '12 mins ago',
            'status': 'ACTIVE',
            'details': 'Medical assistance requested via SOS trigger.',
            'contact': '+230 5123 4567'
        },
        {
            'id': 2,
            'client_name': 'Linda Gironzmon',
            'campsite': 'Le Morne Coastal Trail',
            'timestamp': '2 hours ago',
            'status': 'RESOLVED',
            'details': 'Adverse weather guidance dispatch completed.',
            'contact': '+230 5987 6543'
        }
    ]

    context = {
        'admin_name': admin_name,
        'emergency_alerts': active_emergencies,
    }
    return render(request, 'admin_dashboard/emergency_alerts.html', context)


@user_passes_test(is_admin, login_url='/login/')
def master_data(request):
    """
    Client Profile & Master Data Management sub-view.
    """
    return render(request, 'admin_dashboard/master_data.html', {'admin_name': get_formatted_admin_name(request.user)})


@user_passes_test(is_admin, login_url='/login/')
def business_policies(request):
    """
    Business Policies & Operational Rules sub-view.
    """
    return render(request, 'admin_dashboard/business_policies.html', {'admin_name': get_formatted_admin_name(request.user)})


@user_passes_test(is_admin, login_url='/login/')
def manage_catalogue(request):
    """
    Camping Catalogue Content Management sub-view.
    """
    return render(request, 'admin_dashboard/manage_catalogue.html', {'admin_name': get_formatted_admin_name(request.user)})


@user_passes_test(is_admin, login_url='/login/')
def audit_logs(request):
    """
    System Audit Records & Compliance Logs sub-view.
    """
    return render(request, 'admin_dashboard/audit_logs.html', {
        'admin_name': get_formatted_admin_name(request.user),
        'audit_logs': SystemAuditLog.objects.all().order_by('-timestamp')
    })


@user_passes_test(is_admin, login_url='/login/')
def health(request):
    """
    Operational System Health Monitoring sub-view.
    """
    return render(request, 'admin_dashboard/system_health.html', {
        'admin_name': get_formatted_admin_name(request.user),
        'health_logs': SystemHealthLog.objects.all().order_by('-timestamp')
    })