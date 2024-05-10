from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.passenger_factory import PassengerFactory
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory


class RideViewsetTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/rides/"
        self.person = PersonFactory(user=self.user)

        self.ride = RideFactory(driver=self.person)
        self.payload = RideFactory.ride_data()
        del self.payload["driver"]

    def test_list_rides(self):
        # Given
        expected_result_keys = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "quantity_of_passengers",
            "whatsapp_group_link",
            "notes",
            "status",
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

        self.assertEqual(len(response_data), 1)

    def test_create_ride(self):
        # Given
        expected_keys = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "quantity_of_passengers",
            "notes",
            "status",
        ]

        # When
        response = self.auth_client.post(self.url, self.payload)

        # Then
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))

    def test_method_post_for_unauthorized(self):
        # When
        response = self.client.post(self.url, self.payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_method_get_for_not_allowed(self):
        # When
        response = self.client.get(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_method_put_not_allowed(self):
        # When
        response = self.auth_client.put(self.url)

        # Then
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_method_delete_not_allowed(self):
        # When
        response = self.auth_client.delete(self.url)

        # Then
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_get_for_diferet_driver_not_results(self):
        # Given
        self.ride.driver = PersonFactory()
        self.ride.save()

        # When
        response = self.auth_client.get(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_get_passengers(self):
        # Given
        passenger = PassengerFactory(ride=self.ride)
        url = f"{self.url}{self.ride.uuid}/passengers/"

        # When
        response = self.auth_client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["uuid"], str(passenger.uuid))
