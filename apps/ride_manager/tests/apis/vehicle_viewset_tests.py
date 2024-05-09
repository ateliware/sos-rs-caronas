

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.vehicle_factory import VehicleFactory


class VehicleViewsetTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/vehicle"
        self.person = PersonFactory()
        self.vehicle = VehicleFactory(person=self.person)
        self.payload = VehicleFactory.vehicle_data()
    
    def test_list_vehicles(self):
        # Given
        expected_main_keys = [
            "count",
            "next",
            "previous",
            "results",
        ]
        expected_result_keys = [
            "id",
            "person",
            "model",
            "brand",
            "year",
            "plate",
            "created_at",
            "updated_at",
        ]

        # When
        response = self.auth_client.get(self.url)

        # Then
        response_data = response.json()
        response_vehicle = response_data["results"][0]
        response_main_keys = list(response_data.keys())
        self.assertEqual(response.status_code, 200)

        for item in expected_main_keys:
            with self.subTest(item=item):
                self.assertIn(item, response_main_keys)

        for item in expected_result_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_vehicle.keys()))