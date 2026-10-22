from django.shortcuts import render


def create_booking(request):
    return render(request, 'bookings/booking.html')


def confirmation(request):
    return render(request, 'bookings/confirmation.html')


def my_bookings(request):
    return render(request, 'bookings/mybooking.html')