from apps.ride_manager.models.vehicle import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
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
        ]
