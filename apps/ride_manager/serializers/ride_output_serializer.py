from rest_framework import serializers

from apps.address_manager.serializers import CitySerializer
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.affected_place_serializer import (
    AffectedPlaceSerializer,
)
from apps.ride_manager.serializers.vehicle_serializer import VehicleSerializer


class RideOutputSerializer(serializers.ModelSerializer):

    origin = CitySerializer()
    destination = AffectedPlaceSerializer()
    vehicle = VehicleSerializer()

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
            "whatsapp_group_link",
            "notes",
            "status",
            "created_at",
        ]
