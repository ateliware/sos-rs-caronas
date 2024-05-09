from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.custom_user_factory import CustomUserFactory
from apps.term_manager.tests.factories.term_acceptance_factory import (
    TermAcceptanceFactory,
)
from apps.term_manager.tests.factories.term_factory import TermFactory

BASE_TEST_ENDPOINT = "/api/v1/acceptance-terms/"


class TermAcceptanceViewSetTests(BaseTest):
    def setUp(self):
        super().setUp()

    def test_list_acceptance_terms(self):
        # Given
        acceptance_term = TermAcceptanceFactory(user=self.user)
        url = BASE_TEST_ENDPOINT
        expected_main_keys = [
            "count",
            "next",
            "previous",
            "results",
        ]
        expected_result_keys = [
            "id",
            "term",
            "hashed_term",
            "created_at",
        ]

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        response_acceptance_term = response_data["results"][0]
        response_main_keys = list(response_data.keys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in expected_main_keys:
            with self.subTest(item=item):
                self.assertIn(item, response_main_keys)

        for item in expected_result_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_acceptance_term.keys()))

    def test_list_acceptance_terms_when_epu_isnt_owner_of_any_acceptance_term(
        self,
    ):
        # Given
        url = BASE_TEST_ENDPOINT
        acceptance_term = TermAcceptanceFactory()

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["count"], 0)

    def test_create_acceptance_term(self):
        # Given
        url = BASE_TEST_ENDPOINT
        term = TermFactory()
        payload = {"term": term.id}
        expected_keys = [
            "id",
            "term",
            "hashed_term",
            "created_at",
        ]

        # When
        response = self.auth_client.post(url, payload, format="json")

        # Then
        response_data = response.json()
        response_keys = list(response_data.keys())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["term"], term.id)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, response_keys)

    def test_retrieve_acceptance_term(self):
        # Given
        acceptance_term = TermAcceptanceFactory(user=self.user)
        url = f"{BASE_TEST_ENDPOINT}{acceptance_term.id}/"
        expected_keys = [
            "id",
            "term",
            "hashed_term",
            "created_at",
        ]

        # When
        response = self.auth_client.get(url)

        # Then
        response_data = response.json()
        response_keys = list(response_data.keys())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in expected_keys:
            with self.subTest(item=item):
                self.assertIn(item, response_keys)

    def test_retrieve_acceptance_term_when_epu_isnt_owner_of_acceptance_term(
        self,
    ):
        # Given
        acceptance_term = TermAcceptanceFactory()
        url = f"{BASE_TEST_ENDPOINT}{acceptance_term.id}/"

        # When
        response = self.auth_client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_acceptance_term_when_acceptance_term_doesnt_exist(self):
        # Given
        url = f"{BASE_TEST_ENDPOINT}9999999/"

        # When
        response = self.auth_client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_allowed_methods(self):
        # Given
        url = BASE_TEST_ENDPOINT
        payload = {}
        test_cases = [
            self.auth_client.patch,
            self.auth_client.put,
            self.auth_client.delete,
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                # When
                response = test_case(url, payload, format="json")

                # Then
                self.assertEqual(
                    response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
                )

    def test_when_client_is_unauthenticated(self):
        # Given
        url = BASE_TEST_ENDPOINT
        payload = {}
        test_cases = [
            self.client.get,
            self.client.post,
        ]
        expected_message = {
            "detail": "As credenciais de autenticação não foram fornecidas."
        }
        expected_status_code = status.HTTP_401_UNAUTHORIZED

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                # When
                response = test_case(url, payload, format="json")

                # Then
                self.assertEqual(response.status_code, expected_status_code)
                self.assertEqual(response.json(), expected_message)
