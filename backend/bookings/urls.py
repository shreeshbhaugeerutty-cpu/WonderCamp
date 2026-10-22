from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create-booking/', views.create_booking, name='create_booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]