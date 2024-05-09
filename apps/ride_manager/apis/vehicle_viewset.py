from apps.core.apis.generic_viewset_user_validator import GenericUserViewSet
from apps.ride_manager.models.vehicle import Vehicle
from apps.ride_manager.serializers.vehicle_serializer import VehicleSerializer


class VehicleViewset(GenericUserViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
