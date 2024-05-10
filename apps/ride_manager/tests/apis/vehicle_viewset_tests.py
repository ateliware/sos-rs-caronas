from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.valid_base64_image_factory import (
    valid_base64_image,
)
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
            "person",
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

    def test_create_vehicle_when_cnh_isnt_verified(self):
        # Given
        expected_keys = [
            "uuid",
            "person",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
            "created_at",
        ]

        # When
        payload = {
            **self.payload,
            "cnh_number": "123456789",
            "cnh_picture": valid_base64_image(),
        }
        response = self.auth_client.post(
            self.url,
            payload,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))

    def test_create_vehicle_when_cnh_is_verified(self):
        # Given
        self.person.cnh_is_verified = True
        self.person.save()
        expected_keys = [
            "uuid",
            "person",
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

    def test_create_vehicle_without_cnh_info_and_cnh_isnt_verified(self):
        # Given
        expected_error = "Número e foto da CNH são obrigatórios"

        # When
        response = self.auth_client.post(
            self.url,
            self.payload,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], expected_error)

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

    def test_not_allowed_methods(self):
        # Given
        test_cases = [
            (
                f"{self.url}{self.vehicle.pk}/",
                self.auth_client.put,
            ),
            (
                f"{self.url}{self.vehicle.pk}/",
                self.auth_client.patch,
            ),
            (
                f"{self.url}{self.vehicle.pk}/",
                self.auth_client.delete,
            ),
        ]
        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED

        # When
        for url, api_client in test_cases:
            response = api_client(url)

            # Then
            self.assertEqual(response.status_code, expected_status_code)
