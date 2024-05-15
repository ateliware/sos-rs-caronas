from django.contrib.admin import AdminSite

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin import AffectedPlaceAdmin
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)


class AffectedAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.affected_place = AffectedPlaceFactory()
        self.admin = AffectedPlaceAdmin(AffectedPlace, AdminSite())

    def test_list_display(self):
        # Given
        expected_list_display = [
            "city",
            "main_person",
            "main_contact",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "city",
            "main_person",
            "main_contact",
            "address",
            "informations",
            "uuid",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When/Then
        self.execute_admin_tests(expected_fields, "fields")

    def test_ordering(self):
        # Given
        expected_ordering = ["city"]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_search_fields(self):
        # Given
        expected_search_fields = ["city__name"]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        # Given
        expected_list_filter = ["city"]

        # When/Then
        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "uuid",
            "created_at",
            "updated_at", 
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
