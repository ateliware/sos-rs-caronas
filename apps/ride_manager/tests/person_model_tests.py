from django.core.exceptions import ValidationError

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.models.person import Person
from apps.ride_manager.tests.factories.person_factory import PersonFactory


class PersonModelTests(BaseTest):
    def test_create_person_model_instance(self):
        # Given
        expected_attrs = [
            "uuid",
            "user",
            "name",
            "phone",
            "emergency_phone",
            "emergency_contact",
            "birth_date",
            "avatar",
            "cnh_number",
            "cnh_picture",
            "document_picture",
            "city",
            "zip_code",
            "cnh_is_verified",
            "document_is_verified",
            "profile_is_verified",
            "is_active",
            "created_at",
            "updated_at",
        ]

        # When
        person = PersonFactory()
        db_person = Person.objects.get(uuid=person.uuid)

        # Then
        self.assertIsInstance(person, Person)

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(person, attr_name)
                person_attr = getattr(person, attr_name)
                db_person_attr = getattr(db_person, attr_name)
                self.assertEqual(person_attr, db_person_attr)

    def test_person_model_verbose_names(self):
        # Given
        expected_verbose_name = "Pessoa"
        expected_verbose_name_plural = "Pessoas"

        # When
        meta = Person._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_upload_path(self):
        # Given
        person = PersonFactory()
        filename = "test.jpg"
        expected_upload_path = f"person_files/{person.uuid}/{filename}"

        # When
        upload_path = person.avatar.field.upload_to(person, filename)

        # Then
        self.assertEqual(upload_path, expected_upload_path)

    def test_person_create_raise_exception_when_missing_required_fields(self):
        # Given
        test_cases = [
            "user",
            "name",
            "phone",
            "birth_date",
            "city",
            "zip_code",
        ]
        city = CityFactory()

        for attr in test_cases:
            # When
            with self.subTest(attr=attr):
                person_data = PersonFactory.person_data()
                person_data["user"] = self.user
                person_data["city"] = city
                person_data[attr] = None

                # Then
                with self.assertRaises(Exception):
                    Person.objects.create(**person_data)

    def test_person_create_raise_exception_when_invalid_zip_code_format(self):
        # Given
        person_data = PersonFactory.person_data()
        person_data["user"] = self.user
        person_data["city"] = CityFactory()
        person_data["zip_code"] = "123456"

        # When/Then
        with self.assertRaises(ValidationError):
            Person.objects.create(**person_data)
