from rest_framework import status

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.passenger import (
    StatusChoices as PassengerStatusChoices,
)
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)
from apps.ride_manager.tests.factories.passenger_factory import PassengerFactory
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory
from apps.ride_manager.tests.factories.vehicle_factory import VehicleFactory


class RideSearchViewsetTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/rides/search/"
        self.person = PersonFactory(user=self.user)
        self.vehicle = VehicleFactory(person=self.person)
        self.ride = RideFactory(
            driver=self.person, vehicle=self.vehicle, quantity_of_passengers=4
        )
        self.passenger = PassengerFactory(
            ride=self.ride, status=PassengerStatusChoices.ACCEPTED
        )

    def test_search_rides(self):
        # Given
        expected_result_keys = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "status",
            "quantity_of_passengers",
            "confirmed_passengers",
            "created_at",
            "qtt_vacancies",
        ]

        # When
        response = self.auth_client.get(self.url)

        # Then
        response_data = response.json()
        response_ride = response_data[0]
        self.assertEqual(response.status_code, 200)

        for item in expected_result_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_ride.keys()))

        self.assertEqual(response_ride["quantity_of_passengers"], 4)
        self.assertEqual(response_ride["confirmed_passengers"], 1)
        self.assertEqual(response_ride["qtt_vacancies"], 3)

    def test_search_rides_filter_by_origin(self):
        # Given in setUp
        city = CityFactory()
        another_ride = RideFactory(origin=city)

        # When
        response = self.auth_client.get(self.url, {"origin": city.pk})

        # Then
        response_data = response.json()
        response_ride = response_data[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_ride["uuid"], str(another_ride.uuid))

    def test_search_rides_filter_by_destination(self):
        # Given in setUp
        city = CityFactory()
        affected_place = AffectedPlaceFactory(city=city)
        another_ride = RideFactory(destination=affected_place)

        # When
        response = self.auth_client.get(
            self.url, {"destination": affected_place.pk}
        )

        # Then
        response_data = response.json()
        response_ride = response_data[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_ride["uuid"], str(another_ride.uuid))

    def test_method_get_for_not_allowed(self):
        # Given
        test_cases = [
            self.auth_client.post,
            self.auth_client.put,
            self.auth_client.patch,
            self.auth_client.delete,
        ]
        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED

        # When
        for api_client in test_cases:
            response = api_client(self.url)

            # Then
            self.assertEqual(response.status_code, expected_status_code)

    def test_not_authenticated_user_cant_search_rides(self):
        # When
        response = self.client.get(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
