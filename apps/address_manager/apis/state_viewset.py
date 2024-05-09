from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.address_manager.apis.filters.state_filter import StateFilter
from apps.address_manager.models import State
from apps.address_manager.serializers.state_serializer import StateSerializer


class StateViewSet(ModelViewSet):
    queryset = State.objects.all().order_by("pk")
    serializer_class = StateSerializer
    permission_classes = [AllowAny]
    filterset_class = StateFilter
