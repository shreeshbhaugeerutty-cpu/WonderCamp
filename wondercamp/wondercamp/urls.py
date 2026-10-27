from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend.vehicles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.placeholder, name='home'),
    path('list/', views.placeholder, name='list'),
    path('camping-vans/', views.placeholder, name='camping_vans'),
    path('rv-details/<int:pk>/', views.rv_detail, name='rv_detail'),
    path('rv-details/<int:pk>/', views.rv_detail, name='rv_details_id'),
    path('notifications/', include(('backend.notifications.urls', 'notifications'), namespace='notifications')),
    path('bookings/', include('backend.bookings.urls', namespace='bookings')),

    # Auth placeholders to resolve template links
    path('register/', views.placeholder, name='register'),
    path('logout/', views.placeholder, name='logout'),
    path('profile/', views.placeholder, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
