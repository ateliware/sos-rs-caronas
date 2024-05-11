from django.urls import path

from apps.ride_manager.views.home import home_view
from apps.ride_manager.views.login import login_view
from apps.ride_manager.views.logout import logout_view
from apps.ride_manager.views.person import PersonView
from apps.ride_manager.views.ride import create_ride
from apps.ride_manager.views.vehicle import create_vehicle

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home_view, name="home"),
    path("person/create/", PersonView.create, name="register"),
    path("ride/create/", create_ride, name="create_ride"),
    path("vehicle/add/", create_vehicle, name="add_vehicle"),
]
