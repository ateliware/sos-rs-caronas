from django.contrib import admin

from apps.ride_manager.models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    def cpf(self, obj):
        return obj.user.cpf

    cpf.short_description = "CPF"

    list_display = [
        "name",
        "phone",
        "birth_date",
        "cnh_is_verified",
        "document_is_verified",
        "profile_is_verified",
        "is_active",
    ]
    fieldsets = [
        (
            "Dados pessoais",
            {
                "fields": [
                    "uuid",
                    "user",
                    "name",
                    "birth_date",
                    "phone",
                    "avatar",
                ]
            },
        ),
        (
            "Endereço",
            {
                "fields": [
                    "city",
                    "zip_code",
                ]
            },
        ),
        (
            "Contato de emergência",
            {
                "fields": [
                    "emergency_phone",
                    "emergency_contact",
                ]
            },
        ),
        (
            "Documentos",
            {
                "fields": [
                    "cnh_number",
                    "cnh_picture",
                    "cpf",
                    "document_picture",
                ]
            },
        ),
        (
            "Status",
            {
                "fields": [
                    "cnh_is_verified",
                    "document_is_verified",
                    "profile_is_verified",
                    "is_active",
                ]
            },
        ),
    ]
    search_fields = [
        "name",
        "phone",
    ]
    list_filter = [
        "profile_is_verified",
        "document_is_verified",
        "cnh_is_verified",
        "is_active",
    ]
    ordering = [
        "name",
    ]
    readonly_fields = [
        "uuid",
        "user",
        "name",
        "phone",
        "emergency_phone",
        "emergency_contact",
        "birth_date",
        "avatar",
        "cnh_number",
        "cnh_picture",
        "cpf",
        "document_picture",
        "city",
        "zip_code",
        "created_at",
        "updated_at",
    ]
