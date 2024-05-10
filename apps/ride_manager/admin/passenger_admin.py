from django.contrib import admin

from apps.ride_manager.models.passenger import Passenger


class PassengerInlineAdmin(admin.TabularInline):
    model = Passenger
    extra = 1

    fields = (
        "person",
        "is_driver",
        "status",
    )

    readonly_fields = [
        "uuid",
        "person",
        "is_driver",
        "status",
    ]
