import logging
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from apps.address_manager.models.city import City
from apps.ride_manager.forms.form_ride import RideForm
from apps.ride_manager.models.affected_place import AffectedPlace
from apps.ride_manager.models.passenger import (
    Passenger,
    StatusChoices as PassengerStatusChoices,
)
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
            request.session["message"] = "Carona cadastrada com sucesso."
            return redirect("ride_detail", ride_id=ride.uuid)
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
        },
    )


@login_required(login_url="/login/")
def my_rides(request):
    """
    List all rides that the logged user is the driver
    """

    message = ""
    # Retrieving rides where the logged in user is the driver
    rides_as_driver = Ride.objects.filter(driver__user=request.user).annotate(
        confirmed_passengers_count=Count(
            "passenger",
            filter=Q(passenger__status=PassengerStatusChoices.ACCEPTED),
        )
    )

    # checking if need confirmation in the rides that the user is the driver
    for ride in rides_as_driver:
        ride.has_passenger_waiting_confirmation = Passenger.objects.filter(
            ride=ride, status=PassengerStatusChoices.PENDING
        ).exists()
        if ride.has_passenger_waiting_confirmation:
            message = "Você tem passageiros aguardando confirmação."

    # rides that the user is passenger
    passenger_rides = Passenger.objects.filter(person__user=request.user)
    passenger_ride_ids = [passenger.ride.uuid for passenger in passenger_rides]
    rides_as_passenger = Ride.objects.filter(
        uuid__in=passenger_ride_ids
    ).annotate(
        confirmed_passengers_count=Count(
            "passenger",
            filter=Q(passenger__status=PassengerStatusChoices.ACCEPTED),
        )
    )

    # add to rideas_as_passenger the status of the passenger in the ride
    for ride in rides_as_passenger:
        passenger = Passenger.objects.get(ride=ride, person__user=request.user)
        ride.passenger_status = passenger.status

    context = {
        "rides_as_driver": rides_as_driver,
        "rides_as_passenger": rides_as_passenger,
        "message": message,
    }
    return render(request, "ride/my_rides.html", context)


def ride_list(request):
    """
    List all rides available for the logged in user
    """

    filters = {"status": "OPEN"}
    origin = request.GET.get("origin")
    destination = request.GET.get("destination")
    date = request.GET.get("date")
    applyed_filters_str = "Nenhum filtro aplicado."

    if origin:
        city = City.objects.get(id=origin)
        applyed_filters_str = f"Filtrando por: saindo de {city}"
        filters["origin"] = origin
    if destination:
        if destination == "any_destination":
            applyed_filters_str += ", para qualquer destino"
        else:
            destination = AffectedPlace.objects.get(uuid=destination)
            applyed_filters_str += f", para {destination}"
            filters["destination"] = destination
    if date:
        formated_data = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        applyed_filters_str += f" no dia {formated_data}."
        filters["date"] = date
    else:
        filters["date__gte"] = datetime.now().date()

    if request.user.is_anonymous:
        # filter rides open and date >= today
        rides = (
            Ride.objects.filter(**filters)
            .annotate(
                confirmed_passengers_count=Count(
                    "passenger",
                    filter=Q(passenger__status=PassengerStatusChoices.ACCEPTED),
                )
            )
            .order_by("-date")
        )
    else:
        rides = (
            Ride.objects.filter(**filters)
            .annotate(
                confirmed_passengers_count=Count(
                    "passenger",
                    filter=Q(passenger__status=PassengerStatusChoices.ACCEPTED),
                )
            )
            .exclude(driver__user=request.user)
        ).order_by("-date")

    affected_places = AffectedPlace.objects.all().order_by("city")
    cities = City.objects.all().order_by("name")
    context = {
        "rides": rides,
        "affected_places": affected_places,
        "cities": cities,
        "filters": applyed_filters_str,
    }
    return render(request, "ride/list_ride.html", context)


