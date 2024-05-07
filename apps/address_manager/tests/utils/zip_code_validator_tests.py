import re
from unittest import TestCase

import pytest
from faker import Faker

from apps.address_manager.utils.zip_code_format_validator import (
    zip_code_format_validator,
)

fake = Faker("pt_BR")


class ZipCodeValidorTest(TestCase):
    def test_zip_code_format_validator_returns_true_for_valid_zip_code(self):
        # Given
        fake_zip_code = fake.numerify(text="#####-###")

        # When
        result = zip_code_format_validator(fake_zip_code)

        # Then
        self.assertTrue(result)

    def test_zip_code_format_validator_returns_false_for_invalid_zip_code(self):
        # Given
        test_cases = [
            "12345-6789",
            "123456789",
            "1234-5678",
            "123",
            "12300.123",
        ]

        for zip_code in test_cases:
            # When
            with self.subTest(zip_code=zip_code):
                result = zip_code_format_validator(zip_code)

                # Then
                self.assertFalse(result)
