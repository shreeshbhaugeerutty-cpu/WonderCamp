from django.urls import path
from . import views

app_name = "campsites"

urlpatterns = [
    path("", views.explorer, name="explorer"),             # /campsites/
    path("<int:pk>/", views.detail, name="detail"),        # /campsites/3/
]