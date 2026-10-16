from django.contrib import admin
from .models import RV, RVRatingBreakdown, RVReview, RVPriceHistory

class RVRatingBreakdownInline(admin.StackedInline):
    model = RVRatingBreakdown
    extra = 0

class RVReviewInline(admin.TabularInline):
    model = RVReview
    extra = 1

class RVPriceHistoryInline(admin.TabularInline):
    model = RVPriceHistory
    extra = 1

@admin.register(RV)
class RVAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'capacity', 'overall_rating')
    inlines = [RVRatingBreakdownInline, RVReviewInline, RVPriceHistoryInline]