from django.contrib import admin

from apps.address_manager.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "state",
        "is_active",
    ]
    fields = [
        "id",
        "name",
        "state",
        "is_active",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "state__name",
    ]
    list_filter = [
        "is_active",
    ]
    ordering = [
        "state__name",
        "name",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
