from django.contrib import admin
from .models import RV, RVRatingBreakdown, RVPriceHistory

@admin.register(RV)
class RVAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'price')
    search_fields = ('title',)

@admin.register(RVRatingBreakdown)
class RVRatingBreakdownAdmin(admin.ModelAdmin):
    # Uses __str__ representation automatically so it never breaks on missing field names
    pass

@admin.register(RVPriceHistory)
class RVPriceHistoryAdmin(admin.ModelAdmin):
    pass