from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from apps.core.apis.generic_viewset_user_validator import GenericUserViewSet

from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.ride_input_serializer import (
    RideInputSerializer,
)
from apps.ride_manager.serializers.ride_output_serializer import (
    RideOutputSerializer,
)


class RideViewset(GenericUserViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideOutputSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        model = self.queryset.model
        person = self.get_person()

        queryset = model.objects.none()
        if person:
            queryset = model.objects.filter(driver=person).order_by(
                "-created_at"
            )
        return queryset

    @extend_schema(
        request=RideInputSerializer,
        responses={status.HTTP_201_CREATED: RideOutputSerializer},
    )
    def create(self, request, *args, **kwargs):
        driver = self.get_person()
        if not driver:
            return Response(
                {"message": "Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RideInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save(driver=driver)
        except ValidationError as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
