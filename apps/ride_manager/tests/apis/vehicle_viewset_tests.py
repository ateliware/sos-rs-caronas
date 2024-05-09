from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.vehicle_factory import VehicleFactory


class VehicleViewsetTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/vehicles/"
        self.person = PersonFactory(user=self.user)
        self.vehicle = VehicleFactory(person=self.person)
        self.payload = VehicleFactory.vehicle_data()

    def test_list_vehicles(self):
        # Given
        expected_keys = [
            "uuid",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
            "created_at",
        ]

        # When
        response = self.auth_client.get(self.url)

        # Then
        response_data = response.json()
        response_vehicle = response_data[0]
        self.assertEqual(response.status_code, 200)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_vehicle.keys()))

        self.assertEqual(len(response_data), 1)

    def test_create_vehicle(self):
        # Given
        expected_keys = [
            "uuid",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
            "created_at",
        ]

        # When
        response = self.auth_client.post(
            self.url,
            self.payload,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))

    def test_put_vehicle(self):
        # Given
        url = f"{self.url}{self.vehicle.uuid}/"
        payload = VehicleFactory.vehicle_data()

        # When
        response = self.auth_client.put(url, payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_vehicle(self):
        # Given
        url = f"{self.url}{self.vehicle.uuid}/"

        # When
        response = self.auth_client.delete(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tests_not_authenticated_user_cant_list_vehicles(self):
        # When
        response = self.client.get(self.url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_not_authenticated_user_cant_create_vehicle(self):
        # When
        response = self.client.post(self.url, self.payload)

        # Then
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
