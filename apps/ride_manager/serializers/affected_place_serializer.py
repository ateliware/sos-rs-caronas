from rest_framework import serializers

from apps.address_manager.serializers.city_serializer import CitySerializer
from apps.ride_manager.models.affected_place import AffectedPlace


class AffectedPlaceSerializer(serializers.ModelSerializer):

    city = CitySerializer()

    class Meta:
        model = AffectedPlace
        fields = [
            "uuid",
            "description",
            "address",
            "city",
            "main_person",
            "main_contact",
            "informations",
        ]
