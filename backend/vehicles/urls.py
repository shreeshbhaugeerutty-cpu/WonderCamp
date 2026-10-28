from django.urls import path
from . import views

app_name = "rv"

urlpatterns = [
    path("", views.rv_explorer, name="explorer"),
    path("<int:pk>/", views.rv_details, name="details"),
]