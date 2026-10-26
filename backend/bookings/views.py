from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from backend.campsites.data import CAMPSITES_BY_SLUG


def validate_booking_dates(arrival_date, departure_date):
    today = timezone.localdate()

    if not arrival_date or not departure_date:
        return "Please select one arrival date and one departure date."

    if arrival_date <= today:
        return "Arrival date must be in the future."

    if departure_date <= arrival_date:
        return "Departure date must be after arrival date."

    if departure_date - arrival_date < timedelta(days=3):
        return "Minimum stay is 3 nights."

    return None


@login_required(login_url='login')
def create_booking(request, campsite_id=None, campsite_slug=None):
    # Preserve existing bookmarks while new links identify the campsite by slug.
    if campsite_slug is None:
        campsite_slug = {76: 'bois-cheri', 77: 'black-river'}.get(campsite_id)
    campsite = CAMPSITES_BY_SLUG.get(campsite_slug)
    if campsite is None:
        raise Http404("Campsite not found")

    context = {'campsite': campsite}
    previous_booking = request.session.get('booking_review', {})
    context['initial_booking'] = (
        previous_booking if previous_booking.get('campsite_slug') == campsite_slug else {}
    )
    if request.method == 'POST':
        try:
            counts = {key: int(request.POST.get(key, ''))
                      for key in ('campers', 'vehicles', 'pets', 'tents')}
        except (ValueError, TypeError):
            context['error'] = 'Please enter valid whole numbers for your party.'
            return render(request, 'bookings/booking.html', context)

        minimums = {'campers': campsite['min_campers'], 'vehicles': 0, 'pets': 0, 'tents': 1}
        for key, minimum in minimums.items():
            maximum = campsite['max_' + key]
            if not minimum <= counts[key] <= maximum:
                context['error'] = f'{key.capitalize()} must be between {minimum} and {maximum} for this campsite.'
                return render(request, 'bookings/booking.html', context)
        try:
            arrival = date.fromisoformat(request.POST.get('arrival_date', ''))
            departure = date.fromisoformat(request.POST.get('departure_date', ''))
        except (ValueError, TypeError):
            error = 'Please select valid arrival and departure dates.'
        else:
            error = validate_booking_dates(arrival, departure)
        if error:
            context['error'] = error
            return render(request, 'bookings/booking.html', context)

        nights = (departure - arrival).days
        accommodation = campsite['price'] * nights
        electricity, water, cleaning = 120 * nights, 420, 188
        context['booking_review'] = {
            'checkIn': arrival.isoformat(), 'checkOut': departure.isoformat(),
            'nights': nights, **counts, 'pricePerNight': campsite['price'],
            'accommodationFee': accommodation, 'electricity': electricity,
            'water': water, 'cleaning': cleaning,
            'total': accommodation + electricity + water + cleaning,
        }
        request.session['booking_review'] = {'campsite_slug': campsite_slug, **context['booking_review']}
        return render(request, 'bookings/confirmation.html', context)
    return render(request, 'bookings/booking.html', context)


@login_required(login_url='login')
def confirmation(request):
    review = request.session.get('booking_review')
    if not review or review.get('campsite_slug') not in CAMPSITES_BY_SLUG:
        from django.shortcuts import redirect
        return redirect('campsites:explorer')
    return render(request, 'bookings/confirmation.html', {
        'campsite': CAMPSITES_BY_SLUG[review['campsite_slug']], 'booking_review': review,
    })


@login_required(login_url='login')
def my_bookings(request):
    return render(request, 'bookings/mybooking.html')
