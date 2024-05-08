import pytest
from django.contrib.admin import AdminSite

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin import RideAdmin
from apps.ride_manager.models.ride import Ride


class RideAdminTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.admin = RideAdmin(Ride, AdminSite())

    def test_list_display(self):
        # Given
        expected_list_display = [
            "origin",
            "destination",
            "date",
            "work_shift",
            "status",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        # Given
        expected_fields = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "driver",
            "notes",
            "status",
            "created_at",
            "updated_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_fields, "fields")

    def test_ordering(self):
        # Given
        expected_ordering = ["date"]

        # When/Then
        self.execute_admin_tests(expected_ordering, "ordering")

    def test_search_fields(self):
        # Given
        expected_search_fields = [
            "date",
            "origin__name",
            "destination__name",
            "driver__name",
        ]

        # When/Then
        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        # Given
        expected_list_filter = [
            "status",
            "destination__city",
        ]

        # When/Then
        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_readonly_fields(self):
        # Given
        expected_readonly_fields = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "driver",
            "status",
            "created_at",
            "updated_at",
        ]

        # When/Then
        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
