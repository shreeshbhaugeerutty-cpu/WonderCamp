<<<<<<< HEAD

from django.urls import path
from . import views

urlpatterns = [
    path('camping-vans/', views.camping_vans, name='camping_vans'),
    path('camping-vans/<int:rv_id>/', views.rv_details, name='rv_details_id'),
]

=======
from django.urls import path
from . import views

app_name = "rv"

urlpatterns = [
    path("", views.rv_explorer, name="explorer"),
    path("<int:pk>/", views.rv_details, name="details"),
]
>>>>>>> sahil
