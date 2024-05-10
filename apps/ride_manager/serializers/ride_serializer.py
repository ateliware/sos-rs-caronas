from rest_framework import serializers

from apps.ride_manager.models.ride import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "whatspp_group_link",
            "notes",
            "status",
            "created_at",
        ]
