from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST

from .models import Booking, BookingLine
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


def active_campsite_bookings(campsite, exclude_booking_id=None):
    bookings = Booking.objects.filter(
        Q(campsite_name=campsite['name'])
        | Q(bookingline__line_type='accommodation', bookingline__item_name=campsite['slug']),
        status__in=('pending', 'confirmed', 'completed'),
    )
    if exclude_booking_id is not None:
        bookings = bookings.exclude(pk=exclude_booking_id)
    return bookings.distinct()


def render_booking(request, context):
    context['booked_ranges'] = [
        {'start': start.isoformat(), 'end': end.isoformat()}
        for start, end in active_campsite_bookings(context['campsite'], context.get('modify_id'))
        .filter(departure_date__gt=timezone.localdate())
        .values_list('arrival_date', 'departure_date')
    ]
    return render(request, 'bookings/booking.html', context)


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
        error, review = validate_review(request.POST, campsite)
        if error:
            context['error'] = error
            context['initial_booking'] = form_values(request.POST)
            return render_booking(request, context)
        context['booking_review'] = review
        request.session['booking_review'] = {'campsite_slug': campsite_slug, **review}
        return render(request, 'bookings/confirmation.html', context)
    return render_booking(request, context)


@login_required(login_url='login')
def confirmation(request):
    review = request.session.get('booking_review')
    if not review or review.get('campsite_slug') not in CAMPSITES_BY_SLUG:
        from django.shortcuts import redirect
        return redirect('campsites:explorer')
    return render(request, 'bookings/confirmation.html', {
        'campsite': CAMPSITES_BY_SLUG[review['campsite_slug']], 'booking_review': review,
    })




def validate_review(data, campsite, exclude_booking_id=None):
    context = {}
    try:
        counts = {key: int(data.get(key, ''))
                  for key in ('campers', 'vehicles', 'pets', 'tents')}
    except (ValueError, TypeError):
        context['error'] = 'Please enter valid whole numbers for your party.'
        return context['error'], None

    minimums = {'campers': campsite['min_campers'], 'vehicles': 0, 'pets': 0, 'tents': 1}
    for key, minimum in minimums.items():
        maximum = campsite['max_' + key]
        if not minimum <= counts[key] <= maximum:
            context['error'] = f'{key.capitalize()} must be between {minimum} and {maximum} for this campsite.'
            return context['error'], None
    try:
        arrival = date.fromisoformat(data.get('arrival_date', ''))
        departure = date.fromisoformat(data.get('departure_date', ''))
    except (ValueError, TypeError):
        error = 'Please select valid arrival and departure dates.'
    else:
        error = validate_booking_dates(arrival, departure)
    if error:
        context['error'] = error
        return context['error'], None

    overlapping = active_campsite_bookings(campsite, exclude_booking_id).filter(
        arrival_date__lt=departure, departure_date__gt=arrival,
    )
    if overlapping.exists():
        return ('This campsite is already booked for your selected dates. '
                'Please choose different dates.'), None

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
    return None, context['booking_review']


def form_values(data):
    values = {'checkIn': data.get('arrival_date', ''), 'checkOut': data.get('departure_date', '')}
    for key in ('campers', 'vehicles', 'pets', 'tents'):
        try:
            values[key] = int(data.get(key, ''))
        except (ValueError, TypeError):
            pass
    return values


def save_lines(booking, review, campsite):
    entries = [
        ('accommodation', campsite['slug'], review['nights'], review['pricePerNight']),
        ('electricity', 'Electricity', review['nights'], 120),
        ('water', 'Water pack', 1, 420), ('cleaning', 'Cleaning', 1, 188),
        ('pets', 'Pets', review['pets'], 0), ('tents', 'Tents', review['tents'], 0),
    ]
    for kind, name, quantity, price in entries:
        BookingLine.objects.create(
            booking=booking, line_type=kind, item_name=name, quantity=quantity,
            unit_price=price, line_total=quantity * price,
            start_date=booking.arrival_date, end_date=booking.departure_date,
        )


def booking_context(booking):
    lines = {line.line_type: line for line in booking.bookingline_set.all()}
    stay = lines.get('accommodation') or lines.get('pitch')
    campsite = CAMPSITES_BY_SLUG.get(stay.item_name) if stay else None
    if not campsite:
        campsite = next((site for site in CAMPSITES_BY_SLUG.values()
                         if site['name'] == booking.campsite_name), None)
    # Older bookings may reference a campsite name no longer in the catalogue.
    display_site = {**(campsite or {}), 'name': booking.campsite_name,
                    'location': booking.campsite_location}
    def cost(kind):
        return float(lines[kind].line_total) if kind in lines else 0
    review = {
        'checkIn': booking.arrival_date.isoformat(), 'checkOut': booking.departure_date.isoformat(),
        'nights': (booking.departure_date - booking.arrival_date).days,
        'campers': booking.no_of_adults, 'vehicles': booking.no_of_vehicles,
        'pets': lines['pets'].quantity if 'pets' in lines else 0,
        'tents': lines['tents'].quantity if 'tents' in lines else 1,
        'pricePerNight': float(stay.unit_price) if stay else 0,
        'accommodationFee': float(stay.line_total) if stay else 0,
        'electricity': cost('electricity'), 'water': cost('water'),
        'cleaning': cost('cleaning'), 'total': float(booking.total_cost),
    }
    return {'booking': booking, 'campsite': display_site, 'booking_review': review,
            'can_modify': bool(campsite) and booking.status in ('pending', 'confirmed')}


