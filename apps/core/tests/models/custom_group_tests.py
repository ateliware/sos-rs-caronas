from django.contrib.auth.models import Group

from apps.core.models import CustomGroup
from apps.core.tests.base_test import BaseTest


class CustomGroupTests(BaseTest):
    def test_proxy_inheritance(self):
        custom_group = CustomGroup.objects.create(name="Test Group")
        self.assertIsInstance(custom_group, CustomGroup)
        self.assertIsInstance(custom_group, Group)

    def test_proxy_verbose_name(self):
        self.assertEqual(CustomGroup._meta.verbose_name, "Grupo")
        self.assertEqual(CustomGroup._meta.verbose_name_plural, "Grupos")
        self.assertEqual(CustomGroup._meta.app_label, "core")
