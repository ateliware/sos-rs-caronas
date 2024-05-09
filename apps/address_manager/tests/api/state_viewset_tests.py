from rest_framework import status

from apps.address_manager.tests.factories import StateFactory
from apps.core.tests.base_test import BaseTest

BASE_TEST_ENDPOINT = "/api/v1/states/"


class StateViewSetTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.state = StateFactory()

    def test_list_states(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_main_keys = ["count", "next", "previous", "results"]
        expected_results_keys = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["count"], 1)
        self.assertEqual(response_data["next"], None)
        self.assertEqual(response_data["previous"], None)

        for result in response_data["results"]:
            self.assertEqual(list(result.keys()), expected_results_keys)
            self.assertEqual(result["name"], self.state.name)
            self.assertEqual(result["code"], self.state.code)

    def test_create_state(self):
        # Given
        url = BASE_TEST_ENDPOINT
        state_data = StateFactory.state_data()
        expected_main_keys = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        response = self.auth_client.post(
            url,
            state_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["name"], state_data["name"])
        self.assertEqual(response_data["code"], state_data["code"])

    def test_filter_states(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_id = self.state.id

        # When
        response = self.auth_client.get(url, {"name": self.state.name})

        # Then
        response_data = response.json()
        response_state = response_data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), 1)
        self.assertEqual(response_state["id"], expected_id)

    def test_filter_states_when_passed_partial_name(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_results_qtt = 1
        other_state = StateFactory(name=self.fake.password())

        # When
        response = self.auth_client.get(url, {"name": other_state.name[:5]})

        # Then
        response_data = response.json()
        response_state = response_data["results"][0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data["results"]), expected_results_qtt)
        self.assertEqual(response_state["id"], other_state.id)

    def test_retrieve_state(self):
        # Given
        state = StateFactory()
        url = f"{BASE_TEST_ENDPOINT}{state.id}/"
        expected_main_keys = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["id"], state.id)

    def test_update_state(self):
        # Given
        state = StateFactory()
        url = f"{BASE_TEST_ENDPOINT}{state.id}/"
        state_update_data = StateFactory.state_data()
        expected_main_keys = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        response = self.auth_client.put(
            url,
            state_update_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["id"], state.id)
        self.assertEqual(response_data["name"], state_update_data["name"])
        self.assertEqual(response_data["code"], state_update_data["code"])

    def test_partial_update_state(self):
        # Given
        state = StateFactory()
        url = f"{BASE_TEST_ENDPOINT}{state.id}/"
        state_update_data = {"name": "New State Name"}
        expected_main_keys = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        response = self.auth_client.patch(
            url,
            state_update_data,
        )

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_data.keys()), expected_main_keys)
        self.assertEqual(response_data["id"], state.id)
        self.assertEqual(response_data["name"], state_update_data["name"])

    def test_delete_state(self):
        # Given
        state = StateFactory()
        url = f"{BASE_TEST_ENDPOINT}{state.id}/"

        # When
        response = self.auth_client.delete(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
