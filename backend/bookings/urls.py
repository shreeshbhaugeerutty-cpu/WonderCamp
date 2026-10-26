
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create-booking/<int:campsite_id>/', views.create_booking, name='create_booking'),

    path('create-booking/<slug:campsite_slug>/', views.create_booking, name='create_booking'),

    path('confirmation/', views.confirmation, name='confirmation'),
    path('save-booking/<slug:campsite_slug>/', views.save_booking, name='save_booking'),
    path('my-bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/<int:booking_id>/modify/', views.modify_booking, name='modify_booking'),
    path('my-bookings/<int:booking_id>/update/', views.update_booking, name='update_booking'),
    path('my-bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
]
