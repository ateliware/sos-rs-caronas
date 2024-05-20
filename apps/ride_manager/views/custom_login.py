from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from apps.ride_manager.forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomLoginForm

    def get_success_url(self):
        self.request.session["show_caution_modal"] = True
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse_lazy("home")
