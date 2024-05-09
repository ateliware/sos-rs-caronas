from django.contrib import admin

from apps.ride_manager.models import Invite


class InviteInLineAdmin(admin.StackedInline):
    model = Invite
    extra = 0
    fields = [
        "id",
        "voluntary",
        "status",
        "created_at",
        "updated_at",
        "is_active",
    ]
    readonly_fields = [
        "id",
        "ride",
        "voluntary",
        "status",
        "created_at",
        "updated_at",
    ]
