import logging

from django.shortcuts import redirect, render

from apps.ride_manager.forms.form_vehicle import VehicleForm
from apps.ride_manager.models.person import Person


def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.person = get_person(request)

            vehicle.save()
            return redirect(
                "create_ride"
            )  # Redirect to a success page or another view
    else:
        form = VehicleForm()
    return render(request, "create_vehicle.html", {"form": form})


def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person
