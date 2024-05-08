from django.contrib import admin

from apps.ride_manager.models import AffectedPlace


@admin.register(AffectedPlace)
class AffectedPlaceAdmin(admin.ModelAdmin):
    list_display = [
        "city",
        "main_person",
        "main_contact",
    ]
    fieldsets = [
        (
            "Informações Básicas",
            {
                "fields": [
                    "city",
                    "main_person",
                    "main_contact",
                    "address",
                    "informations",
                ]
            },
        ),
    ]
    ordering = ["city"]
    search_fields = ["city__name"]
    list_filter = ["city"]