from apps.core.tests.base_test import BaseTest
from apps.term_manager.admin import TermAcceptanceAdmin
from apps.term_manager.models import TermAcceptance
from apps.term_manager.tests.factories.term_acceptance_factory import (
    TermAcceptanceFactory,
)


class TermAcceptanceAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.term_acceptance = TermAcceptanceFactory()
        self.admin = TermAcceptanceAdmin(TermAcceptance, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "term",
            "user",
            "created_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "id",
            "term",
            "user",
            "hashed_term",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_fields, "fields")

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "term__version",
            "user__first_name",
        ]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "-id",
        ]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "id",
            "hashed_term",
            "created_at",
            "updated_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
