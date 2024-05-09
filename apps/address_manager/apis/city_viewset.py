from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.address_manager.models import City, State
from apps.address_manager.serializers.city_serializer import (
    CityCreateSerializer,
    CitySerializer,
)


# It's possible override standard methods, giving you more control over the behavior of the view
@extend_schema(request=CityCreateSerializer)
class CityViewSet(ModelViewSet):
    queryset = City.objects.all().order_by("pk")
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def create(self, request):
        city_name = request.data.get("name")
        state_code = request.data.get("state_code")

        if not city_name or not state_code:
            return Response(
                {"error": "name and state_code are required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            state = State.objects.filter(code=state_code).first()

            if not state:
                return Response(
                    {"error": "state not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            city = City.objects.create(
                name=city_name,
                state=state,
            )
            city_serialized = CitySerializer(city)
            return Response(
                city_serialized.data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, **kwargs):
        city_id = kwargs.get("pk")
        city_name = request.data.get("name")
        state_code = request.data.get("state_code", "").upper()

        if not city_name or not state_code:
            return Response(
                {"error": "name and state_code are required fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            city = City.objects.filter(pk=city_id).first()

            if not city:
                return Response(
                    {"error": "city not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            state = State.objects.filter(code=state_code).first()

            if not state:
                return Response(
                    {"error": "state not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            city.name = city_name
            city.state = state
            city.save()
            city_serialized = CitySerializer(city)
            return Response(
                city_serialized.data,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "partial update not allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Other methods are: list (get all items), retrieve (get one item), destroy(delete)
