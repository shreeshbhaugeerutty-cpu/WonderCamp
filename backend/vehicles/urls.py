from django.urls import path
from . import views

urlpatterns = [
    path('camping-vans/', views.camping_vans, name='camping_vans'),
]