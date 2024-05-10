import logging

from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.ride_manager.models.passenger import Passenger
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.ride_input_serializer import (
    RideInputSerializer,
)
from apps.ride_manager.serializers.ride_output_serializer import (
    RideOutputSerializer,
)
from apps.ride_manager.serializers.passenger_serializer import (
    PassengerSerializer,
)


class RideViewset(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideOutputSerializer
    permission_classes = [IsAuthenticated]
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

    @action(detail=True, methods=["get"], url_path="passengers")
    def get_passengers(self, request, pk=None):
        """
        From a given ride uuid, received as query param
        retrieves all passengers associated with it, serialize them,
        and then return the list of passengers.
        """
        try:
            ride = self.get_object()
            passengers = Passenger.objects.filter(ride=ride)
            serializer = PassengerSerializer(passengers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response(
                [{"message": "Carona não encontrada"}],
                status=status.HTTP_404_NOT_FOUND,
            )

    def get_person(self):
        person = None
        try:
            person = Person.objects.get(user=self.request.user)
        except Person.DoesNotExist:
            logging.error(
                "Authenticated client is not a valid registered user."
            )
        return person
