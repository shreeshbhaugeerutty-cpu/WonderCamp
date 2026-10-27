from django.contrib import admin
from .models import RV, RVReview, RVRatingBreakdown, RVPriceHistory


class RVReviewInline(admin.TabularInline):
    model = RVReview
    extra = 1


class RVPriceHistoryInline(admin.TabularInline):
    model = RVPriceHistory
    extra = 1


class RVRatingBreakdownInline(admin.StackedInline):
    model = RVRatingBreakdown
    extra = 0


@admin.register(RV)
class RVAdmin(admin.ModelAdmin):
    list_display = ('name', 'rv_class', 'price_per_day', 'overall_rating')
    search_fields = ('name', 'rv_class')
    inlines = [RVRatingBreakdownInline, RVReviewInline, RVPriceHistoryInline]


@admin.register(RVReview)
class RVReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'rv', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')


@admin.register(RVPriceHistory)
class RVPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('rv', 'day', 'price')
    list_filter = ('rv',)