from django.contrib import admin

from apps.ride_manager.models.ride_origin import RideOrigin


@admin.register(RideOrigin)
class RideOriginAdmin(admin.ModelAdmin):
    list_display = [
        "city",
        "enabled",
    ]
    fields = [
        "city",
        "enabled",
        "uuid",
        "created_at",
        "updated_at",
    ]

    ordering = ["city"]
    search_fields = ["city__name"]
    list_filter = ["city"]
    readonly_fields = [
        "uuid",
        "created_at",
        "updated_at",
    ]
