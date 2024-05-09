from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class GenericUserViewSet(ModelViewSet):
    """
    This is a Generic ViewSet used for authenticated requests
    which the user must be the owner of the object(s)
    that the request must performs
    """

    serializer_class = None  # Subclasses must define this atribute
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        model = self.queryset.model
        user = self.request.user

        queryset = model.objects.none()
        if user:
            queryset = model.objects.filter(person=user).order_by("-created_at")
        return queryset

    def perform_create(self, serializer):
        person = self.request.user
        if person:
            return serializer.save(person=person)
        raise ValidationError("Missing Authenticated User.")
