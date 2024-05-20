from django.test import RequestFactory
from django.urls import reverse

from apps.core.tests.base_test import FAKE_CPF, BaseTest


class CustomLoginViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.client_factory = RequestFactory()
        self.url = reverse("login")

    def test_login(self):
        # Given
        cpf = FAKE_CPF
        password = "testpassword"

        # When
        response = self.view_unauth_client.post(
            self.url,
            data={"cpf": cpf, "password": password},
        )

        # Then
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

    def test_session_has_show_caution_modal_is_set_to_true(self):
        # Given
        cpf = FAKE_CPF
        password = "testpassword"

        # When
        response = self.view_unauth_client.post(
            self.url,
            data={"cpf": cpf, "password": password},
        )
        request_session = self.view_unauth_client.session
        # Then
        self.assertTrue(request_session.get("show_caution_modal"))

    def test_login_invalid_cpf(self):
        # Given
        cpf = "12345678901"
        password = "testpassword"
        expected_message = "Usuário ou senha incorretos!"

        # When
        response = self.view_unauth_client.post(
            self.url,
            data={"cpf": cpf, "password": password},
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_message, response.content.decode())

    def test_login_invalid_password(self):
        # Given
        cpf = FAKE_CPF
        password = "wrongpassword"
        expected_message = "Usuário ou senha incorretos!"

        # When
        response = self.view_unauth_client.post(
            self.url,
            data={"cpf": cpf, "password": password},
        )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_message, response.content.decode())
