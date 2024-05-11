import logging

from django.shortcuts import redirect, render

from apps.ride_manager.forms.form_vehicle import VehicleForm
from apps.ride_manager.models.person import Person


def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST, request.FILES)

        print("\n\n-----------HERE\n\n")
        if form.is_valid():
            print("Form is valid.")
            cnh_number = form.cleaned_data.get('cnh_number')
            cnh_picture = request.FILES.get('cnh_picture')

            person = get_person(request)
            print("\n\n-----------HERE\n\n")
            print(person)
            if person:
                print("Person found.")
                person.cnh_number = cnh_number
                if cnh_picture:  # Ensure a file was uploaded
                    person.cnh_picture = cnh_picture
                print("Person data updated.")
                try:
                    person.save()
                except Exception as e:
                    logging.error(f"Error saving person data: {e}")
                    return render(request, "create_vehicle.html", {"form": form, "error": "Erro ao salvar dados do usuário."})
                print("Person data saved.")
                vehicle = form.save(commit=False)
                print("Vehicle data saved 1.")
                vehicle.person = person
                try:
                    vehicle.save()
                    print("Vehicle data saved2.")
                except Exception as e:
                    logging.error(f"Error saving vehicle data: {e}")
                    return render(request, "create_vehicle.html", {"form": form, "error": "Erro ao salvar dados do veículo."})

                return redirect("success_vehicle_save")
        else:
            logging.error("Invalid form data.")
            print(form.errors)
           
    else:
        form = VehicleForm()
    return render(request, "create_vehicle.html", {"form": form})

def created_with_success(request):
    return render(request, "created_with_success.html")

def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person
