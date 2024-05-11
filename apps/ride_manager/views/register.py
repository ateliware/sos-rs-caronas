from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.ride_manager.forms.form_person import PersonForm
from apps.ride_manager.models.person import Person


class PersonView(TemplateView):
    def register(request):
        if request.method == "POST":
            form = PersonForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(
                    "login"
                )
            else:
                print(form.errors)
        else:
            form = PersonForm()

        return render(request, "register.html", {"form": form})

    def list(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person"] = Person.objects.all().order_by("pk")
        return context
