from django.contrib import admin

from apps.ride_manager.models import WorkAvailability


@admin.register(WorkAvailability)
class WorkAvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        "person",
        "origin",
        "destination",
        "date",
        "work_shift",
        "status",
    ]
    fields = [
        "id",
        "person",
        "origin",
        "destination",
        "any_destination",
        "date",
        "work_shift",
        "status",
        "created_at",
        "updated_at",
        "is_active",
    ]

    ordering = ["person"]
    search_fields = ["person__name"]
    list_filter = ["origin", "destination", "date", "work_shift", "status"]
    readonly_fields = ["id", "created_at", "updated_at"]
