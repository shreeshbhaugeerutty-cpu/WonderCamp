
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

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

    # 3. Custom Admin Dashboard (FR 6.1 - FR 6.6)
    path('admin-dashboard/', include('backend.admin_dashboard.urls')),

    # 4. Teammate App Routes (Untouched)
    path('notifications/', include('backend.notifications.urls')),
    path('campsites/', include('backend.campsites.urls')),
    path('vehicles/', include('backend.vehicles.urls')),
    path('accounts/', include('backend.accounts.urls')),
    path('bookings/', include('backend.bookings.urls')),
    path('payments/', include('backend.payments.urls')),

    # 5. Google OAuth2 Login
    path("accounts/", include("allauth.urls")),

    # 6. Map & SOS Feature
    path('map/', include('backend.map.urls')),
]
