from django.contrib.admin import AdminSite

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin import RideOriginAdmin
from apps.ride_manager.models.ride_origin import RideOrigin
from apps.ride_manager.tests.factories.ride_origin_factory import (
    RideOriginFactory,
)


class RideOriginAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.ride_origin = RideOriginFactory()
        self.admin = RideOriginAdmin(RideOrigin, AdminSite())

    def test_list_display(self):
        # Given
        expected_list_display = [
            "city",
            "enabled",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "city",
            "enabled",
            "uuid",
            "created_at",
            "updated_at",
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
