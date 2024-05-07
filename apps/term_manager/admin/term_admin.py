from django.contrib import admin

from apps.term_manager.models import Term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        "version",
        "type",
    ]
    fields = [
        "id",
        "version",
        "type",
        "content",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "version",
        "type",
    ]
    ordering = [
        "id",
        "version",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
