from django.test import TestCase
from faker import Faker

from apps.core.models import CustomUser
from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")


class CustomUserManagerTest(TestCase):
    def test_create_user_creates_user(self):
        # Given
        cpf = get_only_numbers(fake.cpf())
        password = fake.password()

        # When
        user = CustomUser.objects.create_user(cpf, password)

        # Then
        self.assertEqual(user.cpf, cpf)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_creates_superuser(self):
        # Given
        cpf = get_only_numbers(fake.cpf())
        password = fake.password()

        # When
        user = CustomUser.objects.create_superuser(cpf, password)

        # Then
        self.assertEqual(user.cpf, cpf)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
