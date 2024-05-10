from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.ride_factory import RideFactory

class RideViewsetTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/rides/"
        self.person = PersonFactory(user=self.user)
        self.ride = RideFactory(driver=self.person)
        self.payload = RideFactory.ride_data()
    
    def test_list_rides(self):
        # Given
        expected_result_keys = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "whatspp_group_link",
            "notes",
            "status",
        ]

        # When
        response = self.auth_client.get(self.url)

        # Then
        response_data = response.json()
        response_ride = response_data["results"][0]
        self.assertEqual(response.status_code, 200)

        for item in expected_result_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_ride.keys()))

        self.assertEqual(response_data["count"], 1)
    
    def test_create_ride(self):
        # Given
        expected_keys = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "driver",
            "vehicle",
            "whatspp_group_link",
            "notes",
            "status",
        ]

        # When
        response = self.auth_client.post(self.url, self.payload)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, 201)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))
