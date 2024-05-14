from django.contrib import admin

from apps.ride_manager.models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        "model",
        "color",
        "plate",
        "is_active",
    ]
    search_fields = [
        "model",
        "plate",
    ]
    list_filter = [
        "is_verified",
        "is_active",
    ]
    ordering = ["model", "plate"]
    readonly_fields = [
        "uuid",
        # "person",
        # "model",
        # "color",
        # "plate",
        # "plate_picture",
        # "vehicle_picture",
        # "created_at",
        "updated_at",
    ]
