from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', views.profile, name='profile'),
    path('account/delete/', views.delete_account, name='delete_account'),
]