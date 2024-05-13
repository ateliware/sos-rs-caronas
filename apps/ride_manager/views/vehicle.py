import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.ride_manager.forms.form_vehicle import VehicleForm
from apps.ride_manager.models.person import Person
from apps.ride_manager.models.vehicle import Vehicle


@login_required(login_url="/login/")
def create_vehicle(request):
    """
    Before add a new vehicle we check if the person has a submission waiting for approval.
    If there is we redirect to the success_vehicle_save page.
    """
    person = get_person(request)
    if Vehicle.objects.filter(person=person, is_verified=False).exists() and not person.cnh_is_verified:
        return redirect("success_vehicle_save")
    
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)

        if form.is_valid():
            cnh_number = form.cleaned_data.get("cnh_number")
            cnh_picture = request.FILES.get("cnh_picture")

            if person:
                person.cnh_number = cnh_number
                if cnh_picture:  # Ensure a file was uploaded
                    person.cnh_picture = cnh_picture
                try:
                    person.save()
                except Exception as e:
                    logging.error(f"Error saving person data: {e}")
                    return render(
                        request,
                        "ride/create_vehicle.html",
                        {
                            "form": form,
                            "error": "Erro ao salvar dados do usuário.",
                        },
                    )

                vehicle = form.save(commit=False)
                vehicle.person = person
                try:
                    vehicle.save()
                except Exception as e:
                    logging.error(f"Error saving vehicle data: {e}")
                    return render(
                        request,
                        "ride/create_vehicle.html",
                        {
                            "form": form,
                            "error": "Erro ao salvar dados do veículo.",
                        },
                    )
                return redirect("success_vehicle_save")
        else:
            logging.error("Invalid form data.")

    else:
        form = VehicleForm()
    return render(request, "ride/create_vehicle.html", {"form": form})


@login_required(login_url="/login/")
def created_with_success(request):
    return render(request, "ride/vehicle_created_with_success.html")


def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person
