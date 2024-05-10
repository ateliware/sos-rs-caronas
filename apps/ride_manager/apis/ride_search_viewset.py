from datetime import date

from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.ride_manager.apis.filters.ride_filter import RideFilter
from apps.ride_manager.models.passenger import (
    StatusChoices as PassengerStatusChoices,
)
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.ride_output_serializer import (
    RideOutputSerializer,
)


class RideSearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    filterset_class = RideFilter
    serializer_class = RideOutputSerializer

    def get_queryset(self):
        queryset = Ride.objects.all(
        ).annotate(
            qtt_passengers=Count("passenger")
        )
        # ).filter(
        #     passenger__status=PassengerStatusChoices.ACCEPTED,
        # )
        return queryset
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
