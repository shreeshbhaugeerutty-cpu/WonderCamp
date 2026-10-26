from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone

from .models import SystemAuditLog, SystemHealthLog, EmergencyAlert
from .forms import AdminProfileForm
from backend.notifications.utils import create_notification


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
    Main Operational Admin Dashboard view.
    """
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

        # 2. Dynamic Notification Dispatch using helper function
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
def master_data(request):
    return render(request, 'admin_dashboard/master_data.html', {'admin_name': get_formatted_admin_name(request.user)})


@user_passes_test(is_admin, login_url='/login/')
def business_policies(request):
    return render(request, 'admin_dashboard/business_policies.html', {'admin_name': get_formatted_admin_name(request.user)})


@user_passes_test(is_admin, login_url='/login/')
def manage_catalogue(request):
    return render(request, 'admin_dashboard/manage_catalogue.html', {'admin_name': get_formatted_admin_name(request.user)})


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