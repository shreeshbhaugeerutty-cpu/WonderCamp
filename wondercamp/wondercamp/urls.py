"""
URL configuration for wondercamp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views
from backend.map import views as map_views
from backend.payments import views as payment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='home'),
    path('', include('backend.campsites.urls')),
    path('', include('backend.vehicles.urls')),
    path('', include('backend.accounts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', include('backend.bookings.urls')),
    path('notifications/',include ('backend.notifications.urls')),
    #  Map & SOS Routes
    path('map/', map_views.map_view, name='map'),
    path('sos/', map_views.sos_view, name='sos'),
    path('sos/trigger/', map_views.sos_trigger, name='sos_trigger'),

    #  Payment Routes
    path('payment/', payment_views.payment_view, name='payment'),
    path('payment/done/', payment_views.payment_done, name='payment_done'),
]

