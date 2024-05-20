from django.urls import path

from apps.ride_manager.views import (
    CustomLoginView,
    HomeView,
    RegistrationFormView,
)
from apps.ride_manager.views.home import about, home_view
from apps.ride_manager.views.logout import logout_view
from apps.ride_manager.views.register import send_verify_code, validate_code
from apps.ride_manager.views.ride import (
    create_ride,
    my_rides,
    ride_detail,
    ride_list,
    ride_passenger_confirmation,
    ride_solicitation,
)
from apps.ride_manager.views.vehicle import create_vehicle, created_with_success

urlpatterns = [
    path(
        "",
        ride_list,
        name="ride_list",
    ),
    path(
        "login/",
        CustomLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        logout_view,
        name="logout",
    ),
    path(
        "home/",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "about/",
        about,
        name="about",
    ),
    path(
        "register/",
        RegistrationFormView.as_view(),
        name="register",
    ),
    path(
        "send_verify_code/",
        send_verify_code,
        name="send_verify_code",
    ),
    path(
        "validate_code/",
        validate_code,
        name="validate_code",
    ),
    path(
        "ride/detail/<uuid:ride_id>/",
        ride_detail,
        name="ride_detail",
    ),
    path(
        "ride/create/",
        create_ride,
        name="create_ride",
    ),
    path(
        "ride/my-rides/",
        my_rides,
        name="my_rides",
    ),
    path(
        "ride/solicitation/<uuid:ride_id>",
        ride_solicitation,
        name="ride_solicitation",
    ),
    path(
        "ride/confirmation/<uuid:ride_id>/<uuid:passenger_id>",
        ride_passenger_confirmation,
        name="ride_passenger_confirmation",
    ),
    # set a path for rides with filter containing the origin, destinatino and date parameters
    path(
        "rides/<str:origin>/<str:destination>/<str:date>/",
        ride_list,
        name="list_rides",
    ),
    path(
        "rides/",
        ride_list,
        name="list_rides",
    ),
    path(
        "vehicle/add/",
        create_vehicle,
        name="add_vehicle",
    ),
    path(
        "vehicle/success/",
        created_with_success,
        name="success_vehicle_save",
    ),
]
