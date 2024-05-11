import logging

from django.db.models import Count
from django.shortcuts import redirect, render

from apps.address_manager.models.city import City
from apps.ride_manager.forms.form_ride import RideForm
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.models.vehicle import Vehicle


def create_ride(request):
    """
    First we get the logged in user, then we check if the user has a vehicle verified.
    If the driver has a vehicle verified, we create a ride.
    Otherwise, we redirect the user to the vehicle creation page.
    """
    user = request.user
    if not Vehicle.objects.filter(is_verified=True, person__user=user).exists():
        return redirect("add_vehicle")
    if not Person.objects.filter(user=user, cnh_is_verified=True).exists():
        return redirect("success_vehicle_save")

    vehicle = Vehicle.objects.filter(
        is_verified=True, person__user=user
    ).first()
    affetced_places = AffectedPlace.objects.all()
    cities = City.objects.all()

    if request.method == "POST":
        form = RideForm(request.POST, request.FILES)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.driver = get_person(request)

            try:
                ride.save()
            except Exception as e:
                logging.error(f"Error saving ride data: {e}")
                return render(
                    request,
                    "create_ride.html",
                    {"form": form, "error": "Erro ao salvar dados da carona."},
                )
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = RideForm()

    return render(
        request,
        "create_ride.html",
        {
            "form": form,
            "vehicle": vehicle,
            "cities": cities,
            "affected_places": affetced_places,
            "affected_places": affetced_places,
        },
    )


def my_rides(request):
    """
    List all rides that the logged user is the driver
    """
    rides = Ride.objects.filter(driver__user=request.user).order_by("-date")
    return render(request, "my_rides.html", {"rides": rides})


def open_rides(request):
    """
    List all rides available for the logged in user
    """
    rides = Ride.objects.filter(status="OPEN").annotate(
        num_passengers=Count("passenger")
    )
    return render(request, "list_ride.html", {"rides": rides})


def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person
