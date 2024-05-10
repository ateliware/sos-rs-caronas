from rest_framework import serializers

from apps.ride_manager.models.voluntary import Voluntary
from apps.ride_manager.serializers.person_register_serializers import (
    PersonSimpleSerializer,
)


class VoluntarySearchSerializer(serializers.ModelSerializer):
    person = PersonSimpleSerializer(read_only=True)

    class Meta:
        model = Voluntary
        fields = [
            "id",
            "person",
            "origin",
            "destination",
            "work_shift",
            "status",
            "created_at",
        ]
