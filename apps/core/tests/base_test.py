from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker
from rest_framework.test import APIClient, override_settings


@override_settings(
    DEFAULT_FILE_STORAGE="django.core.files.storage.memory.InMemoryStorage"
)
class BaseTest(TestCase):
    def setUp(self):
        self.user = self.create_test_user()
        self.auth_client = self.create_authenticated_client()
        self.unauth_client = APIClient()
        self.fake = Faker("pt_BR")

    def create_test_user(self, email="test@email.com", password="testpassword"):
        user_model = get_user_model()
        return user_model.objects.create_user(
            email=email,
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
