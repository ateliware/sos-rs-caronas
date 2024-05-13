from django.urls import path

from apps.ride_manager.views.home import home_view, public_home
from apps.ride_manager.views.login import login_view
from apps.ride_manager.views.logout import logout_view
from apps.ride_manager.views.register import (
    register,
    send_verify_code,
    validate_code,
)
from apps.ride_manager.views.ride import (
    create_ride,
    my_rides,
    open_rides,
    ride_detail,
    ride_solicitation,
    ride_passenger_confirmation,
)
from apps.ride_manager.views.vehicle import create_vehicle, created_with_success


urlpatterns = [
    path("", public_home, name="public_home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home_view, name="home"),
    path("register/", register, name="register"),
    path("send_verify_code/", send_verify_code, name="send_verify_code"),
    path("validate_code/", validate_code, name="validate_code"),
    path("ride/detail/<uuid:ride_id>/", ride_detail, name="ride_detail"),
    path("ride/create/", create_ride, name="create_ride"),
    path("ride/my-rides/", my_rides, name="my_rides"),
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
    path("rides/", open_rides, name="list_rides"),
    path("vehicle/add/", create_vehicle, name="add_vehicle"),
    path("vehicle/success/", created_with_success, name="success_vehicle_save"),
]