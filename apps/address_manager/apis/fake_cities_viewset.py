from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.address_manager.tests.factories.city_factory import CityFactory


# It's possible write endpoint not vinculated with a model
class FakeCityViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = request.query_params
        qtt_cities = int(query_params.get("qtt_cities", 10))
        cities = list()

        for _ in range(qtt_cities):
            new_city = CityFactory.city_data()
            cities.append(new_city)

        response = {
            "cities": cities,
        }

        return Response(
            response,
            status=status.HTTP_200_OK,
        )
