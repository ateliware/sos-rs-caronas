from apps.core.apis.generic_viewset_user_validator import GenericUserViewSet
from apps.term_manager.models import TermAcceptance
from apps.term_manager.serializers import TermAcceptanceSerializer


class TermAcceptanceViewSet(GenericUserViewSet):
    serializer_class = TermAcceptanceSerializer
    queryset = TermAcceptance.objects.all()
    http_method_names = ["get", "post"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-created_at")
