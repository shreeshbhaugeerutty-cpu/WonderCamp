
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create-booking/<int:campsite_id>/', views.create_booking, name='create_booking'),

    path('check-pitch-availability/<int:campsite_id>/', views.check_pitch_availability, name='check_pitch_availability'),

    path('save-booking/<int:campsite_id>/', views.save_booking, name='save_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    
]
