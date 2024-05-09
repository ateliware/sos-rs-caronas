from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.address_manager.apis import CityViewSet, StateViewSet

router = DefaultRouter()
router.register(r"states", StateViewSet, basename="states")
router.register(r"cities", CityViewSet, basename="cities")

urlpatterns = []
urlpatterns += router.urls
