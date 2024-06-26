from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin.voluntary_admin import VoluntaryAdmin
from apps.ride_manager.models.voluntary import Voluntary
from apps.ride_manager.tests.factories.voluntary_factory import VoluntaryFactory


class VoluntaryAdminTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.voluntary = VoluntaryFactory()
        self.admin = VoluntaryAdmin(Voluntary, None)

    def test_list_display(self):
        expected_list_display = [
            "person",
            "origin",
            "destination",
            "date",
            "work_shift",
            "status",
        ]

        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        expected_fields = [
            "id",
            "person",
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
            "status",
            "created_at",
            "updated_at",
            "is_active",
        ]

        self.execute_admin_tests(expected_fields, "fields")

    def test_ordering(self):
        expected_ordering = ["person"]

        self.execute_admin_tests(expected_ordering, "ordering")

    def test_search_fields(self):
        expected_search_fields = ["person__name"]

        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        expected_list_filter = [
            "origin",
            "destination",
            "date",
            "work_shift",
            "status",
        ]

        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_readonly_fields(self):
        expected_readonly_fields = [
            "id",
            "person",
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
            "status",
            "created_at",
            "updated_at",
        ]

        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
