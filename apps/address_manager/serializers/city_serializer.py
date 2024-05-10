from rest_framework import serializers

from apps.address_manager.models import City
from apps.address_manager.serializers.state_serializer import (
    NestedStateSerializer,
)


class CitySerializer(serializers.ModelSerializer):
    state = NestedStateSerializer()

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "state",
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]


class CityCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    state_code = serializers.CharField(required=True)
