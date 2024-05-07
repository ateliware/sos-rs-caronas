from hashlib import sha256

from apps.core.tests.base_test import BaseTest
from apps.core.tests.factories.custom_user_factory import CustomUserFactory
from apps.term_manager.models import TermAcceptance
from apps.term_manager.tests.factories.term_acceptance_factory import (
    TermAcceptanceFactory,
)
from apps.term_manager.tests.factories.term_factory import TermFactory


class TermAcceptanceTests(BaseTest):
    def test_create_term_acceptance_model_instance(self):
        # Given
        expected_attrs = [
            "id",
            "term",
            "user",
            "hashed_term",
            "created_at",
            "updated_at",
        ]

        # When
        term_acceptance = TermAcceptanceFactory()
        db_term_acceptance = TermAcceptance.objects.get(id=term_acceptance.id)

        # Then
        self.assertIsInstance(term_acceptance, TermAcceptance)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(term_acceptance, attr_name)
                term_acceptance_attr = getattr(term_acceptance, attr_name)
                db_term_acceptance_attr = getattr(db_term_acceptance, attr_name)
                self.assertEqual(term_acceptance_attr, db_term_acceptance_attr)

    def test_term_acceptance_model_verbose_names(self):
        # Given
        expected_verbose_name = "Aceite de Termo"
        expected_verbose_name_plural = "Aceites de Termo"

        # When
        meta = TermAcceptance._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_if_hashed_term_is_generated_on_save(self):
        # Given
        term_acceptance = TermAcceptanceFactory()

        # When
        term_acceptance.save()

        # Then
        self.assertIsNotNone(term_acceptance.hashed_term)

    def test_if_hashed_term_is_generated_correctly(self):
        # Given
        term = TermFactory()
        user = CustomUserFactory()
        expected_content = f"{term.content}|{user.email}"
        expected_hashed_content = sha256(expected_content.encode()).hexdigest()

        # When
        term_acceptance = TermAcceptance(term=term, user=user)
        term_acceptance.save()

        # Then
        db_term_acceptance = TermAcceptance.objects.get(id=term_acceptance.id)
        self.assertEqual(
            db_term_acceptance.hashed_term,
            expected_hashed_content,
        )
