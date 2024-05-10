from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.ride_manager.apis.filters.voluntary_search_filter import (
    VoluntarySearchFilter,
)
from apps.ride_manager.enums.voluntary_availability_status_choices import (
    VoluntaryAvailabilityStatusChoices,
)
from apps.ride_manager.models.voluntary import Voluntary
from apps.ride_manager.serializers.voluntary_serializers import (
    VoluntarySearchSerializer,
)


class VoluntarySearchViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    filterset_class = VoluntarySearchFilter
    serializer_class = VoluntarySearchSerializer

    def get_queryset(self):
        return Voluntary.objects.exclude(
            status=VoluntaryAvailabilityStatusChoices.CLOSED
        )

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        date = query_params.get("date")
        origin = query_params.get("origin")
        if not date or not origin:
            return Response(
                {"message": "Os campos 'date' e 'origin' são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().list(request, *args, **kwargs)
