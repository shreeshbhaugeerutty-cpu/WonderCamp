from django.contrib import admin

from .models import RV, RVComment, RVPriceHistory, RVRatingBreakdown


@admin.register(RV)
class RVAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "subtitle", "price")
    search_fields = ("title",)


@admin.register(RVRatingBreakdown)
class RVRatingBreakdownAdmin(admin.ModelAdmin):
    pass


@admin.register(RVPriceHistory)
class RVPriceHistoryAdmin(admin.ModelAdmin):
    pass


@admin.register(RVComment)
class RVCommentAdmin(admin.ModelAdmin):
    list_display = ("name", "rv_slug", "rating", "created_at")
    list_filter = ("rv_slug", "rating")