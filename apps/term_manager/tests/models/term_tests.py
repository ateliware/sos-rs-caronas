from django.core.exceptions import ValidationError

from apps.core.tests.base_test import BaseTest
from apps.term_manager.models import Term
from apps.term_manager.tests.factories.term_factory import TermFactory


class TermTests(BaseTest):
    def test_create_term_model_instance(self):
        # Given
        expected_attrs = [
            "id",
            "version",
            "type",
            "content",
            "created_at",
            "updated_at",
        ]

        # When
        term = TermFactory()
        db_term = Term.objects.get(id=term.id)

        # Then
        self.assertIsInstance(term, Term)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(term, attr_name)
                term_attr = getattr(term, attr_name)
                db_term_attr = getattr(db_term, attr_name)
                self.assertEqual(term_attr, db_term_attr)

    def test_term_model_verbose_names(self):
        # Given
        expected_verbose_name = "Termo"
        expected_verbose_name_plural = "Termos"

        # When
        meta = Term._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_term_create_raise_exception_when_invalid_term_type(self):
        # Given
        term_data = TermFactory.term_data()
        term_data["type"] = "invalid_type"

        # When
        with self.assertRaises(ValidationError):
            Term.objects.create(**term_data)
