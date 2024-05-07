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

        # When
        result = self.admin.list_display

        # Then
        for item in expected_list_display:
            with self.subTest(item=item):
                self.assertIn(item, result)

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

        # When
        result = self.admin.fields

        # Then
        for item in expected_fields:
            with self.subTest(item=item):
                self.assertIn(item, result)

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "term__version",
            "user__first_name",
        ]

        # When
        result = self.admin.search_fields

        # Then
        for item in expected_search_fields:
            with self.subTest(item=item):
                self.assertIn(item, result)

    def test_ordering(self):
        # Given
        expected_ordering = [
            "-id",
        ]

        # When
        result = self.admin.ordering

        # Then
        self.assertEqual(expected_ordering, result)

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "id",
            "hashed_term",
            "created_at",
            "updated_at",
        ]

        # When
        result = self.admin.readonly_fields

        # Then
        for item in expected_readonly_fields:
            with self.subTest(item=item):
                self.assertIn(item, result)
