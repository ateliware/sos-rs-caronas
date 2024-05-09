from django.core.exceptions import ValidationError

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.invite import Invite
from apps.ride_manager.tests.factories.invite_factory import InviteFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory
from apps.ride_manager.tests.factories.voluntary_factory import VoluntaryFactory


class InviteModelTests(BaseTest):
    def test_create_invite_model_instance(self):
        # Given
        expected_attrs = [
            "id",
            "voluntary",
            "status",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        invite = InviteFactory()
        db_invite = Invite.objects.get(id=invite.id)

        # Then
        self.assertIsInstance(invite, Invite)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(invite, attr_name)
                invite_attr = getattr(invite, attr_name)
                db_invite_attr = getattr(db_invite, attr_name)
                self.assertEqual(invite_attr, db_invite_attr)

    def test_invite_model_verbose_names(self):
        # Given
        expected_verbose_name = "Convite"
        expected_verbose_name_plural = "Convites"

        # When
        meta = Invite._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_invite_raise_exception_when_missing_required_fields(
        self,
    ):
        # Given
        test_cases = [
            "ride",
            "voluntary",
        ]
        ride = RideFactory()
        voluntary = VoluntaryFactory()

        for field in test_cases:
            with self.subTest(field=field):
                # When
                invite_data = {
                    "ride": ride,
                    "voluntary": voluntary,
                }
                invite_data[field] = None

                # Then
                with self.assertRaises(Exception):
                    Invite.objects.create(**invite_data)

    def test_invite_raise_exception_when_invalid_status(self):
        # Given
        invite_data = {
            "ride": RideFactory(),
            "voluntary": VoluntaryFactory(),
            "status": "invalid_status",
        }

        # When/Then
        with self.assertRaises(ValidationError):
            Invite.objects.create(**invite_data)
