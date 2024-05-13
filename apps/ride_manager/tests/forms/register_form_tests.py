from django.core.files.uploadedfile import SimpleUploadedFile

from apps.core.tests.base_test import BaseTest
from apps.ride_manager.forms import RegistrationForm


class RegistrationFormTests(BaseTest):   
    def test_placeholder_and_label(self):
        # Given
        form = RegistrationForm()

        # Then
        for field_name, (label, placeholder) in form.field_labels.items():
            self.assertEqual(form.fields[field_name].label, label)
            self.assertEqual(form.fields[field_name].widget.attrs['placeholder'], placeholder)


