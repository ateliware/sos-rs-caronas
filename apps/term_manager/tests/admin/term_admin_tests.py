from apps.core.tests.base_test import BaseTest
from apps.term_manager.admin import TermAdmin
from apps.term_manager.models import Term
from apps.term_manager.tests.factories.term_factory import TermFactory


class TermAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.term = TermFactory()
        self.admin = TermAdmin(Term, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "version",
            "type",
        ]

        # When/then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "id",
            "version",
            "type",
            "content",
            "created_at",
            "updated_at",
        ]

        # When/then
        self.execute_admin_tests(expected_fields, "fields")

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "version",
            "type",
        ]

        # When/then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_ordering(self):
        # Given
        expected_ordering = [
            "id",
            "version",
        ]

        # When/then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

        # When/then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
