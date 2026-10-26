<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('camping-vans/', views.camping_vans, name='camping_vans'),
    path('camping-vans/<int:rv_id>/', views.rv_details, name='rv_details_id'),
]
=======
>>>>>>> sahil
