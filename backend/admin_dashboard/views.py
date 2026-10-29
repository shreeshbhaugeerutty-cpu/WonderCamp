import math

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from django.utils.timesince import timesince
from django.views.decorators.http import require_POST

from backend.map.models import SOSAlert, Spot
from .models import SystemAuditLog, SystemHealthLog
from .forms import AdminProfileForm


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


# ---------------------------------------------------------------------------
# SOS helpers
# ---------------------------------------------------------------------------

def _ago(moment):
    if (timezone.now() - moment).total_seconds() < 60:
        return 'just now'
    # timesince() gives "2 hours, 5 minutes"; keep the largest unit only.
    return f"{timesince(moment).split(',')[0]} ago"


def _distance_km(lat1, lng1, lat2, lng2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lng2 - lng1) / 2) ** 2)
    return 2 * 6371.0 * math.asin(math.sqrt(a))


def _nearest_spot(alert, spots):
    """Return 'Near <spot> (x.x km)' for the closest known spot within 10 km, else ''."""
    if not alert.has_location or not spots:
        return ''
    km, spot = min(
        ((_distance_km(alert.latitude, alert.longitude, s.latitude, s.longitude), s) for s in spots),
        key=lambda pair: pair[0],
    )
    return f"Near {spot.name} ({km:.1f} km)" if km <= 10 else ''


def _alert_to_dict(alert, spots):
    """
    Shape an SOSAlert like the dicts the Emergency Alerts template already
    renders (id, client_name, campsite, timestamp, status, details, contact),
    plus location fields for map links.
    """
    if alert.has_location:
        coords = f"{alert.latitude:.5f}, {alert.longitude:.5f}"
        near = _nearest_spot(alert, spots)
        campsite = f"{near} ({coords})" if near else coords
    else:
        campsite = 'Location not shared'

    details = ['SOS triggered from the WonderCamp app.']
    if alert.has_location:
        if alert.accuracy is not None:
            details.append(f"GPS accuracy about {round(alert.accuracy)} m.")
        details.append(f"Location updated {_ago(alert.updated_at)}.")
    else:
        details.append('No location was shared.')
    if alert.is_resolved and alert.resolved_at:
        who = f" by {get_formatted_admin_name(alert.resolved_by)}" if alert.resolved_by else ''
        details.append(f"Resolved {_ago(alert.resolved_at)}{who}.")

    user = alert.user
    contact = 'N/A'
    if user:
        contact = (
            getattr(user, 'phone_number', '')
            or getattr(user, 'phone', '')
            or getattr(user, 'email', '')
            or 'N/A'
        )

    return {
        'id': alert.id,
        'client_name': alert.client_name,
        'campsite': campsite,
        'timestamp': _ago(alert.timestamp),
        'status': 'RESOLVED' if alert.is_resolved else 'ACTIVE',
        'details': ' '.join(details),
        'contact': contact,
        'latitude': alert.latitude,
        'longitude': alert.longitude,
        'has_location': alert.has_location,
        'map_url': alert.map_url,
    }


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
        'active_sos_count': SOSAlert.objects.filter(is_resolved=False).count(),
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
    Emergency SOS Alerts Management & Dispatch View, fed by real SOSAlert rows
    created from the camper-facing SOS page (active alerts first, newest first).
    """
    admin_name = get_formatted_admin_name(request.user)

    spots = list(Spot.objects.only('name', 'latitude', 'longitude'))
    alerts = (
        SOSAlert.objects
        .select_related('user', 'resolved_by')
        .order_by('is_resolved', '-timestamp')[:100]
    )

    context = {
        'admin_name': admin_name,
        'emergency_alerts': [_alert_to_dict(a, spots) for a in alerts],
        'active_sos_count': SOSAlert.objects.filter(is_resolved=False).count(),
    }
    return render(request, 'admin_dashboard/emergency_alerts.html', context)


@user_passes_test(is_admin, login_url='/login/')
@require_POST
def resolve_emergency_alert(request, pk):
    """
    Mark an SOS alert as resolved. The camper's SOS page notices on its next
    location update and stops sharing.
    """
    alert = get_object_or_404(SOSAlert, pk=pk)
    if not alert.is_resolved:
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.save(update_fields=['is_resolved', 'resolved_at', 'resolved_by', 'updated_at'])
        messages.success(request, 'SOS alert marked as resolved.')
    return redirect('admin_dashboard:emergency_alerts')


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