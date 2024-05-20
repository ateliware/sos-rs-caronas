from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from faker import Faker
from rest_framework.test import APIClient, override_settings

from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")

FAKE_CPF = get_only_numbers(fake.cpf())


@override_settings(
    DEFAULT_FILE_STORAGE="django.core.files.storage.memory.InMemoryStorage"
)
class BaseTest(TestCase):
    def setUp(self):
        self.user = self.create_test_user()
        self.auth_client = self.create_authenticated_client()
        self.unauth_client = APIClient()
        self.view_client = Client(user=self.user)
        self.view_client.login(username=FAKE_CPF, password="testpassword")
        self.view_unauth_client = Client()
        self.fake = fake

    def create_test_user(self, cpf=FAKE_CPF, password="testpassword"):
        user_model = get_user_model()
        return user_model.objects.create_user(
            cpf=cpf,
            password=password,
        )

    def create_authenticated_client(self, user=None):
        client = APIClient()
        user = user or self.user
        client.force_authenticate(user=user)
        return client

    def assertHasAttr(self, obj, attr):
        self.assertTrue(
            hasattr(obj, attr),
            f"{obj.__class__.__name__} does not have attribute {attr}",
        )

    def execute_admin_tests(self, expected_list: list, test_attr: str):
        # When
        result = getattr(self.admin, test_attr)

        # Then
        for item in expected_list:
            with self.subTest(item=item):
                self.assertIn(item, result)
