from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.affected_place_factory import (
    AffectedPlaceFactory,
)


class AffectedPlaceViewsetTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/affected_places/"

    def test_list_affected_places(self):
        # Given
        AffectedPlaceFactory()

        expected_keys = [
            "uuid",
            "description",
            "address",
            "city",
            "main_person",
            "main_contact",
            "informations",
        ]

        # When
        response = self.auth_client.get(self.url)

        # Then
        response_data = response.json()

        response_affected_place = response_data[0]
        self.assertEqual(response.status_code, 200)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_affected_place.keys()))

        self.assertEqual(len(response_data), 1)

    def test_not_allowed_methods(self):
        # Given
        methods = ["post", "put", "patch", "delete"]

        # When
        for method in methods:
            with self.subTest(method=method):
                response = getattr(self.auth_client, method)(self.url)

                # Then
                self.assertEqual(response.status_code, 405)
