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
            "version",
            "type",
            "content",
            "created_at",
            "updated_at",
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
            "version",
            "type",
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
            "id",
            "version",
        ]

        # When
        result = self.admin.ordering

        # Then
        self.assertEqual(expected_ordering, result)

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

        # When
        result = self.admin.readonly_fields

        # Then
        for item in expected_readonly_fields:
            with self.subTest(item=item):
                self.assertIn(item, result)
