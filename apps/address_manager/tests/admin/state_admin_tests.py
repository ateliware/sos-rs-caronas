from apps.address_manager.admin import StateAdmin
from apps.address_manager.models import State
from apps.address_manager.tests.factories.state_factory import StateFactory
from apps.core.tests.base_test import BaseTest


class StateAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.state = StateFactory()
        self.admin = StateAdmin(State, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "name",
            "code",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_fields, "fields")

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "name",
            "code",
        ]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "name",
        ]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")

    def test_list_filter(self):
        # Given
        expected_list_filter = [
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_filter, "list_filter")
