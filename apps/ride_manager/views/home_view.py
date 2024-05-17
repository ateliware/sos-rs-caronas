from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from apps.ride_manager.models import Ride
from apps.ride_manager.enums import PassengerStatusChoices


class HomeView(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Ride

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user has some ride as driver with passengers waiting for approval.
        rides = Ride.objects.filter(driver__user=self.request.user).annotate(
            pending_passengers_count=Count(
                "passenger",
                filter=Q(passenger__status=PassengerStatusChoices.PENDING),
            )
        )
        # check if in some ride the user is the driver and there are passengers waiting for approval
        need_evaluation = any(ride.pending_passengers_count > 0 for ride in rides)
        context["need_evaluation"] = need_evaluation
        return context