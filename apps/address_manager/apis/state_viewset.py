from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.address_manager.apis.filters.state_filter import StateFilter
from apps.address_manager.models import State
from apps.address_manager.serializers.state_serializer import StateSerializer


# This is the most easy way to create a ViewSet, just inherit from viewsets.ModelViewSet
class StateViewSet(ModelViewSet):
    queryset = State.objects.all().order_by("pk")
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = StateFilter
