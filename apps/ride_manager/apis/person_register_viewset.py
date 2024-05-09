from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.core.serializers.standard_response_serializer import (
    StandardResponseSerializer,
    StandardResponseSerializerError,
)
from apps.ride_manager.serializers.person_register_serializers import (
    PersonModelSerializer,
    PersonRegisterSerializer,
)
from apps.ride_manager.services.person_register_service import (
    PersonRegisterService,
)


class PersonRegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PersonRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: PersonModelSerializer,
            status.HTTP_400_BAD_REQUEST: StandardResponseSerializer,
            status.HTTP_404_NOT_FOUND: StandardResponseSerializer,
        },
    )
    def create(self, request):
        try:
            serializer = PersonRegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            service = PersonRegisterService(data=serializer.validated_data)
            phone_is_valid = service.check_phone_validation()

            if not phone_is_valid:
                raise Response(
                    {"message": "Telefone não validado"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response = service.register_person()

            return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            response = {
                "errors": str(e),
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
