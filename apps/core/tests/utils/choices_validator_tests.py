from unittest import TestCase

from faker import Faker

from apps.core.utils.choices_validator import validate_choice
from apps.term_manager.enums import TermTypeChoices

fake = Faker("pt_BR")


class ValidateChoicesTest(TestCase):
    def test_validate_choices_returns_true_when_valid_choices(self):
        # Given
        test_cases = TermTypeChoices.values

        # When
        for choice in test_cases:
            with self.subTest(choice=choice):
                result = validate_choice(choice, TermTypeChoices)

                # Then
                self.assertTrue(result)

    def test_validate_choices_return_false_when_invalid_choice(
        self,
    ):
        # Given
        choice = "invalid_document_type"

        # When
        result = validate_choice(choice, TermTypeChoices)

        # Then
        self.assertFalse(result)
