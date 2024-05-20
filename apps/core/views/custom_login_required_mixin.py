from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse
from django.http import HttpResponseRedirect


class CustomLoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse("login") + "?next=" + request.path
            )
        return super().dispatch(request, *args, **kwargs)
