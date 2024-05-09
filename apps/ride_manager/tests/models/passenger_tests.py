import pytest

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.passenger import Passenger
from apps.ride_manager.tests.factories.passenger_factory import PassengerFactory
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory


class PassengerModelTests(BaseTest):
    def setUp(self):
        super().setUp()
        person = PersonFactory(user=self.user)
        ride = RideFactory(driver=person)
        self.passenger = PassengerFactory(person=person, ride=ride)

    def test_create_passenger_model_instance(self):
        # Given/When
        db_passenger = Passenger.objects.get(pk=self.passenger.pk)
        expected_db_passenger_str = (
            f"{db_passenger.person.name} - {db_passenger.ride}"
        )

        # Then
        self.assertIsInstance(self.passenger, Passenger)
        self.assertEqual(str(self.passenger), expected_db_passenger_str)

    def test_passenger_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Passageiro"
        expected_verbose_name_plural = "Passageiros"

        # When
        meta = Passenger._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_passenger_create_raise_exception_when_missing_required_fields(
        self,
    ):
        # Given
        test_cases = ["person", "ride", "is_driver", "status"]

        for attr_name in test_cases:
            # When
            with self.subTest(attr=attr_name):
                test_data = PassengerFactory.passenger_data()
                test_data[attr_name] = None
                with pytest.raises(Exception):
                    PassengerFactory(**test_data)
