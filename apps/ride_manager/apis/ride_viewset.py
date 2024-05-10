import logging

from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.ride_manager.models.person import Person
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.serializers.ride_serializer import RideSerializer


class RideViewset(ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        model = self.queryset.model
        person = self.get_person()

        queryset = model.objects.none()
        if person:
            queryset = model.objects.filter(driver=person).order_by(
                "-created_at"
            )
        return queryset

    def perform_create(self, serializer):
        person = self.get_person()
        if person:
            return serializer.save(driver=person)
        raise ValidationError("Missing Authenticated User.")

    def get_person(self):
        person = None
        try:
            person = Person.objects.get(user=self.request.user)
        except Person.DoesNotExist:
            logging.error(
                "Authenticated client is not a valid registered user."
            )
        return person
