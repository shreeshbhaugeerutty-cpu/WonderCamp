from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST

from backend.campsites.models import Campsite, Pitch
from .dummy_data import ELECTRICITY_PER_NIGHT, WATER_FEE, CLEANING_FEE
from .models import Booking, BookingLine

CANCELLATION_POLICY = 'Free cancellation up to 7 days before arrival'


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


def is_pitch_available(campsite, pitch, arrival_date, departure_date, exclude_id=None):
    existing_bookings = BookingLine.objects.filter(
        line_type='pitch',
        item_name=pitch,
        booking__campsite_name=campsite.name,
        booking__status__in=['pending', 'confirmed'],
        start_date__lt=departure_date,
        end_date__gt=arrival_date,
    )

    if exclude_id:
        existing_bookings = existing_bookings.exclude(booking_id=exclude_id)

    return not existing_bookings.exists()


def get_costs(pitch, nights):
    pitch_fee = pitch.price_per_night * nights
    electricity_fee = ELECTRICITY_PER_NIGHT * nights
    total_cost = pitch_fee + electricity_fee + WATER_FEE + CLEANING_FEE

    return {
        'price_per_night': pitch.price_per_night,
        'pitch_fee': pitch_fee,
        'electricity_fee': electricity_fee,
        'water_fee': WATER_FEE,
        'cleaning_fee': CLEANING_FEE,
        'total_cost': total_cost,
    }


def show_form(request, campsite, error=None, existing=None, booking_id=None):
    return render(request, 'bookings/booking.html', {
        'campsite': campsite,
        'pitches': Pitch.objects.filter(campsite=campsite),
        'error': error,
        'existing': existing,
        'booking_id': booking_id,
    })


def save_lines(booking, b):
    nights = b['number_of_nights']
    add_line(booking, 'pitch', b['pitch'], nights, b['price_per_night'])
    add_line(booking, 'electricity', 'Electricity', nights, ELECTRICITY_PER_NIGHT)
    add_line(booking, 'water', 'Water Pack', 1, b['water_fee'])
    add_line(booking, 'cleaning', 'Cleaning Fee', 1, b['cleaning_fee'])
    add_line(booking, 'pets', 'Pets', b['pets'], 0)
    add_line(booking, 'tents', 'Tents / Grills', b['tents'], 0)


def add_line(booking, line_type, item_name, quantity, unit_price):
    BookingLine.objects.create(
        booking=booking,
        line_type=line_type,
        item_name=item_name,
        quantity=quantity,
        unit_price=unit_price,
        line_total=quantity * unit_price,
        start_date=booking.arrival_date,
        end_date=booking.departure_date,
    )


def check_booking_form(data, campsite, exclude_id=None):
    # returns (error, booking) - error is None if everything is ok
    pitch = Pitch.objects.filter(campsite=campsite, name=data.get('pitch')).first()

    if pitch is None:
        return 'Please select a valid pitch.', None

    try:
        campers = int(data.get('campers'))
        vehicles = int(data.get('vehicles'))
        pets = int(data.get('pets'))
        tents = int(data.get('tents'))
    except (ValueError, TypeError):
        return 'Please enter valid numbers of campers, vehicles, pets and tents.', None

    if campers < 1 or campers > pitch.max_campers:
        return 'The number of campers exceeds the allowed capacity.', None
    if vehicles < 0 or vehicles > pitch.max_vehicles:
        return 'The number of vehicles exceeds the allowed capacity.', None
    if pets < 0 or pets > pitch.max_pets:
        return 'The number of pets exceeds the allowed capacity.', None
    if tents < 0 or tents > pitch.max_tents:
        return 'The number of tents exceeds the allowed capacity.', None

    try:
        arrival_date = date.fromisoformat(data.get('arrival_date'))
        departure_date = date.fromisoformat(data.get('departure_date'))
    except (ValueError, TypeError):
        return 'Please select valid arrival and departure dates.', None

    error = validate_booking_dates(arrival_date, departure_date)
    if error:
        return error, None

    if not is_pitch_available(campsite, pitch.name, arrival_date, departure_date, exclude_id):
        return 'This pitch is already booked for the selected dates. Please choose another pitch or different dates.', None

    number_of_nights = (departure_date - arrival_date).days

    booking = {
        'pitch': pitch.name,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'number_of_nights': number_of_nights,
        'campers': campers,
        'vehicles': vehicles,
        'pets': pets,
        'tents': tents,
    }
    booking.update(get_costs(pitch, number_of_nights))

    return None, booking


@login_required(login_url='login')
def check_pitch_availability(request, campsite_id):
    campsite = get_object_or_404(Campsite, id=campsite_id)

    try:
        arrival_date = date.fromisoformat(request.GET.get('arrival_date', ''))
        departure_date = date.fromisoformat(request.GET.get('departure_date', ''))
    except ValueError:
        return JsonResponse({'error': 'Invalid dates'}, status=400)

    error = validate_booking_dates(arrival_date, departure_date)

    if error:
        return JsonResponse({'error': error}, status=400)

    exclude_id = request.GET.get('exclude')
    if exclude_id and not exclude_id.isdigit():
        exclude_id = None
    availability = {}

    for pitch in Pitch.objects.filter(campsite=campsite):
        availability[pitch.name] = is_pitch_available(
            campsite, pitch.name, arrival_date, departure_date, exclude_id
        )

    return JsonResponse(availability)


