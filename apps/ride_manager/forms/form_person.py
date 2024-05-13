from django import forms

from apps.ride_manager.models.person import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "phone",
            "emergency_phone",
            "emergency_contact",
            "city",
            "birth_date",
            "avatar",
            "document_picture",
        ]