@login_required(login_url='login')
@require_POST
@transaction.atomic
def save_booking(request, campsite_slug):
    campsite = CAMPSITES_BY_SLUG.get(campsite_slug)
    if campsite is None:
        raise Http404('Campsite not found')
    error, review = validate_review(request.POST, campsite)
    if error:
        return render_booking(request, {
            'campsite': campsite, 'initial_booking': form_values(request.POST), 'error': error,
        })
    with transaction.atomic():
        booking = Booking.objects.create(
            customer=request.user, reference_no=get_random_string(32),
            campsite_name=campsite['name'], campsite_location=campsite['location'],
            total_cost=review['total'], arrival_date=review['checkIn'], departure_date=review['checkOut'],
            no_of_adults=review['campers'], no_of_vehicles=review['vehicles'],
            cancellation_policy_snapshot='',
        )
        booking.reference_no = f'WC-{booking.created_at.year}-{booking.id:05d}'
        booking.save(update_fields=['reference_no'])
        save_lines(booking, review, campsite)
    request.session.pop('booking_review', None)
    if request.POST.get('action') == 'save_for_later':
        messages.success(request, f'Booking {booking.reference_no} saved. Your dates are reserved; you can pay later from My Bookings.')
        return redirect('bookings:my_bookings')
    return redirect('secure_checkout', booking_id=booking.pk)


@login_required(login_url='login')
def my_bookings(request):
    bookings = list(Booking.objects.filter(customer=request.user).prefetch_related('bookingline_set'))
    for booking in bookings:
        context = booking_context(booking)
        booking.nights = context['booking_review']['nights']
        booking.image = context['campsite'].get('image', '')
        booking.can_modify = context['can_modify']
        booking.filter_status = booking.status if booking.status in ('cancelled', 'completed') else 'upcoming'
    return render(request, 'bookings/mybooking.html', {'bookings': bookings})


@login_required(login_url='login')
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    return render(request, 'bookings/confirmation.html', booking_context(booking))


@login_required(login_url='login')
def modify_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    context = booking_context(booking)
    if not context['can_modify']:
        messages.error(request, 'This booking cannot be modified.')
        return redirect('bookings:my_bookings')
    context['initial_booking'] = context['booking_review']
    context['modify_id'] = booking.id
    if request.method == 'POST':
        error, review = validate_review(request.POST, context['campsite'], booking.id)
        if error:
            context['error'] = error
            context['initial_booking'] = form_values(request.POST)
        else:
            context['booking_review'] = review
            context.pop('booking')
            return render(request, 'bookings/confirmation.html', context)
    return render_booking(request, context)


@login_required(login_url='login')
@require_POST
def update_booking(request, booking_id):
    with transaction.atomic():
        booking = get_object_or_404(Booking.objects.select_for_update(), pk=booking_id, customer=request.user)
        context = booking_context(booking)
        if not context['can_modify']:
            messages.error(request, 'This booking cannot be modified.')
            return redirect('bookings:my_bookings')
        error, review = validate_review(request.POST, context['campsite'], booking.id)
        if error:
            context.update(error=error, initial_booking=form_values(request.POST), modify_id=booking.id)
            return render_booking(request, context)
        booking.arrival_date = review['checkIn']
        booking.departure_date = review['checkOut']
        booking.no_of_adults = review['campers']
        booking.no_of_vehicles = review['vehicles']
        booking.total_cost = review['total']
        booking.save(update_fields=['arrival_date', 'departure_date', 'no_of_adults', 'no_of_vehicles', 'total_cost'])
        booking.bookingline_set.all().delete()
        save_lines(booking, review, context['campsite'])
    messages.success(request, f'Booking {booking.reference_no} updated.')
    return redirect('bookings:my_bookings')


@login_required(login_url='login')
@require_POST
def cancel_booking(request, booking_id):
    with transaction.atomic():
        booking = get_object_or_404(Booking.objects.select_for_update(), pk=booking_id, customer=request.user)
        if booking.status in ('pending', 'confirmed'):
            booking.status = 'cancelled'
            booking.save(update_fields=['status'])
            messages.success(request, f'Booking {booking.reference_no} cancelled.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
    return redirect('bookings:my_bookings')
