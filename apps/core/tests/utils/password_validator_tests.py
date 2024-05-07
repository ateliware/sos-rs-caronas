from unittest import TestCase

from faker import Faker

from apps.core.utils.password_validator import validate_password

fake = Faker("pt_BR")


class PasswordValidorTests(TestCase):
    def test_validate_password(self):
        # Given
        test_cases = [
            (
                f"aA1!{fake.password(length=6)}",
                True,
            ),  # password with all required chars
            ("aA1", False),  # password without special char
            ("aA!", False),  # password without number
            ("a1!", False),  # password without uppercase letter
            ("A1!", False),  # password without lowercase letter
        ]

        for password, expected_result in test_cases:
            with self.subTest(
                password=password,
                expected_result=expected_result,
            ):
                # When
                response_valid = validate_password(
                    password,
                )

                # Then
                self.assertEqual(response_valid, expected_result)
