import json
from django.shortcuts import render, get_object_or_404
from .models import RV

def placeholder(request):
    rvs = RV.objects.all()
    return render(request, 'RV/rvexplorer.html', {'rvs': rvs})

def rv_detail(request, pk):
    rv = get_object_or_404(RV, pk=pk)
    
    # Query price history ordered by day
    history = rv.price_history.order_by('day')
    days = [item.day for item in history]
    prices = [float(item.price) for item in history]
    
    context = {
        'rv': rv,
        'rating_breakdown': getattr(rv, 'ratings_breakdown', None),
        'reviews': rv.reviews.all(),
        'days_json': json.dumps(days),
        'prices_json': json.dumps(prices),
    }
    return render(request, 'RV/rvdetails.html', context)