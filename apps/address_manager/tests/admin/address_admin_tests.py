from apps.address_manager.admin import AddressAdmin
from apps.address_manager.models import Address
from apps.address_manager.tests.factories.address_factory import AddressFactory
from apps.core.tests.base_test import BaseTest


class AddressAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.address = AddressFactory()
        self.admin = AddressAdmin(Address, None)

    def test_list_display(self):
        # Given
        expected_list_display = [
            "user",
            "description",
            "street",
            "number",
            "city",
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
            "user",
            "description",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "zip_code",
            "is_active",
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
            "user__first_name",
            "city_name",
            "zip_code",
        ]

        # When
        result = self.admin.search_fields

        # Then
        for item in expected_search_fields:
            with self.subTest(item=item):
                self.assertIn(item, result)

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

    def test_ordering(self):
        # Given
        expected_ordering = [
            "user",
            "city",
        ]

        # When
        result = self.admin.ordering

        # Then
        for item in expected_ordering:
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
