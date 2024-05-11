from django.shortcuts import redirect, render

from apps.address_manager.models.city import City
from apps.ride_manager.forms.form_ride import RideForm
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.vehicle import Vehicle


def create_ride(request):
    """
    First we get the logged in user, then we check if the user has a vehicle verified.
    If the driver fas a vehicle verified, we create a ride.
    Otherwise, we redirect the user to the vehicle creation page.
    """
    user = request.user
    if not Vehicle.objects.filter(is_verified=True, person__user=user).exists():
        return redirect("add_vehicle")

    vehicle = Vehicle.objects.filter(
        is_verified=True, person__user=user
    ).first()
    affetced_places = AffectedPlace.objects.all()
    cities = City.objects.all()

    print("cities", cities)

    if request.method == "POST":
        form = RideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
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
