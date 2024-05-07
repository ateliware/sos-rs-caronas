import re
from unittest import TestCase

from faker import Faker

from apps.core.utils.regex_utils import get_only_numbers

fake = Faker("pt_BR")


class RegexUtilsTest(TestCase):
    def test_get_only_numbers_returns_only_numbers(self):
        # Given
        fake_cpf = fake.cpf()
        expected_cpf = re.sub("[^0-9]", "", fake_cpf)

        # When
        result = get_only_numbers(fake_cpf)

        # Then
        self.assertEqual(result, expected_cpf)
