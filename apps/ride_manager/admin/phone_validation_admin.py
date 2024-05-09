from django.contrib import admin

from apps.client_manager.models.phone_validation import PhoneValidation


@admin.register(PhoneValidation)
class PhoneValidationAdmin(admin.ModelAdmin):
    fields = [
        "uuid",
        "integration_sid",
        "phone",
        "created_at",
        "updated_at",
        "is_active",
    ]
    list_display = ["uuid", "phone", "is_active"]
    readonly_fields = [
        "uuid",
        "integration_sid",
        "phone",
        "created_at",
        "updated_at",
        "is_active",
    ]
    ordering = ["-created_at"]
