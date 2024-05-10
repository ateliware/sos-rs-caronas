from copy import deepcopy
from uuid import uuid4

from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.services.person_register_service import (
    PersonRegisterService,
)
from apps.ride_manager.tests.factories.person_register_payload_factory import (
    person_register_payload_factory,
)
from apps.ride_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)
from apps.term_manager.enums import TermTypeChoices
from apps.term_manager.tests.factories.term_factory import TermFactory

fake = Faker("pt_BR")


class PersonRegisterServiceTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.payload = person_register_payload_factory()
        self.city = CityFactory()
        self.phone_validation = PhoneValidationFactory(
            is_active=True,
            phone=self.payload["phone"],
        )
        self.payload["validation_uuid"] = str(self.phone_validation.uuid)
        self.payload["city_id"] = self.city.id

    def test_check_phone_validation_successfully(self):
        # Given
        service = PersonRegisterService(self.payload)

        # When
        response = service.check_phone_validation()

        # Then
        self.assertTrue(response)

    def test_check_phone_validation_with_not_validated_phone(self):
        # Given
        self.phone_validation.is_active = False
        self.phone_validation.save()
        service = PersonRegisterService(self.payload)
        expected_error = "Código de validação inválido"

        # When
        response = service.check_phone_validation()

        # Then
        self.assertFalse(response)

    def test_check_phone_validation_with_invalid_uuid(self):
        # Given
        payload = deepcopy(self.payload)
        payload["validation_uuid"] = str(uuid4())
        service = PersonRegisterService(payload)
        expected_error = "Código de validação inválido"

        # When
        with self.assertRaises(Exception) as context:
            service.check_phone_validation()

        # Then
        self.assertIn(expected_error, str(context.exception))

    def test_create_custom_user_successfully(self):
        # Given
        service = PersonRegisterService(self.payload)
        spllitted_name = self.payload["name"].split(" ")

        # When
        user = service.create_custom_user()

        # Then
        self.assertEqual(user.cpf, self.payload["cpf"])
        self.assertEqual(user.first_name, spllitted_name[0].capitalize())
        self.assertEqual(user.last_name, spllitted_name[-1].capitalize())
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_custom_user_with_invalid_data(self):
        # Given
        payload = deepcopy(self.payload)
        payload["cpf"] = "12345678901"
        service = PersonRegisterService(payload)
        expected_error = "Erro ao criar usuário"

        # When
        with self.assertRaises(Exception) as context:
            service.create_custom_user()

        # Then
        self.assertIn(expected_error, str(context.exception))

    def test_create_person_successfully(self):
        # Given
        service = PersonRegisterService(self.payload)
        user = service.create_custom_user()

        # When
        person = service.create_person(user)

        # Then
        self.assertEqual(person.user, user)
        self.assertEqual(person.name, self.payload["name"])
        self.assertEqual(person.phone, self.payload["phone"])
        self.assertEqual(
            person.birth_date.strftime("%Y-%m-%d"), self.payload["birth_date"]
        )
        self.assertEqual(
            person.emergency_phone, self.payload["emergency_phone"]
        )

    def test_create_person_with_invalid_data(self):
        # Given
        payload = deepcopy(self.payload)
        payload["birth_date"] = "invalid_date"
        service = PersonRegisterService(payload)
        expected_error = "Erro ao criar Pessoa"

        # When
        with self.assertRaises(Exception) as context:
            service.create_person(None)

        # Then
        self.assertIn(expected_error, str(context.exception))

    def test_create_acceptance_terms_successfully(self):
        # Given
        use_term = TermFactory(type=TermTypeChoices.USE)
        privacy_term = TermFactory(type=TermTypeChoices.PRIVACY)
        service = PersonRegisterService(self.payload)
        user = service.create_custom_user()
        person = service.create_person(user)

        # When
        response = service.create_acceptance_terms(person)

        # Then
        self.assertEqual(len(response), 2)
        for acceptance_term in response:
            with self.subTest(acceptance_term=acceptance_term):
                self.assertEqual(acceptance_term.user, person.user)
                self.assertIn(acceptance_term.term, [use_term, privacy_term])

    def test_create_acceptance_terms_when_terms_not_found(self):
        # Given
        service = PersonRegisterService(self.payload)
        user = service.create_custom_user()
        person = service.create_person(user)
        expected_error = "Termo não encontrado"

        # When
        with self.assertRaises(Exception) as context:
            service.create_acceptance_terms(person)

        # Then
        self.assertIn(expected_error, str(context.exception))

    def test_create_acceptance_terms_without_epu(self):
        # Given
        service = PersonRegisterService(self.payload)
        expected_error = "Erro ao criar termos de aceite"

        # When
        with self.assertRaises(Exception) as context:
            service.create_acceptance_terms(None)

        # Then
        self.assertIn(expected_error, str(context.exception))

    def test_register_person_successfully(self):
        # Given
        use_term = TermFactory(type=TermTypeChoices.USE)
        privacy_term = TermFactory(type=TermTypeChoices.PRIVACY)
        service = PersonRegisterService(self.payload)
        expected_keys = [
            "uuid",
            "name",
            "phone",
            "emergency_phone",
            "emergency_contact",
            "birth_date",
            "avatar",
        ]

        # When
        response = service.register_person()

        # Then
        response_keys = list(response.keys())
        for key in expected_keys:
            with self.subTest(key=key):
                self.assertIn(key, response_keys)

    def test_register_epu_with_invalid_data(self):
        # Given
        payload = deepcopy(self.payload)
        payload["city_id"] = 0
        service = PersonRegisterService(payload)
        expected_error = "Erro ao criar Pessoa"

        # When
        with self.assertRaises(Exception) as context:
            service.register_person()

        # Then
        self.assertIn(expected_error, str(context.exception))
