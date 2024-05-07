from django.contrib import admin

from apps.address_manager.models import State


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
        "is_active",
    ]
    fields = [
        "id",
        "name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "code",
    ]
    list_filter = [
        "is_active",
    ]
    ordering = [
        "name",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
