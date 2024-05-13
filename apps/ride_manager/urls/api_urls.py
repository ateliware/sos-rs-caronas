from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ride_manager.apis import (
    AffectedPlaceViewSet,
    PersonRegisterViewSet,
    RideSearchViewSet,
    RideViewset,
    ValidatePhoneCheckCodeApiView,
    ValidatePhoneSendCodeApiView,
    VehicleViewset,
    VoluntaryViewset,
)

router = DefaultRouter()

router.register(r"rides", RideViewset, basename="rides")
router.register(r"vehicles", VehicleViewset, basename="vehicles")
router.register(r"voluntaries", VoluntaryViewset, basename="voluntaries")

router.register(
    r"affected_places", AffectedPlaceViewSet, basename="affected_places"
)

urlpatterns = [
    path(
        "validate_phone/send_code/",
        ValidatePhoneSendCodeApiView.as_view(),
        name="validate_phone_send_code",
    ),
    path(
        "validate_phone/check_code/",
        ValidatePhoneCheckCodeApiView.as_view(),
        name="validate_phone_check_code",
    ),
    path(
        "person/register/",
        PersonRegisterViewSet.as_view({"post": "create"}),
        name="person_register",
    ),
    path(
        "rides/search/",
        RideSearchViewSet.as_view({"get": "list"}),
        name="rides_search",
    ),
]

urlpatterns += router.urls
