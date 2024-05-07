import pytest

from apps.address_manager.models import State
from apps.address_manager.tests.factories import StateFactory
from apps.core.tests.base_test import BaseTest


class StateModelTests(BaseTest):
    def test_create_state_model_instance(self):
        # Given
        expected_attrs = ["name", "code"]

        # When
        state = StateFactory()
        db_state = State.objects.get(pk=state.pk)

        # Then
        self.assertIsInstance(state, State)
        self.assertEqual(str(state), state.name)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(state, attr_name)
                state_attr = getattr(state, attr_name)
                db_state_attr = getattr(db_state, attr_name)
                self.assertEqual(state_attr, db_state_attr)

    def test_state_code_must_be_uppercase(self):
        # Given
        state = StateFactory(code="sp")

        # When
        state.save()

        # Then
        self.assertEqual(state.code, "SP")

    def test_state_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Estado"
        expected_verbose_name_plural = "Estados"

        # When
        meta = State._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)


@pytest.mark.parametrize("attr_name", ["name", "code"])
def test_state_create_raise_exception_without_required_fields(attr_name):
    # Given
    test_data = {attr_name: None}

    # Then
    with StateModelTests().assertRaises(Exception):
        StateFactory.objects.create(**test_data)
