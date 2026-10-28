from django.shortcuts import render
import json
from django.shortcuts import render, get_object_or_404
from .models import RV, RVRatingBreakdown

from django.http import Http404

def rv_details(request, rv_id):
    rv_id = int(rv_id)
    
    # Try fetching the database object
    try:
        rv_obj = RV.objects.get(id=rv_id)
    except RV.DoesNotExist:
        # Fallback dictionary if model instance doesn't exist yet
        rv_obj = None

    # Fetch reviews linked to this RV from database
    db_reviews = RVRatingBreakdown.objects.filter(rv_id=rv_id)
    
    rv_reviews = []
    for r in db_reviews:
        # Get rating count / stars safely
        stars = getattr(r, 'rating', 5)
        
        rv_reviews.append({
            'name': getattr(r, 'user_name', getattr(r, 'user', 'Guest')),
            'rating': '★' * stars + '☆' * (5 - stars) if isinstance(stars, int) else str(stars),
            'comment': getattr(r, 'review_text', getattr(r, 'comment', ''))
        })

    return render(request, 'RV/rvdetails.html', {
        'rv': rv_obj,
        'rv_id': rv_id,
        'rv_reviews': rv_reviews,
    })

# Full Dictionary with integrated reviews for all 3 RVs
RVS = {
    1: {
        "title": "Class A Motorhomes RV",
        "subtitle": "High luxury RV",
        "price": "Rs 16,500",
        "reviews": [
            {"name": "Sarah Jenkins", "rating": "★★★★★", "comment": "Absolute luxury on wheels! Super spacious and modern."},
            {"name": "David Miller", "rating": "★★★★★", "comment": "Drove across the coast smoothly. Worth every rupee."},
            {"name": "Elena Rostova", "rating": "★★★★☆", "comment": "Great experience, very clean interior and comfy beds."},
        ]
    },
    2: {
        "title": "Class B Motorhomes RV",
        "subtitle": "Medium luxury RV",
        "price": "Rs 12,000",
        "reviews": [
            {"name": "Mark Spencer", "rating": "★★★★★", "comment": "Easy to park and drive. Perfect size for small families."},
            {"name": "Chloe Bennett", "rating": "★★★★☆", "comment": "Very reliable camper van with great fuel efficiency."},
        ]
    },
    3: {
        "title": "Class C Motorhomes RV",
        "subtitle": "Medium luxury RV",
        "price": "Rs 7,800",
        "reviews": [
            {"name": "Thor Odinson", "rating": "★★★★★", "comment": "Comfortable living while still being connected to mother nature."},
            {"name": "Tony Stark", "rating": "★★★★★", "comment": "Top-tier luxury and smooth driving setup for high-end camping."},
            {"name": "Steve Rogers", "rating": "★★★★☆", "comment": "Exceptionally reliable vehicle with great sleeping arrangements."},
            {"name": "Natasha Romanoff", "rating": "★★★★☆", "comment": "Super clean interior, huge water capacity, and cozy beds."},
        ]
    },
}

def rv_details(request, rv_id):
    rv_id = int(rv_id)
    rv = RVS.get(rv_id)
    
    if rv is None:
        raise Http404("RV not found")
    
    # Extract reviews directly for context
    rv_reviews = rv.get("reviews", [])
    return render(request, 'RV/rvdetails.html', {
        'rv': rv,
        'rv_id': int(rv_id),  # Ensure rv_id is passed as an integer
    })

import random

def rv_details(request, rv_id):
    rv = RVS.get(int(rv_id))
    if rv is None:
        raise Http404("RV not found")
        
    # Example: Fetch 30-day price history array from your database/model
    # or generate relative to current price
    current_price = int(rv.get("price", "9990").replace("Rs", "").replace(",", "").strip())
    
    # Send history array to template
    price_history = [current_price * factor for factor in [1.0, 0.9, 1.1, 0.95, 1.05, 1.2, 0.9, 1.15, 1.0]]
    
    return render(request, 'RV/rvdetails.html', {
        'rv': rv, 
        'rv_id': int(rv_id),
        'price_history': price_history
    })

def camping_vans(request):
    return render(request, 'RV/rvexplorer.html')


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
    price_points = []

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