@login_required(login_url='login')
def create_booking(request, campsite_id):
    campsite = get_object_or_404(Campsite, id=campsite_id)

    if request.method == 'POST':
        error, booking = check_booking_form(request.POST, campsite)

        if error:
            return show_form(request, campsite, error)

        booking['campsite'] = campsite
        return render(request, 'bookings/confirmation.html', booking)

    return show_form(request, campsite)


@login_required(login_url='login')
@require_POST
def save_booking(request, campsite_id):
    campsite = get_object_or_404(Campsite, id=campsite_id)

    error, b = check_booking_form(request.POST, campsite)

    if error:
        return show_form(request, campsite, error)

    booking = Booking.objects.create(
        customer=request.user,
        reference_no=get_random_string(12),
        campsite_name=campsite.name,
        campsite_location=campsite.location,
        total_cost=b['total_cost'],
        arrival_date=b['arrival_date'],
        departure_date=b['departure_date'],
        no_of_adults=b['campers'],
        no_of_vehicles=b['vehicles'],
        cancellation_policy_snapshot=CANCELLATION_POLICY,
    )
    booking.reference_no = f"WC-{booking.created_at.year}-{booking.id:05d}"
    booking.save()

    save_lines(booking, b)

    messages.success(request, f"Booking {booking.reference_no} saved.")
    return redirect('bookings:my_bookings')


@login_required(login_url='login')
def booking_detail(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
    except Booking.DoesNotExist:
        raise Http404("Booking not found")

    lines = {}
    for line in booking.bookingline_set.all():
        lines[line.line_type] = line

    context = {
        'booking': booking,
        'campsite': {'name': booking.campsite_name, 'location': booking.campsite_location},
        'pitch': lines['pitch'].item_name,
        'arrival_date': booking.arrival_date,
        'departure_date': booking.departure_date,
        'number_of_nights': (booking.departure_date - booking.arrival_date).days,
        'campers': booking.no_of_adults,
        'vehicles': booking.no_of_vehicles,
        'pets': lines['pets'].quantity,
        'tents': lines['tents'].quantity,
        'price_per_night': lines['pitch'].unit_price,
        'pitch_fee': lines['pitch'].line_total,
        'electricity_fee': lines['electricity'].line_total,
        'water_fee': lines['water'].line_total,
        'cleaning_fee': lines['cleaning'].line_total,
        'total_cost': booking.total_cost,
    }
    return render(request, 'bookings/confirmation.html', context)


@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)

    for booking in bookings:
        if booking.status in ['cancelled', 'completed']:
            booking.filter_status = booking.status
        else:
            booking.filter_status = 'upcoming'

        pitch_line = booking.bookingline_set.filter(line_type='pitch').first()
        booking.pitch = pitch_line.item_name if pitch_line else ''
        booking.nights = (booking.departure_date - booking.arrival_date).days
        campsite = Campsite.objects.filter(name=booking.campsite_name).first()
        booking.campsite_id = campsite.id if campsite else 0

    return render(request, 'bookings/mybooking.html', {'bookings': bookings})


@login_required(login_url='login')
@require_POST
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
    except Booking.DoesNotExist:
        raise Http404("Booking not found")

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Booking {booking.reference_no} was cancelled.")
    else:
        messages.error(request, "This booking can not be cancelled.")

    return redirect('bookings:my_bookings')


def get_existing(booking):
    lines = {}
    for line in booking.bookingline_set.all():
        lines[line.line_type] = line

    return {
        'pitch': lines['pitch'].item_name,
        'arrival_date': booking.arrival_date,
        'departure_date': booking.departure_date,
        'campers': booking.no_of_adults,
        'vehicles': booking.no_of_vehicles,
        'pets': lines['pets'].quantity,
        'tents': lines['tents'].quantity,
    }


@login_required(login_url='login')
def modify_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
    except Booking.DoesNotExist:
        raise Http404("Booking not found")

    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, "This booking can not be modified.")
        return redirect('bookings:my_bookings')

    campsite = get_object_or_404(Campsite, name=booking.campsite_name)
    existing = get_existing(booking)

    if request.method == 'POST':
        error, b = check_booking_form(request.POST, campsite, booking.id)

        if error:
            return show_form(request, campsite, error, existing, booking.id)

        b['campsite'] = campsite
        b['modify_id'] = booking.id
        return render(request, 'bookings/confirmation.html', b)

    return show_form(request, campsite, existing=existing, booking_id=booking.id)


@login_required(login_url='login')
@require_POST
def update_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, customer=request.user)
    except Booking.DoesNotExist:
        raise Http404("Booking not found")

    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, "This booking can not be modified.")
        return redirect('bookings:my_bookings')

    campsite = get_object_or_404(Campsite, name=booking.campsite_name)
    error, b = check_booking_form(request.POST, campsite, booking.id)

    if error:
        return show_form(request, campsite, error, get_existing(booking), booking.id)

    with transaction.atomic():
        booking.arrival_date = b['arrival_date']
        booking.departure_date = b['departure_date']
        booking.no_of_adults = b['campers']
        booking.no_of_vehicles = b['vehicles']
        booking.total_cost = b['total_cost']
        booking.save()

        booking.bookingline_set.all().delete()
        save_lines(booking, b)

    messages.success(request, f"Booking {booking.reference_no} was updated.")
    return redirect('bookings:my_bookings')
