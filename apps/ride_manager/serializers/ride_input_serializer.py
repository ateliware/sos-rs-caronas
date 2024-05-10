from rest_framework import serializers

from apps.core.serializers.base_64_serializer import Base64FileField
from apps.ride_manager.models.ride import Ride


class RideInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "quantity_of_passengers",
            "status",
            "notes",
        ]
