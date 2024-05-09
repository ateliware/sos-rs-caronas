from rest_framework import status

from apps.address_manager.serializers.state_serializer import (
    NestedStateSerializer,
)
from apps.address_manager.tests.factories import CityFactory, StateFactory
from apps.core.tests.base_test import BaseTest

BASE_TEST_ENDPOINT = "/api/v1/cities/"


class CityViewSetTest(BaseTest):
    def test_create_city_successfully(self):
        # Given
        url = BASE_TEST_ENDPOINT
        state = StateFactory()
        city_data = CityFactory.city_data()
        expected_main_keys = [
            "id",
            "name",
            "state",
            "created_at",
            "updated_at",
            "is_active",
        ]
        city_data["state_code"] = state.code

        # When
        response = self.auth_client.post(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["name"], city_data["name"])

    def test_create_city_without_name(self):
        # Given
        url = BASE_TEST_ENDPOINT
        state = StateFactory()
        city_data = CityFactory.city_data()
        expected_error_message = "name and state_code are required fields"
        del city_data["name"]
        city_data["state_code"] = state.code

        # When
        response = self.auth_client.post(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_create_city_without_state_code(self):
        # Given
        url = BASE_TEST_ENDPOINT
        city_data = CityFactory.city_data()
        expected_error_message = "name and state_code are required fields"
        del city_data["state_code"]

        # When
        response = self.auth_client.post(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_create_city_with_invalid_state_code(self):
        # Given
        url = BASE_TEST_ENDPOINT
        city_data = CityFactory.city_data()
        expected_error_message = "state not found"
        city_data["state_code"] = "invalid_code"

        # When
        response = self.auth_client.post(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_create_city_return_500_internal_server_error(self):
        # Given
        url = BASE_TEST_ENDPOINT
        state = StateFactory()
        city_data = CityFactory.city_data()
        city_data["name"] = "City Name" * 100
        expected_error_message = "value too long for type character varying"
        city_data["state_code"] = state.code

        # When
        response = self.auth_client.post(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIn(expected_error_message, response_data["error"])

    def test_update_city_sucessfully(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        city_data = CityFactory.city_data()
        expected_main_keys = [
            "id",
            "name",
            "state",
            "created_at",
            "updated_at",
            "is_active",
        ]
        city_data["state_code"] = city.state.code

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["id"], city.id)
        self.assertEqual(response_data["name"], city_data["name"])

    def test_update_city_without_name(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        city_data = CityFactory.city_data()
        expected_error_message = "name and state_code are required fields"
        del city_data["name"]
        city_data["state_code"] = city.state.code

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_update_city_without_state_code(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        city_data = CityFactory.city_data()
        expected_error_message = "name and state_code are required fields"
        del city_data["state_code"]

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_update_city_with_invalid_state_code(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        city_data = CityFactory.city_data()
        expected_error_message = "state not found"
        city_data["state_code"] = "invalid_code"

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_update_city_when_city_not_found(self):
        # Given
        url = f"{BASE_TEST_ENDPOINT}999999/"
        city_data = CityFactory.city_data()
        expected_error_message = "city not found"
        city_data["state_code"] = "invalid_code"

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_update_city_return_500_internal_server_error(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        city_data = CityFactory.city_data()
        city_data["name"] = "City Name" * 100
        expected_error_message = "value too long for type character varying"
        city_data["state_code"] = city.state.code

        # When
        response = self.auth_client.put(
            url,
            city_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        self.assertIn(expected_error_message, response_data["error"])

    def test_list_cities(self):
        # Given
        url = BASE_TEST_ENDPOINT
        city_1 = CityFactory()
        city_2 = CityFactory()
        expected_main_keys = ["count", "next", "previous", "results"]
        expected_results_keys = [
            "id",
            "name",
            "state",
            "created_at",
            "updated_at",
            "is_active",
        ]
        cities_names = [city_1.name, city_2.name]
        states = [
            NestedStateSerializer(city_1.state).data,
            NestedStateSerializer(city_2.state).data,
        ]

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["count"], 2)
        self.assertEqual(response_data["next"], None)
        self.assertEqual(response_data["previous"], None)

        for result in response_data["results"]:
            self.assertEqual(list(result.keys()), expected_results_keys)
            self.assertIn(result["name"], cities_names)
            self.assertIn(result["state"], states)

    def test_retrieve_city(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        expected_main_keys = [
            "id",
            "name",
            "state",
            "created_at",
            "updated_at",
            "is_active",
        ]
        expected_state = NestedStateSerializer(city.state).data

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["name"], city.name)
        self.assertEqual(response_data["state"], expected_state)

    def test_partial_update_city(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"
        data = {"name": "new name"}
        expected_error_message = "partial update not allowed"
        # When
        response = self.auth_client.patch(url, data)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["error"], expected_error_message)

    def test_delete_city(self):
        # Given
        city = CityFactory()
        url = f"{BASE_TEST_ENDPOINT}{city.id}/"

        # When
        response = self.auth_client.delete(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
