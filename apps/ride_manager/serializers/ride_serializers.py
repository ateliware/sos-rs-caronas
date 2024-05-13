from rest_framework import serializers

from apps.address_manager.serializers import CitySerializer
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.affected_place_serializer import (
    AffectedPlaceSerializer,
)
from apps.ride_manager.serializers.vehicle_serializers import (
    VehicleSerializer,
    VehicleSimpleSerializer,
)


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
            "whatsapp_group_link",
            "quantity_of_passengers",
            "notes",
            "status",
            "created_at",
        ]


class RideSearchSerializer(serializers.ModelSerializer):
    confirmed_passengers = serializers.IntegerField()
    origin = CitySerializer()
    destination = AffectedPlaceSerializer()
    vehicle = VehicleSimpleSerializer()

    class Meta:
        model = Ride
        fields = [
            "uuid",
            "date",
            "work_shift",
            "origin",
            "destination",
            "vehicle",
            "status",
            "quantity_of_passengers",
            "confirmed_passengers",
            "created_at",
        ]

    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        response_data["qtt_vacancies"] = (
            response_data["quantity_of_passengers"]
            - response_data["confirmed_passengers"]
        )
        return response_data
