import json
from django.shortcuts import render, get_object_or_404
from .models import RV, RVRatingBreakdown


def rv_explorer(request):
    """View to list all RVs on the main explorer/camping-vans page."""
    rvs = RV.objects.all()
    return render(request, 'RV/rvexplorer.html', {'rvs': rvs})


def rv_details(request, rv_id=1):
    """View to display single RV details with dynamic images, ratings, and chart data."""
    rv_obj = get_object_or_404(RV, id=rv_id)

    # 1. Safe resolution for admin media uploads
    image_url = None
    if rv_obj.image:
        try:
            image_url = rv_obj.image.url
        except ValueError:
            image_url = None

    # 2. Dynamic static fallback per RV (e.g., images/image 1.png, images/image 3.png)
    static_fallback = f"images/image {rv_obj.id}.png"

    # 3. Direct query lookup for rating breakdown to guarantee retrieval
    breakdown = {}
    rating_obj = RVRatingBreakdown.objects.filter(rv=rv_obj).first()

    if rating_obj:
        breakdown = {
            'location': rating_obj.location,
            'rooms': rating_obj.rooms,
            'value': rating_obj.value,
            'cleanliness': rating_obj.cleanliness,
            'service': rating_obj.service,
            'sleep_quality': rating_obj.sleep_quality,
        }

    # 4. Price history chart points
    price_points = list(rv_obj.price_history.values_list('price', flat=True)) if hasattr(rv_obj, 'price_history') else []

    context = {
        'rv': {
            'id': rv_obj.id,
            'title': rv_obj.title,
            'subtitle': rv_obj.subtitle,
            'price': rv_obj.price,
            'capacity': rv_obj.capacity,
            'amenities': rv_obj.amenities,
            'image': image_url,
            'static_fallback': static_fallback,
            'fallback_image': rv_obj.fallback_image,
            'rating': rv_obj.overall_rating,
            'ratings_breakdown': breakdown,
            'reviews': rv_obj.reviews.all() if hasattr(rv_obj, 'reviews') else [],
            'price_history': json.dumps(price_points),
        }
    }
    return render(request, 'RV/rvdetails.html', context)