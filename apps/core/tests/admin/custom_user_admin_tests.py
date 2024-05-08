from apps.core.admin import CustomUserAdmin
from apps.core.models import CustomUser
from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories import CustomUserFactory


class CustomUserAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.user = CustomUserFactory()
        self.admin = CustomUserAdmin(CustomUser, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "cpf",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_list_filter(self):
        # Given
        expected_list_filter = [
            "is_staff",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_fieldsets(self):
        # Given
        expected_access_fieldsets = ["cpf", "email", "password"]
        expected_personal_info_fieldsets = ["first_name", "last_name"]
        expected_permissions_fieldsets = [
            "is_staff",
            "groups",
            "user_permissions",
        ]

        # When
        result = self.admin.fieldsets

        # Then
        access_fieldsets_results = result[0][1]["fields"]
        for item in expected_access_fieldsets:
            with self.subTest(item=item):
                self.assertIn(item, access_fieldsets_results)

        personal_info_fieldsets_results = result[1][1]["fields"]
        for item in expected_personal_info_fieldsets:
            with self.subTest(item=item):
                self.assertIn(item, personal_info_fieldsets_results)

        permissions_fieldsets_results = result[2][1]["fields"]
        for item in expected_permissions_fieldsets:
            with self.subTest(item=item):
                self.assertIn(item, permissions_fieldsets_results)

    def test_add_fieldsets(self):
        # Given
        expected_add_fieldsets = [
            "cpf",
            "password_1",
            "password_2",
        ]

        # When
        result = self.admin.add_fieldsets

        # Then
        add_fieldsets_results = result[0][1]["fields"]
        for item in expected_add_fieldsets:
            with self.subTest(item=item):
                self.assertIn(item, add_fieldsets_results)

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "cpf",
            "first_name",
            "last_name",
        ]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "first_name",
            "last_name",
            "cpf",
        ]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")
