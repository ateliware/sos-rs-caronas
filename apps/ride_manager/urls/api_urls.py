from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.ride_manager.apis import (
    validate_phone_check_code,
    validate_phone_send_code,
)

router = DefaultRouter()
urlpatterns = [
    path(
        "validate_phone/send_code/",
        validate_phone_send_code.ValidatePhoneSendCodeApiView.as_view(),
    ),
    path(
        "validate_phone/check_code/",
        validate_phone_check_code.ValidatePhoneCheckCodeApiView.as_view(),
    ),
]

urlpatterns += router.urls
