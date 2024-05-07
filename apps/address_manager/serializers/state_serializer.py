from rest_framework import serializers

from apps.address_manager.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            "id",
            "name",
            "code",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
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