@login_required(login_url="/login/")
def ride_detail(request, ride_id):
    """
    Show the details of a ride
    The ride has some rule to show informations.
    If the user logged in is the driver, we show all passengers and their status.
    If the user logged in is a passenger confirmed in the ride, we'll show all the informations too.
    However if the user in not the driver and is not a passenger confirmed in the ride, we'll show only the basic ride informations.
    And if he is as a passenger in the ride, but not confirmed, we'll show the basic informations his informations.
    """
    ride = Ride.objects.get(uuid=ride_id)
    passengers = Passenger.objects.filter(ride__uuid=ride_id).order_by("status")

    message, referer = mount_header(request)
    if request.user == ride.driver.user:
        is_driver = True
        context = {
            "ride": ride,
            "passengers": passengers,
            "is_driver": is_driver,
            "message": message,
            "referer": referer,
        }
        return render(request, "ride/ride_detail.html", context)

    is_driver = False
    # check if the logged in user is in the passengers list
    is_passenger_in_ride = request.user in [
        passenger.person.user for passenger in passengers
    ]

    is_passenger_confirmed = False
    if is_passenger_in_ride:
        passenger_status = [
            passenger.status
            for passenger in passengers
            if passenger.person.user == request.user
        ]
        is_passenger_confirmed = (
            passenger_status[0] == PassengerStatusChoices.ACCEPTED
        )

    if not is_passenger_in_ride:
        passengers = []
    elif is_passenger_in_ride and not is_passenger_confirmed:
        # if the user is a passenger in the ride, but not confirmed
        # return just him as passenger
        passengers = Passenger.objects.filter(
            ride__uuid=ride_id, person__user=request.user
        )

    context = {
        "ride": ride,
        "passengers": passengers,
        "is_driver": is_driver,
        "message": message,
        "referer": referer,
        "is_passenger_in_ride": is_passenger_in_ride,
        "is_passenger_confirmed": is_passenger_confirmed,
    }
    return render(request, "ride/ride_detail.html", context)


@login_required(login_url="/login/")
def ride_passenger_confirmation(request, ride_id, passenger_id):
    """
    Confirm or deny a passenger in a ride,
    verifying the availability of passenger seats, in the case of confirmation.
    This information is in the ride object, quantity_of_passengers attribute.
    It is necessary check if the logged in user is the driver
    """

    ride = Ride.objects.get(uuid=ride_id)
    if request.user != ride.driver.user:
        message = "Somente o motorista da corrida pode aceitar passageiros."
        return ride_detail(request, ride_id=ride_id, message=message)

    confirmed_passengers = Passenger.objects.filter(
        ride=ride, status=PassengerStatusChoices.ACCEPTED
    ).count()
    if confirmed_passengers == ride.quantity_of_passengers:
        message = "Infelizmente não há mais vagas disponíveis para esta carona."
    elif Passenger.objects.filter(
        ride=ride, person__user=request.user
    ).exists():
        message = "O passageiro já está confirmado nesta carona."
    else:
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.status = PassengerStatusChoices.ACCEPTED
        passenger.save()
        message = "Passageiro confirmado com sucesso."

    # save message in session to show in the ride detail page
    request.session["message"] = message
    return redirect("ride_detail", ride_id=ride_id)


@login_required(login_url="/login/")
def ride_solicitation(request, ride_id):
    """
    Request to join a ride
    It is necessary to check if is it possblie to join the ride
    respecting the quantity of passengers available
    """

    ride = Ride.objects.get(uuid=ride_id)
    if ride.status != "OPEN":
        message = "Ops, a carona não está mais disponível :("
        return ride_detail(request, ride_id=ride_id, message=message)

    confirmed_passengers = Passenger.objects.filter(
        ride=ride, status=PassengerStatusChoices.ACCEPTED
    ).count()
    if confirmed_passengers == ride.quantity_of_passengers:
        message = "Ops, a carona já atingiu sua capacidade :("
        return ride_detail(request, ride_id=ride_id, message=message)

    person = get_person(request)
    Passenger.objects.create(
        ride_id=ride_id, person=person, is_driver=False, status="PENDING"
    )

    request.session["message"] = (
        "Solicitação enviada com sucesso. Aguarde a confirmação do motorista."
    )
    return redirect("ride_detail", ride_id=ride_id)


def get_person(request) -> Person:
    person = None
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        logging.error("Authenticated client is not a valid registered user.")
    return person


def mount_header(request):
    message = ""
    # if there is a message in the session, show it
    if "message" in request.session:
        message = request.session["message"]
        del request.session["message"]

    # mounting back link dynamically
    referer = request.META.get("HTTP_REFERER")
    print(referer)
    if referer != request.build_absolute_uri("/") + "rides/":
        application_url = request.build_absolute_uri("/")
        referer = application_url + "ride/my-rides"
    print(referer)
    return message, referer
