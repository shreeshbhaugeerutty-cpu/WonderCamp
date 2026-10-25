from django.urls import path
from . import views
from .views import CustomLoginView, CustomPasswordChangeView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', views.profile, name='profile'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('account/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path("account/notifications/", views.notifications_profile, name="notifications_profile"),
    path('login/', CustomLoginView.as_view(), name='login'),
]