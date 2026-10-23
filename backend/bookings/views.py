from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
# Temporary campsite data until Campsites backend is ready
TEMP_CAMPSITES = {
    76: {
        'name': 'Bois Chéri Private Camp',
        'location': 'Bois Chéri',
    },
    77: {
        'name': 'Black River Campsite',
        'location': 'Black River',
    },
}

from datetime import date
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
def create_booking(request, campsite_id):
    campsite = TEMP_CAMPSITES.get(campsite_id)

    if campsite is None:
        raise Http404("Campsite not found")
    campsite['id'] = campsite_id

    if request.method == 'POST':
        arrival = request.POST.get('arrival_date')
        departure = request.POST.get('departure_date')
        pitch = request.POST.get('pitch')
        campers = request.POST.get('campers')
        vehicles = request.POST.get('vehicles')
        pets = request.POST.get('pets')
        tents = request.POST.get('tents')
        
        valid_pitches = {
          'Hillside G-07': {
          'price': 2800,
          'campers': 4, 'vehicles': 1, 'pets': 2, 'tents': 2
          },
          'Lakeside Loft': {
          'price': 3500,
          'campers': 6, 'vehicles': 2, 'pets': 0, 'tents': 2
          },
          'Mountain Wild': {
          'price': 2500,
          'campers': 8, 'vehicles': 2, 'pets': 2, 'tents': 3
          },
          'Streamside Birch': {
          'price': 4800,
          'campers': 5, 'vehicles': 1, 'pets': 1, 'tents': 2
          },
        }


        if pitch not in valid_pitches:
            return render(request, 'bookings/booking.html', {
            'campsite': campsite,
            'error': 'Please select a valid pitch.'
          })
        try:
           campers = int(campers)
           vehicles = int(vehicles)
           pets = int(pets)
           tents = int(tents)
        except (ValueError, TypeError):
           return render(request, 'bookings/booking.html', {
             'campsite': campsite,
             'error': 'Please enter valid numbers of campers, vehicles, pets and tents.'
           })
        capacity = valid_pitches[pitch]

        if campers < 1 or campers > capacity['campers']:
          return render(request, 'bookings/booking.html', {
            'campsite': campsite,
            'error': 'The number of campers exceeds the allowed capacity.'
          })
        if vehicles < 0 or vehicles > capacity['vehicles']:
           return render(request, 'bookings/booking.html', {
            'campsite': campsite,
            'error': 'The number of vehicles exceeds the allowed capacity.'
          })
        

        if pets < 0 or pets > capacity['pets']:
           return render(request, 'bookings/booking.html', {
            'campsite': campsite,
            'error': 'The number of pets exceeds the allowed capacity.'
         })

        if tents < 0 or tents > capacity['tents']:
          return render(request, 'bookings/booking.html', {
           'campsite': campsite,
           'error': 'The number of tents exceeds the allowed capacity.'
         })




        try:
            arrival_date = date.fromisoformat(arrival)
            departure_date = date.fromisoformat(departure)
        except (ValueError, TypeError):
            error = "Please select valid arrival and departure dates."
        else:
            error = validate_booking_dates(arrival_date, departure_date)

        if error:
            return render(
                request,
                'bookings/booking.html',
                {
                    'campsite': campsite,
                    'error': error,
                }
            )
        
        # Dates are valid.
        # Booking will be saved in a later step.

        # Calculate number of nights
        number_of_nights = (departure_date - arrival_date).days

        # Get price of selected pitch
        price_per_night = valid_pitches[pitch]['price']

        # Calculate pitch cost
        pitch_fee = price_per_night * number_of_nights

        # Additional charges
        electricity_fee = 120 * number_of_nights
        water_fee = 420
        cleaning_fee = 188

        # Calculate total booking cost
        total_cost = pitch_fee + electricity_fee + water_fee + cleaning_fee

        print("Number of nights:", number_of_nights)
        print("Selected pitch:", pitch)
        print("Total booking cost: Rs", total_cost)
       

        return render(request, 'bookings/confirmation.html', {
        'campsite': campsite,
        'pitch': pitch,
        'arrival_date': arrival_date,
        'departure_date': departure_date,
        'number_of_nights': number_of_nights,
        'campers': campers,
        'vehicles': vehicles,
        'pets': pets,
        'tents': tents,
        'total_cost': total_cost,
        })
    
    return render(request, 'bookings/booking.html', {
        'campsite': campsite
    })

@login_required(login_url='login')
def confirmation(request):
    return render(request, 'bookings/confirmation.html')

@login_required(login_url='login')
def my_bookings(request):
    return render(request, 'bookings/mybooking.html')