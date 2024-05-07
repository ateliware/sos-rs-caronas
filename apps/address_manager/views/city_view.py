from django.views.generic import TemplateView

from apps.address_manager.models import City


class CityView(TemplateView):
    template_name = "list_cities.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all().order_by("pk")
        return context
