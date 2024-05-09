from django.forms import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.term_manager.models import TermAcceptance
from apps.term_manager.serializers import TermAcceptanceSerializer


class TermAcceptanceViewSet(ModelViewSet):
    serializer_class = TermAcceptanceSerializer
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user:
            return TermAcceptance.objects.none()

        queryset = TermAcceptance.objects.filter(user=user).order_by(
            "-created_at"
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user:
            return serializer.save(user=user)
        raise ValidationError("Missing Authenticated User.")
