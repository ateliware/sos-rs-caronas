from django import forms

from apps.ride_manager.models.ride import Ride


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = "__all__"  # Use all fields from the Person model
