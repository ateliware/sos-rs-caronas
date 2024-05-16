from django.contrib import admin

from apps.ride_manager.models.vehicle import Vehicle


class VehicleInlineAdmin(admin.StackedInline):
    model = Vehicle
    extra = 0

    fields = (
        "is_verified",
        "model",
        "plate",
        "vehicle_picture",
        "plate_picture",
    )
    readonly_fields = [
        "uuid",
        "model",
        "plate",
        "plate_picture",
        "vehicle_picture",
        "created_at",
        "updated_at",
    ]
