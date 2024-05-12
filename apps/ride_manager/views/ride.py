import logging

from django.db.models import Count
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from apps.address_manager.models.city import City
from apps.ride_manager.forms.form_ride import RideForm
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.passenger import Passenger
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.ride import Ride
from apps.ride_manager.models.vehicle import Vehicle

@login_required(login_url="/login/")
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
                    "ride/create_ride.html",
                    {"form": form, "error": "Erro ao salvar dados da carona."},
                )
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = RideForm()

    return render(
        request,
        "ride/create_ride.html",
        {
            "form": form,
            "vehicle": vehicle,
            "cities": cities,
            "affected_places": affetced_places,
            "affected_places": affetced_places,
        },
    )

@login_required(login_url="/login/")
def my_rides(request):
    """
    List all rides that the logged user is the driver
    """
    rides = Ride.objects.filter(driver__user=request.user).order_by("-date")

    context = {"rides": rides}
    return render(request, "ride/my_rides.html", context)

@login_required(login_url="/login/")
def open_rides(request):
    """
    List all rides available for the logged in user
    """
    if request.user.is_anonymous:
        rides = Ride.objects.filter(status="OPEN").annotate(
            num_passengers=Count("passenger")
        )
    else:
        rides = Ride.objects.filter(status="OPEN").exclude(
            driver__user=request.user
        ).annotate(num_passengers=Count("passenger"))

    context = {"rides": rides}
    return render(request, "ride/list_ride.html", context)

@login_required(login_url="/login/")
def ride_detail(request, ride_id):
    """
    Show the details of a ride
    """
    
    ride = Ride.objects.get(uuid=ride_id)

    is_driver = False
    if request.user == ride.driver.user:
        is_driver = True
        passengers = Passenger.objects.filter(ride__uuid=ride_id)
    else:
        passengers = Passenger.objects.filter(ride__uuid=ride_id, status="ACCEPTED")
    
    context = {"ride": ride, "passengers": passengers, "is_driver": is_driver}
    return render(request, "ride/ride_detail.html", context)

def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person
