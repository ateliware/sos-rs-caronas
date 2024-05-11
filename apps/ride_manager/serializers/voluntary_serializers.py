from rest_framework import serializers

from apps.ride_manager.models.voluntary import Voluntary


class VoluntaryRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voluntary
        fields = [
            "origin",
            "destination",
            "any_destination",
            "date",
            "work_shift",
        ]
