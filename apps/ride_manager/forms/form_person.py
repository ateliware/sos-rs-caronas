from django import forms

from apps.ride_manager.models.person import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"  # Use all fields from the Person model
