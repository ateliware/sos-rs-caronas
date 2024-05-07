from rest_framework import serializers

from apps.address_manager.models import City
from apps.address_manager.serializers.state_serializer import (
    NestedStateSerializer,
)


class CitySerializer(serializers.ModelSerializer):
    state = NestedStateSerializer()
    created_at = serializers.DateTimeField(format="%d/%m/%Y")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y")

    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "state",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class CityCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    state_code = serializers.CharField(required=True)
