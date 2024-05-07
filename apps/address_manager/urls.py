from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.address_manager.apis import CityViewSet, FakeCityViewSet, StateViewSet
from apps.address_manager.views import CityView

router = DefaultRouter()
router.register(r"api/states", StateViewSet, basename="states")
router.register(r"api/cities", CityViewSet, basename="cities")

urlpatterns = [
    path(
        "api/fake-cities/",
        FakeCityViewSet.as_view(),
        name="fake-cities",
    ),
    path(
        "city/",
        CityView.as_view(),
        name="list_cities",
    ),
]
urlpatterns += router.urls
