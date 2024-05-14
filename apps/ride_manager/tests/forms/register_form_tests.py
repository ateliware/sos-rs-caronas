from django.core.files.uploadedfile import SimpleUploadedFile

from apps.address_manager.tests.factories.city_factory import CityFactory
from apps.core.tests.base_test import BaseTest
from apps.ride_manager.forms import RegistrationForm
from apps.ride_manager.tests.factories.person_register_payload_factory import (
    person_register_payload_factory,
)
import io
# from pillow import Image

class RegistrationFormTests(BaseTest):   
    def test_placeholder_and_label(self):
        # Given
        form = RegistrationForm()

        # Then
        for field_name, (label, placeholder) in form.field_labels.items():
            self.assertEqual(form.fields[field_name].label, label)
            self.assertEqual(form.fields[field_name].widget.attrs['placeholder'], placeholder)


    def test_form_valid(self):
        # Given
        city = CityFactory()
        form_data = person_register_payload_factory()
        del form_data['avatar']
        del form_data['zip_code']
        del form_data['password_confirm']
        form_data["password_confirmation"] = form_data["password"]
        form_data['city_id'] = city.id
        form_data['state_id'] = city.state.id
        form_data["emergency_contact"] = self.fake.name()
        # image = Image.new('RGB', (100, 100), 'white')
        buffer = io.BytesIO()
        # image.save(buffer, format='PNG')
        document_picture = SimpleUploadedFile("document_picture.jpg", content=buffer.getvalue(), content_type="image/jpeg")
        form_data["document_picture"] = document_picture
        form = RegistrationForm(form_data, {"document_picture": document_picture})
        form.is_valid()
        print(form.is_valid())
        print(form.errors)
