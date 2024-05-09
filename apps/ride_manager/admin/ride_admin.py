from django.contrib import admin

from apps.ride_manager.admin.invite_admin import InviteInLineAdmin
from apps.ride_manager.admin.passenger_admin import PassengerInlineAdmin
from apps.ride_manager.models.ride import Ride


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = [
        "origin",
        "destination",
        "date",
        "work_shift",
        "status",
    ]
    fields = [
        "uuid",
        "date",
        "work_shift",
        "origin",
        "destination",
        "vehicle",
        "driver",
        "notes",
        "status",
        "created_at",
        "updated_at",
    ]
    ordering = ["date"]
    search_fields = [
        "date",
        "origin__name",
        "destination__name",
        "driver__name",
    ]
    list_filter = [
        "status",
        "destination__city",
    ]
    readonly_fields = [
        "uuid",
        "date",
        "work_shift",
        "origin",
        "destination",
        "vehicle",
        "driver",
        "status",
        "created_at",
        "updated_at",
    ]

    inlines = [
        PassengerInlineAdmin,
        InviteInLineAdmin,
    ]
