from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response

from apps.core.apis.generic_viewset_user_validator import GenericUserViewSet
from apps.ride_manager.models.vehicle import Vehicle
from apps.ride_manager.serializers.person_register_serializers import (
    PersonModelSerializer,
)
from apps.ride_manager.serializers.vehicle_serializers import (
    VehicleRegisterSerializer,
    VehicleSerializer,
)


class VehicleViewset(GenericUserViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    http_method_names = ["get", "post"]

    @extend_schema(
        request=VehicleRegisterSerializer,
        responses={status.HTTP_201_CREATED: VehicleSerializer},
    )
    def create(self, request, *args, **kwargs):
        try:
            person = self.get_person()
            request_data = request.data.copy()

            cnh_number = request_data.pop("cnh_number", None)
            if isinstance(cnh_number, list):
                cnh_number = cnh_number[0]

            cnh_picture_64 = request_data.pop("cnh_picture", None)
            if isinstance(cnh_picture_64, list):
                cnh_picture_64 = cnh_picture_64[0]

            if not person.cnh_is_verified:
                if not cnh_number or not cnh_picture_64:
                    return Response(
                        {"message": "Número e foto da CNH são obrigatórios"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                person_update_data = {
                    "cnh_number": cnh_number,
                    "cnh_picture": cnh_picture_64,
                }

                person_serializer = PersonModelSerializer(
                    person,
                    data=person_update_data,
                    partial=True,
                )

                person_serializer.is_valid(raise_exception=True)
                person_serializer.save()

            request_data["person"] = person.uuid
            vehicle_serializer = VehicleSerializer(data=request_data)
            vehicle_serializer.is_valid(raise_exception=True)
            vehicle_serializer.save()

            return Response(
                vehicle_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
