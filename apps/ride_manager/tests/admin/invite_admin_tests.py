from apps.core.tests.base_test import BaseTest
from apps.ride_manager.admin.invite_admin import InviteAdmin
from apps.ride_manager.models.invite import Invite
from apps.ride_manager.tests.factories.invite_factory import InviteFactory


class InviteAdminTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.invite = InviteFactory()
        self.admin = InviteAdmin(Invite, None)

    def test_list_display(self):
        expected_list_display = [
            "ride",
            "voluntary",
            "status",
        ]

        self.execute_admin_tests(expected_list_display, "list_display")

    def test_fields(self):
        expected_fields = [
            "id",
            "ride",
            "voluntary",
            "status",
            "created_at",
            "updated_at",
            "is_active",
        ]

        self.execute_admin_tests(expected_fields, "fields")

    def test_ordering(self):
        expected_ordering = ["-ride__date"]

        self.execute_admin_tests(expected_ordering, "ordering")

    def test_search_fields(self):
        expected_search_fields = [
            "ride__destination",
            "ride__driver__name",
            "voluntary__person__name",
        ]

        self.execute_admin_tests(expected_search_fields, "search_fields")

    def test_list_filter(self):
        expected_list_filter = [
            "status",
        ]

        self.execute_admin_tests(expected_list_filter, "list_filter")

    def test_readonly_fields(self):
        expected_readonly_fields = [
            "id",
            "ride",
            "voluntary",
            "status",
            "created_at",
            "updated_at",
        ]

        self.execute_admin_tests(expected_readonly_fields, "readonly_fields")
