
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create-booking/<int:campsite_id>/', views.create_booking, name='create_booking'),

    path('check-pitch-availability/<int:campsite_id>/', views.check_pitch_availability, name='check_pitch_availability'),

    path('confirmation/', views.confirmation, name='confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
]
