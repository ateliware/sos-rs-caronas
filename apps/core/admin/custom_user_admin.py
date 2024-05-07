from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.core.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.core.models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    list_filter = ["is_staff"]
    fieldsets = [
        (
            "Dados de acesso",
            {
                "fields": [
                    "email",
                    "password",
                ]
            },
        ),
        (
            "Informações pessoais",
            {
                "fields": [
                    "first_name",
                    "last_name",
                ]
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_staff",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (
            "Dados de acesso",
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password_1",
                    "password_2",
                ],
            },
        ),
    ]
    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]
    ordering = [
        "first_name",
        "last_name",
        "email",
    ]
    filter_horizontal = []


admin.site.register(CustomUser, CustomUserAdmin)
