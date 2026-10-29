import json
import logging
import math

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.http import require_POST

from backend.notifications.models import Notification
from backend.notifications.utils import create_notification

from .models import SOSAlert, Spot

logger = logging.getLogger(__name__)

SESSION_KEY = "sos_alert_id"
# Per IP address. Keeps anonymous spam out of the admin queue; raise it if many
# campers share one IP (e.g. behind a proxy).
MAX_NEW_ALERTS_PER_HOUR = 10


def _spots(details=True):
    """Spots as plain dicts. details=True adds blurb, image and link for the map page."""
    spots = []
    for spot in Spot.objects.order_by("id"):
        item = {
            "id": spot.id,
            "name": spot.name,
            "category": spot.category,
            "lat": spot.latitude,
            "lng": spot.longitude,
        }
        if details:
            item.update(
                blurb=spot.blurb,
                # image_filename is just a file name, kept in frontend/static/images/
                image_url=static(f"images/{spot.image_filename}"),
                url="#",
            )
        spots.append(item)
    return spots


def map_view(request):
    return render(request, "maps/map.html", {"spots": _spots()})


def sos_view(request):
    return render(request, "maps/sos.html", {"spots": _spots(details=False)})


def _number(value, low, high):
    """Return a float within [low, high], or None if the value is missing."""
    if value in (None, ""):
        return None
    number = float(value)
    if not math.isfinite(number) or not low <= number <= high:
        raise ValueError("number out of range")
    return number


def _active_alert(request):
    """The unresolved alert this browser session already started, if any."""
    alert_id = request.session.get(SESSION_KEY)
    if not alert_id:
        return None
    return SOSAlert.objects.filter(pk=alert_id, is_resolved=False).first()


def _notify_admins(request, alert):
    """Drop an EMERGENCY_ALERT notification into every staff/superuser inbox."""
    User = get_user_model()
    admins = User.objects.filter(is_active=True).filter(Q(is_staff=True) | Q(is_superuser=True))
    dashboard_url = request.build_absolute_uri(reverse("admin_dashboard:emergency_alerts"))
    location = f"Location: {alert.map_url}" if alert.has_location else "No location was shared."
    message = f"{alert.client_name} sent an SOS alert. {location} Manage it here: {dashboard_url}"
    try:
        for admin in admins:
            create_notification(
                admin,
                "Emergency SOS alert",
                message,
                notification_type=Notification.NotificationType.EMERGENCY_ALERT,
            )
    except Exception:
        # The alert itself is already saved; never fail the SOS over a notification.
        logger.exception("Could not create SOS notifications for admins")


def _handle_alert(request, lat, lng, accuracy, is_update):
    alert = _active_alert(request)
    if alert:
        if lat is not None:
            alert.latitude, alert.longitude, alert.accuracy = lat, lng, accuracy
            alert.save(update_fields=["latitude", "longitude", "accuracy", "updated_at"])
        return JsonResponse({"status": "updated", "id": alert.id})

    if is_update:
        # Tracking ping for an alert that an admin has already resolved.
        return JsonResponse({"status": "closed"})

    key = f"sos-create:{request.META.get('REMOTE_ADDR', 'unknown')}"
    cache.add(key, 0, 3600)
    if cache.incr(key) > MAX_NEW_ALERTS_PER_HOUR:
        return JsonResponse(
            {"status": "error", "message": "Too many alerts from this device."}, status=429
        )

    # Location is optional: an alert without coordinates is still recorded.
    alert = SOSAlert.objects.create(
        user=request.user if request.user.is_authenticated else None,
        latitude=lat,
        longitude=lng,
        accuracy=accuracy,
    )
    request.session[SESSION_KEY] = alert.id
    _notify_admins(request, alert)
    return JsonResponse({"status": "sent", "id": alert.id})


@require_POST
def sos_trigger(request):
    """
    Called by the SOS page.
      - First press: creates an SOSAlert and notifies admins.
      - Later calls from the same browser session (the page sends {"update": true}
        every few seconds) refresh the location of that alert instead of creating
        a new one. Once an admin resolves it, the reply is {"status": "closed"}.
    Any failure is returned as JSON so the page can show what went wrong.
    """
    try:
        data = json.loads(request.body or "{}")
        if not isinstance(data, dict):
            raise ValueError("expected a JSON object")
        lat = _number(data.get("lat"), -90, 90)
        lng = _number(data.get("lng"), -180, 180)
        accuracy = _number(data.get("accuracy"), 0, 1_000_000)
        if (lat is None) != (lng is None):
            raise ValueError("lat and lng must be sent together")
        is_update = data.get("update") is True
    except (ValueError, TypeError):
        return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)

    try:
        return _handle_alert(request, lat, lng, accuracy, is_update)
    except Exception as exc:
        logger.exception("SOS alert failed")
        # With DEBUG on (development) show the real reason, e.g. a missing migration.
        message = f"{type(exc).__name__}: {exc}" if settings.DEBUG else "Could not save the alert."
        return JsonResponse({"status": "error", "message": message}, status=500)