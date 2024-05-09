from copy import deepcopy
from uuid import uuid4

from faker import Faker

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.ride_manager.services.person_register_service import PersonRegisterService
from apps.client_manager.tests.factories.epu_register_payload_factory import (
    epu_register_payload_factory,
)
from apps.client_manager.tests.factories.occupation_category_factory import (
    OccupationCategoryFactory,
)
from apps.client_manager.tests.factories.occupation_factory import (
    OccupationFactory,
)
from apps.client_manager.tests.factories.phone_validation_factory import (
    PhoneValidationFactory,
)
from apps.core.tests.base_test import BaseTest
from apps.term_manager.enums import TermTypeChoices
from apps.term_manager.tests.factories.term_factory import TermFactory

fake = Faker("pt_BR")


class EpuRegisterServiceTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.payload = epu_register_payload_factory()
        self.city = CityFactory()
        self.occupation = OccupationFactory()
        self.occupation_category = OccupationCategoryFactory(
            occupation=self.occupation
        )
        self.phone_validation = PhoneValidationFactory(
            is_active=True,
            phone=self.payload["phone"],
        )
        self.payload["validation_uuid"] = str(self.phone_validation.uuid)
        self.payload["city_id"] = self.city.id
        self.payload["occupation_id"] = self.occupation.id
        self.payload["categories_ids"] = [self.occupation_category.id]

    # def test_check_phone_validation_successfully(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)

    #     # When
    #     response = service.check_phone_validation()

    #     # Then
    #     self.assertTrue(response)

    # def test_check_phone_validation_with_not_validated_phone(self):
    #     # Given
    #     self.phone_validation.is_active = False
    #     self.phone_validation.save()
    #     service = EpuRegisterService(self.payload)
    #     expected_error = "Código de validação inválido"

    #     # When
    #     response = service.check_phone_validation()

    #     # Then
    #     self.assertFalse(response)

    # def test_check_phone_validation_with_invalid_uuid(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["validation_uuid"] = str(uuid4())
    #     service = EpuRegisterService(payload)
    #     expected_error = "Código de validação inválido"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.check_phone_validation()

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_custom_user_successfully(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     spllitted_name = self.payload["name"].split(" ")

    #     # When
    #     user = service.create_custom_user()

    #     # Then
    #     self.assertEqual(user.cpf, self.payload["cpf"])
    #     self.assertEqual(user.first_name, spllitted_name[0].capitalize())
    #     self.assertEqual(user.last_name, spllitted_name[-1].capitalize())
    #     self.assertEqual(user.email, self.payload["email"])
    #     self.assertTrue(user.check_password(self.payload["password"]))
    #     self.assertTrue(user.is_active)
    #     self.assertFalse(user.is_staff)
    #     self.assertFalse(user.is_superuser)

    # def test_create_custom_user_with_invalid_data(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["cpf"] = "12345678901"
    #     service = EpuRegisterService(payload)
    #     expected_error = "Erro ao criar usuário"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_custom_user()

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_epu_successfully(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     user = service.create_custom_user()

    #     # When
    #     epu = service.create_epu(user)

    #     # Then
    #     self.assertEqual(epu.user, user)
    #     self.assertEqual(epu.name, self.payload["name"])
    #     self.assertEqual(epu.email, self.payload["email"])
    #     self.assertEqual(epu.phone, self.payload["phone"])
    #     self.assertEqual(epu.birth_date, self.payload["birth_date"])
    #     self.assertEqual(epu.income, self.payload["income"])

    # def test_create_epu_with_invalid_data(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["birth_date"] = "invalid_date"
    #     service = EpuRegisterService(payload)
    #     expected_error = "Erro ao criar EPU"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_epu(None)

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_address_successfully(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     user = service.create_custom_user()
    #     epu = service.create_epu(user)
    #     expected_description = "Principal"

    #     # When
    #     address = service.create_address(epu)

    #     # Then
    #     self.assertEqual(address.epu, epu)
    #     self.assertEqual(address.street, self.payload["street"])
    #     self.assertEqual(address.number, self.payload["number"])
    #     self.assertEqual(address.complement, self.payload["complement"])
    #     self.assertEqual(address.neighborhood, self.payload["neighborhood"])
    #     self.assertEqual(address.city.id, self.payload["city_id"])
    #     self.assertEqual(address.zip_code, self.payload["zip_code"])
    #     self.assertEqual(address.description, expected_description)
    #     self.assertTrue(address.is_main)

    # def test_create_address_with_invalid_data(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["city_id"] = 0
    #     service = EpuRegisterService(payload)
    #     expected_error = "Erro ao criar endereço"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_address(None)

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_epu_documents_successfully(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     user = service.create_custom_user()
    #     epu = service.create_epu(user)

    #     # When
    #     epu_documents = service.create_epu_documents(epu)
    #     epu_document = epu_documents[0]

    #     # Then
    #     self.assertEqual(len(epu_documents), 1)
    #     self.assertEqual(
    #         epu_document.document_type,
    #         self.payload["documents"][0]["document_type"],
    #     )
    #     self.assertEqual(epu_document.is_required, True)
    #     self.assertEqual(epu_document.is_approved, False)
    #     self.assertEqual(epu_document.epu, epu)
    #     self.assertIsNotNone(epu_document.document)

    # def test_create_epu_documents_with_invalid_data(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["documents"][0]["document_type"] = "invalid_document_type"
    #     service = EpuRegisterService(payload)
    #     user = service.create_custom_user()
    #     epu = service.create_epu(user)
    #     expected_error = "Erro ao criar documento de EPU"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_epu_documents(epu)

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_acceptance_terms_successfully(self):
    #     # Given
    #     use_term = TermFactory(type=TermTypeChoices.USE)
    #     privacy_term = TermFactory(type=TermTypeChoices.PRIVACY)
    #     service = EpuRegisterService(self.payload)
    #     user = service.create_custom_user()
    #     epu = service.create_epu(user)

    #     # When
    #     response = service.create_acceptance_terms(epu)

    #     # Then
    #     self.assertEqual(len(response), 2)
    #     for acceptance_term in response:
    #         with self.subTest(acceptance_term=acceptance_term):
    #             self.assertEqual(acceptance_term.epu, epu)
    #             self.assertIn(acceptance_term.term, [use_term, privacy_term])

    # def test_create_acceptance_terms_when_terms_not_found(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     user = service.create_custom_user()
    #     epu = service.create_epu(user)
    #     expected_error = "Termo não encontrado"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_acceptance_terms(epu)

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_create_acceptance_terms_without_epu(self):
    #     # Given
    #     service = EpuRegisterService(self.payload)
    #     expected_error = "Erro ao criar termos de aceite"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.create_acceptance_terms(None)

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))

    # def test_register_epu_successfully(self):
    #     # Given
    #     use_term = TermFactory(type=TermTypeChoices.USE)
    #     privacy_term = TermFactory(type=TermTypeChoices.PRIVACY)
    #     service = EpuRegisterService(self.payload)
    #     expected_keys = [
    #         "epu_uuid",
    #         "address_id",
    #         "epu_documents_id",
    #         "acceptance_terms_id",
    #     ]

    #     # When
    #     response = service.register_epu()

    #     # Then
    #     response_keys = list(response.keys())
    #     for key in expected_keys:
    #         with self.subTest(key=key):
    #             self.assertIn(key, response_keys)

    # def test_register_epu_with_invalid_data(self):
    #     # Given
    #     payload = deepcopy(self.payload)
    #     payload["city_id"] = 0
    #     service = EpuRegisterService(payload)
    #     expected_error = "Erro ao criar endereço"

    #     # When
    #     with self.assertRaises(Exception) as context:
    #         service.register_epu()

    #     # Then
    #     self.assertIn(expected_error, str(context.exception))
