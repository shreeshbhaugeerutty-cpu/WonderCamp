from django.urls import path
from . import views

app_name = 'map'

urlpatterns = [
    path('', views.map_view, name='map'),
    path('sos/', views.sos_view, name='sos'),
    path('sos/trigger/', views.sos_trigger, name='sos_trigger'),
]