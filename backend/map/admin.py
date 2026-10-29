from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Spot, SOSAlert

@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'latitude', 'longitude')
    list_filter = ('category',)

@admin.register(SOSAlert)
class SOSAlertAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'latitude', 'longitude', 'is_resolved')
    list_filter = ('is_resolved',)