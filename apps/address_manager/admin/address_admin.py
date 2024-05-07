from django.contrib import admin

from apps.address_manager.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "description",
        "street",
        "number",
        "city",
    ]
    fields = [
        "user",
        "description",
        "street",
        "number",
        "complement",
        "neighborhood",
        "city",
        "zip_code",
        "is_active",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "user__first_name",
        "city_name",
        "zip_code",
    ]
    list_filter = [
        "is_active",
    ]
    ordering = [
        "user",
        "city",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
