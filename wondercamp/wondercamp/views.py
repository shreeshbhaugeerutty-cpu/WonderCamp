from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')


def landing(request):
    return render(request, 'landing.html')


def my_bookings(request):
    return render(request, 'bookings/mybooking.html')


def booking_summary(request):
    return render(request, 'bookings/booking.html')
