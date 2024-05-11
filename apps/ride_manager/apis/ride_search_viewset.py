from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ride_manager.apis.filters.ride_filter import RideFilter
from apps.ride_manager.models.passenger import (
    StatusChoices as PassengerStatusChoices,
)
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.ride_serializers import RideSearchSerializer


class RideSearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    filterset_class = RideFilter
    serializer_class = RideSearchSerializer

    def get_queryset(self):
        queryset = Ride.objects.all().annotate(
            confirmed_passengers=Count(
                "passenger",
                filter=Q(passenger__status=PassengerStatusChoices.ACCEPTED),
            )
        )
        return queryset
