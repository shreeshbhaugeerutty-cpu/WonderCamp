from django.urls import path
from . import views


urlpatterns = [
    path("camping-vans/", views.camping_vans, name="camping_vans"),
    path("camping-vans/<int:rv_id>/", views.rv_details_by_id, name="rv_details_id"),
    path("camping-vans/<slug:slug>/", views.rv_detail, name="rv_detail"),
]