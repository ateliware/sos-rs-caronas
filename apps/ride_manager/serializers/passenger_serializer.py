from rest_framework import serializers

from apps.ride_manager.models.passenger import Passenger
from apps.ride_manager.serializers.person_serializer import PersonSerializer


class PassengerSerializer(serializers.ModelSerializer):

    person = PersonSerializer()

    class Meta:
        model = Passenger
        fields = [
            "uuid",
            "person",
            "is_driver",
            "status",
        ]
