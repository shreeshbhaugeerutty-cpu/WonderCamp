from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone

# Model & Form Imports
from .models import SystemAuditLog, SystemHealthLog, EmergencyAlert
from .forms import AdminProfileForm, CampsiteForm, RVForm
from backend.notifications.models import Notification
from backend.notifications.utils import create_notification

# Resilient model imports supporting both app structures
try:
    from backend.campsites.models import Campsite
except ImportError:
    from campsites.models import Campsite

try:
    from backend.vehicles.models import RV
except ImportError:
    try:
        from vehicles.models import RV
    except ImportError:
        from backend.rvs.models import RV


def is_admin(user):
    """
    Check if the user is authenticated and has staff or superuser privileges.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def get_formatted_admin_name(user):
    """
    Helper function to dynamically resolve and format the admin's greeting name.
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
    Main Operational Admin Dashboard view with dynamic database notifications.
    Filters on recipient/user first, calculates count on unsliced QuerySet, then slices.
    """
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = user_notifications.filter(is_read=False).count()
    
    audit_logs = SystemAuditLog.objects.all().order_by('-timestamp')[:10]
    health_logs = SystemHealthLog.objects.all().order_by('-timestamp')[:5]
    admin_name = get_formatted_admin_name(request.user)

    context = {
        'admin_name': admin_name,
        'notifications': user_notifications[:5],
        'unread_count': unread_count,
        'audit_logs': audit_logs,
        'health_logs': health_logs,
    }
    return render(request, 'admin_dashboard/operational_dashboard.html', context)


@user_passes_test(is_admin, login_url='/login/')
def admin_profile(request):
    """
    Admin Profile & Account Settings view (edit names, email, change password).
    """
    admin_name = get_formatted_admin_name(request.user)

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = AdminProfileForm(request.POST, instance=request.user)
            password_form = PasswordChangeForm(request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile details updated successfully.')
                return redirect('admin_dashboard:profile')
        elif 'change_password' in request.POST:
            profile_form = AdminProfileForm(instance=request.user)
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('admin_dashboard:profile')
    else:
        profile_form = AdminProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'admin_name': admin_name,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'admin_dashboard/admin_profile.html', context)


@user_passes_test(is_admin, login_url='/login/')
def emergency_alerts(request):
    """
    Dynamic Interactive Emergency SOS Alerts Management & Dispatch View.
    """
    admin_name = get_formatted_admin_name(request.user)

    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        alert_obj = get_object_or_404(EmergencyAlert, pk=alert_id)

        alert_obj.status = 'RESOLVED'
        alert_obj.resolved_at = timezone.now()
        alert_obj.resolved_by = request.user
        alert_obj.save()

        # 1. System Audit Logging
        SystemAuditLog.objects.create(
            actor=request.user,
            action_type='SECURITY',
            details=f"Resolved emergency alert #{alert_obj.pk} for client {alert_obj.client_name}"
        )

        # 2. Dynamic Notification Dispatch
        create_notification(
            user=request.user,
            title="Emergency SOS Resolved",
            message=f"Unit dispatched & alert resolved for {alert_obj.client_name} at {alert_obj.campsite}.",
            request=request
        )

        messages.success(request, f"Emergency alert for {alert_obj.client_name} marked as RESOLVED.")
        return redirect('admin_dashboard:emergency_alerts')

    alerts = EmergencyAlert.objects.all().order_by('-timestamp')

    context = {
        'admin_name': admin_name,
        'emergency_alerts': alerts,
    }
    return render(request, 'admin_dashboard/emergency_alerts.html', context)


@user_passes_test(is_admin, login_url='/login/')
def manage_catalogue(request):
    """
    Manage Campsite and RV Catalogue Explorer entries independently.
    """
    campsites = Campsite.objects.all().order_by('-id')
    rvs = RV.objects.all().order_by('-id')

    campsite_form = CampsiteForm()
    rv_form = RVForm()

    if request.method == 'POST':
        # Campsite Actions
        if 'create_campsite' in request.POST:
            campsite_form = CampsiteForm(request.POST, request.FILES)
            if campsite_form.is_valid():
                campsite_form.save()
                messages.success(request, "New campsite listing added successfully!")
                return redirect('admin_dashboard:manage_catalogue')
        elif 'delete_campsite' in request.POST:
            campsite_id = request.POST.get('campsite_id')
            campsite = get_object_or_404(Campsite, pk=campsite_id)
            campsite.delete()
            messages.success(request, "Campsite listing removed.")
            return redirect('admin_dashboard:manage_catalogue')

        # RV / Vehicle Actions
        elif 'create_rv' in request.POST:
            rv_form = RVForm(request.POST, request.FILES)
            if rv_form.is_valid():
                rv_form.save()
                messages.success(request, "New RV listing added successfully!")
                return redirect('admin_dashboard:manage_catalogue')
        elif 'delete_rv' in request.POST:
            rv_id = request.POST.get('rv_id')
            rv = get_object_or_404(RV, pk=rv_id)
            rv.delete()
            messages.success(request, "RV listing removed.")
            return redirect('admin_dashboard:manage_catalogue')

    context = {
        'admin_name': get_formatted_admin_name(request.user),
        'campsites': campsites,
        'rvs': rvs,
        'campsite_form': campsite_form,
        'rv_form': rv_form,
    }
    return render(request, 'admin_dashboard/manage_catalogue.html', context)


@user_passes_test(is_admin, login_url='/login/')
def master_data(request):
    return render(request, 'admin_dashboard/master_data.html', {
        'admin_name': get_formatted_admin_name(request.user)
    })


@user_passes_test(is_admin, login_url='/login/')
def business_policies(request):
    return render(request, 'admin_dashboard/business_policies.html', {
        'admin_name': get_formatted_admin_name(request.user)
    })


@user_passes_test(is_admin, login_url='/login/')
def audit_logs(request):
    return render(request, 'admin_dashboard/audit_logs.html', {
        'admin_name': get_formatted_admin_name(request.user),
        'audit_logs': SystemAuditLog.objects.all().order_by('-timestamp')
    })


@user_passes_test(is_admin, login_url='/login/')
def health(request):
    return render(request, 'admin_dashboard/system_health.html', {
        'admin_name': get_formatted_admin_name(request.user),
        'health_logs': SystemHealthLog.objects.all().order_by('-timestamp')
    })