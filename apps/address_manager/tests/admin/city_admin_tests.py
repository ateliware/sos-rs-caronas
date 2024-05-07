from apps.address_manager.admin import CityAdmin
from apps.address_manager.models import City
from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest


class CityAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.city = CityFactory()
        self.admin = CityAdmin(City, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "name",
            "state",
            "is_active",
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
            "name",
            "state",
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
            "name",
            "state__name",
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
            "state__name",
            "name",
        ]

        # When
        result = self.admin.ordering

        # Then
        self.assertEqual(expected_ordering, result)

    def test_list_filter(self):
        # Given
        expected_list_filter = [
            "is_active",
        ]

        # When
        result = self.admin.list_filter

        # Then
        for item in expected_list_filter:
            with self.subTest(item=item):
                self.assertIn(item, result)

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
