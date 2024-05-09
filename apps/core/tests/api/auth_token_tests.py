from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")


class AuthTokenTest(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cpf = get_only_numbers(fake.cpf())
        self.password = fake.password()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            cpf=self.cpf,
            password=self.password,
        )

    def test_auth_token_obtain_pair_url_resolves(self):
        url = reverse("token_obtain_pair")
        self.assertEqual(url, "/api/v1/token/")

    def test_auth_token_refresh_url_resolves(self):
        url = reverse("token_refresh")
        self.assertEqual(url, "/api/v1/token/refresh/")

    def test_auth_token_returns_400_when_missing_required_fields(self):
        # Given
        url = reverse("token_obtain_pair")
        expected_required_fields = ["cpf", "password"]

        # When
        response = self.client.post(url)

        # Then
        response_data = response.json()
        response_keys = list(response_data.keys())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_keys, expected_required_fields)

    def test_auth_token_returns_401_when_invalid_credentials(self):
        # Given
        url = reverse("token_obtain_pair")
        payload = {
            "cpf": self.cpf,
            "password": fake.password(),
        }
        expected_message = "Usuário e/ou senha incorreto(s)"

        # When
        response = self.client.post(url, payload)

        # Then
        response_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_data["detail"], expected_message)

    def test_auth_token_returns_200_when_valid_credentials(self):
        # Given
        url = reverse("token_obtain_pair")
        payload = {
            "cpf": self.cpf,
            "password": self.password,
        }
        expected_keys = ["refresh", "access"]

        # When
        resp = self.client.post(url, payload, format="json")

        # Then
        response_data = resp.json()
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(response_data.keys()), expected_keys)
