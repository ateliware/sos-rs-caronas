from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.ride_manager.serializers.person_register_serializers import (
    PersonRegisterResponseSerializer,
    PersonRegisterSerializer,
)


class PersonRegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PersonRegisterSerializer,
        responses={status.HTTP_200_OK: PersonRegisterResponseSerializer},
    )
    def create(self, request):
        try:
            serializer = PersonRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response("teste", status=status.HTTP_201_CREATED)

        except Exception as e:
            response = {
                "errors": str(e),
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)