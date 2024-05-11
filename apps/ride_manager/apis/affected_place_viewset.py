from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.serializers.affected_place_serializer import (
    AffectedPlaceSerializer,
)


class AffectedPlaceViewSet(viewsets.ModelViewSet):
    queryset = AffectedPlace.objects.all().order_by("city__name")
    serializer_class = AffectedPlaceSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
