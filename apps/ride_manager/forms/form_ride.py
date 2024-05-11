from django import forms

from apps.ride_manager.models.ride import Ride


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "quantity_of_passengers"
        ]
