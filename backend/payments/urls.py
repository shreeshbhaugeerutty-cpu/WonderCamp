from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:booking_id>/', views.secure_checkout, name='secure_checkout'),
    path('confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
]