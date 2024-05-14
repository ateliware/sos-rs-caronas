from django.urls import reverse
from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.forms import RegistrationForm
from apps.ride_manager.tests.factories.person_register_payload_factory import (
    person_register_form_data_factory,
    image_file_for_form_factory,
)
from apps.core.models.custom_user import CustomUser
from apps.term_manager.tests.factories.term_factory import TermFactory
from apps.term_manager.enums.term_choices import TermTypeChoices


class RegistrationFormViewTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("register")
        self.city = CityFactory()
        self.form_data = person_register_form_data_factory()
        self.form_data['city_id'] = self.city.id
        self.form_data['state_id'] = self.city.state.id
        self.document_picture = image_file_for_form_factory()
        self.form_data["document_picture"] = self.document_picture

    def test_get_context_data(self):
        # Given in setUp

        # When
        response = self.view_unauth_client.get(self.url)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn("states", response.context)
        self.assertIn("cities", response.context)
        self.assertIn("privacy_policy", response.context)
        self.assertIn("term_of_use", response.context)

    def test_form_valid(self):
        # Given
        TermFactory(type=TermTypeChoices.USE)
        TermFactory(type=TermTypeChoices.PRIVACY)
        form = RegistrationForm(self.form_data, {"document_picture": self.document_picture})

        # When
        response = self.view_unauth_client.post(
            path=self.url, 
            data=form.data,
            files={"document_picture": self.document_picture},
            )
        created_user = CustomUser.objects.filter(
            cpf=self.form_data["cpf"]
        ).first()
        
        # Then
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertIsNotNone(created_user)