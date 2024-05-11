from apps.core.tests.base_test import BaseTest
from apps.ride_manager.tests.factories.person_factory import PersonFactory
from apps.ride_manager.tests.factories.voluntary_factory import VoluntaryFactory


class VoluntaryViewsetTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = "/api/v1/voluntaries/"
        self.person = PersonFactory(user=self.user)
        self.voluntary = VoluntaryFactory(person=self.person)
        self.payload = VoluntaryFactory.voluntary_data()

    def test_create_voluntary(self):
        # Given
        expected_keys = [
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
        ]
        # When
        response = self.auth_client.post(self.url, self.payload)

        # Then
        response_data = response.json()

        self.assertEqual(response.status_code, 201)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))

    def test_not_allowed_methods(self):
        # Given
        methods = ["put", "patch", "delete"]

        # When
        for method in methods:
            with self.subTest(method=method):
                response = getattr(self.auth_client, method)(self.url)

                # Then
                self.assertEqual(response.status_code, 405)
