from django.db.models import Count, Q
from django.views.generic import ListView

from apps.core.views import CustomLoginRequiredMixin
from apps.ride_manager.enums import PassengerStatusChoices
from apps.ride_manager.models import Ride


class HomeView(CustomLoginRequiredMixin, ListView):
    template_name = "home.html"
    model = Ride

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        show_caution_modal = self.request.session.get(
            "show_caution_modal", False
        )
        if show_caution_modal:
            # Remove the session variable after it's used
            self.request.session["show_caution_modal"] = False

        # Check if the user has some ride as driver with passengers waiting for approval.
        rides = Ride.objects.filter(driver__user=self.request.user).annotate(
            pending_passengers_count=Count(
                "passenger",
                filter=Q(passenger__status=PassengerStatusChoices.PENDING),
            )
        )
        # check if in some ride the user is the driver and there are passengers waiting for approval
        need_evaluation = any(
            ride.pending_passengers_count > 0 for ride in rides
        )
        context["need_evaluation"] = need_evaluation
        context["show_caution_modal"] = show_caution_modal
        return context
