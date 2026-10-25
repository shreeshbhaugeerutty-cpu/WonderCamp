"""
URL configuration for WonderCamp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
from backend.map import views as map_views
from backend.payments import views as payment_views
=======
from . import views
>>>>>>> 55ee22bfe5250a618d8fa744ba257a9adddb9a43

urlpatterns = [
    # 1. Django standard admin (renamed to avoid prefix collision with custom admin)
    path('django-admin/', admin.site.urls),

    # 2. Main Landing & Auth
    path('', views.landing, name='home'),
    path('campsites/', include('backend.campsites.urls')),
    path('', include('backend.vehicles.urls')),
    path('', include('backend.accounts.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
<<<<<<< HEAD
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
=======
>>>>>>> 55ee22bfe5250a618d8fa744ba257a9adddb9a43

    # 3. Custom Admin Dashboard (FR 6.1 - FR 6.6)
    path('admin-dashboard/', include('backend.admin_dashboard.urls')),

    # 4. Teammate App Routes (Untouched)
    path('notifications/', include('backend.notifications.urls')),
    path('campsites/', include('backend.campsites.urls')),
    path('vehicles/', include('backend.vehicles.urls')),
    path('accounts/', include('backend.accounts.urls')),
    path('bookings/', include('backend.bookings.urls')),

    # 5. Google OAuth2 Login
    path("accounts/", include("allauth.urls")),
]