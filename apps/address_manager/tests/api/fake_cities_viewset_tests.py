from rest_framework import status

from apps.address_manager.serializers.state_serializer import (
    NestedStateSerializer,
)
from apps.address_manager.tests.factories import CityFactory, StateFactory
from apps.core.tests.base_test import BaseTest

BASE_TEST_ENDPOINT = "/api/fake-cities/"


class FakeCitiesViewSetTest(BaseTest):
    def test_get_fake_cities_successfully(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_main_keys = ["cities"]
        expected_city_keys = [
            "name",
            "state_code",
        ]
        expected_qtt_data = 10

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(
            list(response_data["cities"][0].keys()), expected_city_keys
        )
        self.assertEqual(len(response_data["cities"]), expected_qtt_data)

    def test_get_fake_cities_with_custom_qtt(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_qtt_data = 5
        query_params = {"qtt_cities": expected_qtt_data}

        # When
        response = self.auth_client.get(url, query_params)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["cities"]), expected_qtt_data)
