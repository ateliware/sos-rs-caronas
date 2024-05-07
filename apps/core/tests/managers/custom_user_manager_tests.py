from django.test import TestCase
from faker import Faker

from apps.core.models import CustomUser

fake = Faker("pt_BR")


class CustomUserManagerTest(TestCase):
    def test_create_user_creates_user(self):
        # Given
        email = fake.email()
        password = fake.password()

        # When
        user = CustomUser.objects.create_user(email, password)

        # Then
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_creates_superuser(self):
        # Given
        email = fake.email()
        password = fake.password()

        # When
        user = CustomUser.objects.create_superuser(email, password)

        # Then
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
