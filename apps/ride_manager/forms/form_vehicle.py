from django import forms

from apps.ride_manager.models.vehicle import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["model", "color", "plate", "plate_picture", "vehicle_picture"]
