from decimal import Decimal

from apps.address_manager.models import Address
from apps.address_manager.tests.factories.address_factory import AddressFactory
from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest


class AddressModelTests(BaseTest):
    def test_create_address_model_instance(self):
        # Given
        expected_attrs = [
            "id",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "zip_code",
            "description",
            "user",
            "created_at",
            "updated_at",
            "is_active",
        ]

        # When
        address = AddressFactory()
        db_address = Address.objects.get(id=address.id)

        # Then
        self.assertIsInstance(address, Address)
        self.assertEqual(str(db_address), str(address.id))

        for attr_name in expected_attrs:
            with self.subTest(attr=attr_name):
                self.assertHasAttr(address, attr_name)
                address_attr = getattr(address, attr_name)
                db_address_attr = getattr(db_address, attr_name)
                self.assertEqual(address_attr, db_address_attr)

    def test_address_model_meta_verbose_names(self):
        # Given
        expected_verbose_name = "Endereço"
        expected_verbose_name_plural = "Endereços"

        # When
        meta = Address._meta

        # Then
        self.assertEqual(meta.verbose_name, expected_verbose_name)
        self.assertEqual(meta.verbose_name_plural, expected_verbose_name_plural)

    def test_address_create_raise_exception_when_missing_required_fields(self):
        # Given
        test_cases = [
            "street",
            "number",
            "neighborhood",
            "city",
            "zip_code",
            "description",
            "user",
            "latitude",
            "longitude",
        ]
        city = CityFactory()

        for attr_name in test_cases:
            # When
            with self.subTest(attr=attr_name):
                test_data = AddressFactory.address_data()
                test_data["city"] = city
                test_data["user"] = self.user
                test_data[attr_name] = None

                # Then
                with self.assertRaises(Exception):
                    Address.objects.create(**test_data)

    def test_address_create_raise_exception_when_zip_code_is_wrong(self):
        # Given
        test_data = AddressFactory.address_data()
        test_data["zip_code"] = "123456789"

        # When
        with self.assertRaises(Exception):
            Address.objects.create(**test_data)
