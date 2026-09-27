from django.urls import path
from . import views

urlpatterns = [
    path('campsites/', views.campsites, name='campsites'),
]