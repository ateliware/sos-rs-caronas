import re
from unittest import TestCase

import pytest
from faker import Faker

from apps.core.utils.cpf_validator import CpfValidator

fake = Faker("pt_BR")


class CpfValidorTest(TestCase):
    def test_check_equal_digits_returns_true_for_equal_digits(self):
        # Given
        fake_cpf = "11111111111"

        # When
        validator = CpfValidator()
        result = validator.check_equal_digits(fake_cpf)

        # Then
        self.assertTrue(result)

    def test_check_equal_digits_returns_false_for_different_digits(self):
        # Given
        fake_cpf = fake.cpf()

        # When
        validator = CpfValidator()
        result = validator.check_equal_digits(fake_cpf)

        # Then
        self.assertFalse(result)

    def test_calculate_cpf_verifier_digit_returns_correct_digit_for_first_digit(
        self,
    ):
        # Given
        fake_cpf = re.sub("[^0-9]", "", fake.cpf())
        expected_digit = fake_cpf[-2]

        # When
        validator = CpfValidator()
        result = validator.calculate_cpf_verifier_digit(fake_cpf, 1)

        # Then
        self.assertEqual(result, expected_digit)

    def test_calculate_cpf_verifier_digit_returns_correct_digit_for_second_digit(
        self,
    ):
        # Given
        fake_cpf = re.sub("[^0-9]", "", fake.cpf())
        expected_digit = fake_cpf[-1]

        # When
        validator = CpfValidator()
        result = validator.calculate_cpf_verifier_digit(fake_cpf, 2)

        # Then
        self.assertEqual(result, expected_digit)


# Given
@pytest.mark.parametrize(
    "cpf,expected_result",
    [
        (fake.cpf(), True),  # valid cpf
        ("000.000.000-00", False),  # cpf with all digits equal
        ("111.111.111-11", False),  # cpf with all digits equal
        ("900.880.940-99", False),  # invalid cpf verification digits
        ("74.168.245/0001-69", False),  # cnpj - invalid length
    ],
)
def test_validate_cpf(cpf, expected_result):
    # When
    cpf_only_numbers = re.sub("[^0-9]", "", cpf)
    validator = CpfValidator()
    resp = validator.validate_cpf(cpf_only_numbers)

    # Then
    CpfValidorTest().assertEqual(resp, expected_result)
