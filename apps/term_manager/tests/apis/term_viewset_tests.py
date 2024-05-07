from decouple import config
from rest_framework import status

from apps.core.tests.base_test import BaseTest
from apps.term_manager.models.term import Term
from apps.term_manager.tests.factories.term_factory import TermFactory

BASE_TEST_ENDPOINT = "/api/terms/"
PAGE_SIZE = int(config("REST_PAGE_SIZE", default=20))


class TermViewSetTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.term = TermFactory()

    def test_retrieve_term_successfully(self):
        # Given
        url = f"{BASE_TEST_ENDPOINT}?type={self.term.type}"
        expected_main_keys = [
            "id",
            "version",
            "type",
            "content",
            "created_at",
        ]

        # When
        response = self.unauth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in expected_main_keys:
            with self.subTest(item=item):
                self.assertIn(item, list(response_data.keys()))

    def test_retreive_term_returns_400_when_type_is_not_sent(self):
        # Given
        url = BASE_TEST_ENDPOINT
        expected_response = "Tipo do termo é obrigatório"

        # When
        response = self.unauth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], expected_response)

    def test_retrieve_term_returns_400_when_type_is_invalid(self):
        # Given
        url = f"{BASE_TEST_ENDPOINT}?type=INVALID"
        expected_response = "Tipo do termo inválido"

        # When
        response = self.unauth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], expected_response)

    def test_retrieve_term_returns_404_when_term_not_found(self):
        # Given
        url = f"{BASE_TEST_ENDPOINT}?type={self.term.type}"
        Term.objects.all().delete()
        expected_response = "Termo não encontrado"

        # When
        response = self.unauth_client.get(url)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data["message"], expected_response)
