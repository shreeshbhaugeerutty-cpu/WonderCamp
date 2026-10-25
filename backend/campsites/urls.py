from django.urls import path
 
from . import views
 
app_name = "campsites"
 
urlpatterns = [
    path("", views.explorer, name="explorer"),                # /campsites/
    path("<slug:slug>/", views.detail, name="detail"),        # /campsites/le-morne/
]