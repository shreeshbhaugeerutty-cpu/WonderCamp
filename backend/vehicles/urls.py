from django.urls import path
from . import views

urlpatterns = [
    path('camping-vans/', views.rv_explorer, name='camping_vans'),
    path('rv-details/', views.rv_details, name='rv_details'),
    path('rv-details/<int:rv_id>/', views.rv_details, name='rv_details_id'),
]