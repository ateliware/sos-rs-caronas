from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from apps.ride_manager.models.passenger import (
    StatusChoices as PassengerStatusChoices,
)
from apps.ride_manager.models.ride import Ride


@login_required(login_url="/login/")
def home_view(request):
    """
    Check if the user has some ride as driver with passengers waiting for approval.
    """
    rides = Ride.objects.filter(driver__user=request.user).annotate(
        pending_passengers_count=Count(
            "passenger",
            filter=Q(passenger__status=PassengerStatusChoices.PENDING),
        )
    )
    # check if in some ride the user is the driver and there are passengers waiting for approval
    need_evaluation = any(ride.pending_passengers_count > 0 for ride in rides)
    return render(request, "home.html", {"need_evaluation": need_evaluation})


def public_home(request):
    return render(request, "public/home.html")
