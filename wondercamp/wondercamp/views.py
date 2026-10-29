from django.apps import apps
from django.db import DatabaseError
from django.shortcuts import render


def _count(app_label, model_name):
    """Row count for a model, or 0 if the model or its table doesn't exist yet."""
    try:
        return apps.get_model(app_label, model_name).objects.count()
    except (LookupError, DatabaseError):
        return 0


def landing(request):
    return render(request, 'landing.html', {
        # Assumes the campsites app has a model called Campsite; rename if yours differs.
        'campsite_count': _count('campsites', 'Campsite'),
        'sight_count': _count('map', 'Spot'),
    })