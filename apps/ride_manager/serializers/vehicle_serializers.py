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
            "person",
            "model",
            "color",
            "plate",
            "plate_picture",
            "vehicle_picture",
            "is_verified",
            "created_at",
        ]


class VehicleRegisterSerializer(serializers.Serializer):
    model = serializers.CharField(max_length=255, required=True)
    color = serializers.CharField(max_length=255, required=True)
    plate = serializers.CharField(max_length=7, required=True)
    plate_picture = Base64FileField(default_filename="plate_picture.jpg")
    vehicle_picture = Base64FileField(default_filename="vehicle_picture.jpg")
    cnh_picture = Base64FileField(
        default_filename="cnh_picture.jpg", required=False
    )
    cnh_number = serializers.CharField(max_length=15, required=False)


class VehicleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "uuid",
            "model",
            "color",
            "plate",
            "is_verified",
        ]
