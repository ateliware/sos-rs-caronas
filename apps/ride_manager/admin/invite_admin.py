from django.contrib import admin

from apps.ride_manager.models import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = [
        "ride",
        "voluntary",
        "status",
    ]
    fields = [
        "id",
        "ride",
        "voluntary",
        "status",
        "created_at",
        "updated_at",
        "is_active",
    ]

    ordering = [
        "-ride__date",
    ]
    search_fields = [
        "ride__destination",
        "ride__driver__name",
        "voluntary__person__name",
    ]
    list_filter = [
        "status",
    ]
    readonly_fields = [
        "id",
        "ride",
        "voluntary",
        "status",
        "created_at",
        "updated_at",
    ]
