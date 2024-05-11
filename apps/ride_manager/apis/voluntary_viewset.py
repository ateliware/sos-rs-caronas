from apps.core.apis.generic_viewset_user_validator import GenericUserViewSet
from apps.ride_manager.models.voluntary import Voluntary
from apps.ride_manager.serializers.voluntary_serializers import (
    VoluntaryRegisterSerializer,
)


class VoluntaryViewset(GenericUserViewSet):
    queryset = Voluntary.objects.all()
    serializer_class = VoluntaryRegisterSerializer
    http_method_names = ["post"]
