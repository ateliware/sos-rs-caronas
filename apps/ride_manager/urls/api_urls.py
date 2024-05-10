from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ride_manager.apis import (
    PersonRegisterViewSet,
    RideViewset,
    ValidatePhoneCheckCodeApiView,
    ValidatePhoneSendCodeApiView,
    VehicleViewset,
    VoluntarySearchViewSet,
)

router = DefaultRouter()

router.register(r"vehicles", VehicleViewset, basename="vehicles")
router.register(r"rides", RideViewset, basename="rides")

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
        "voluntaries/search/",
        VoluntarySearchViewSet.as_view({"get": "list"}),
        name="voluntary_search",
    ),
]

urlpatterns += router.urls
