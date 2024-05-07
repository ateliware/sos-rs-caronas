from django.contrib import admin

from apps.term_manager.models.term_acceptance import TermAcceptance


@admin.register(TermAcceptance)
class TermAcceptanceAdmin(admin.ModelAdmin):
    list_display = [
        "term",
        "user",
        "created_at",
    ]
    fields = [
        "id",
        "term",
        "user",
        "hashed_term",
        "created_at",
        "updated_at",
        "is_active",
    ]
    search_fields = [
        "term__version",
        "user__first_name",
    ]
    ordering = [
        "-id",
    ]
    readonly_fields = [
        "id",
        "hashed_term",
        "created_at",
        "updated_at",
    ]
