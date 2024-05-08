from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin import PersonAdmin
from apps.ride_manager.models.person import Person
from apps.ride_manager.tests.factories.person_factory import PersonFactory


class PersonAdminTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.person = PersonFactory()
        self.admin = PersonAdmin(Person, None)

    def test_list_display(self):
        expected_list_display = [
            "name",
            "phone",
            "birth_date",
            "cnh_is_verified",
            "document_is_verified",
            "profile_is_verified",
            "is_active",
        ]

        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fieldsets(self):
        expected_fieldsets = [
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

        self.execute_admin_tests(expected_fieldsets, "fieldsets")

    def test_search_fields(self):
        expected_search_fields = ["name", "phone"]

        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        expected_list_filter = [
            "profile_is_verified",
            "document_is_verified",
            "cnh_is_verified",
            "is_active",
        ]

        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_ordering(self):
        expected_ordering = ["name"]

        self.execute_admin_tests(expected_ordering, "ordering")

    def test_readonly_fields(self):
        expected_readonly_fields = [
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

        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
