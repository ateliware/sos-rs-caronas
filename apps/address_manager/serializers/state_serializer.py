from rest_framework import serializers

from apps.address_manager.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            "id",
            "name",
            "code",
            "is_active",
        ]
        read_only_fields = [
            "id",
        ]


class NestedStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            "id",
            "name",
            "code",
        ]
        read_only_fields = [
            "id",
        ]
