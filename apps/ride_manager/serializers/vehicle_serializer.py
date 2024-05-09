from rest_framework import serializers

from apps.core.serializers.base_64_serializer import Base64FileField
from apps.ride_manager.models.vehicle import Vehicle


class VehicleSerializer(serializers.ModelSerializer):

    plate_picture = Base64FileField(default_filename="plate_picture.jpg")
    vehicle_picture = Base64FileField(default_filename="vehicle_picture.jpg")

    class Meta:
        model = Vehicle
        fields = [
            "uuid",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
            "created_at",
        ]
