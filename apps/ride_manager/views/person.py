from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.ride_manager.forms.form_person import PersonForm
from apps.ride_manager.models.person import Person


class PersonView(TemplateView):
    def create(request):
        if request.method == "POST":
            form = PersonForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(
                    "person_list"
                )  # Redirect to a success page or another view
            else:
                print("ERROUUU")
                print(form.errors)
        else:
            form = PersonForm()

        return render(request, "create_person.html", {"form": form})

    def list(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person"] = Person.objects.all().order_by("pk")
        return context
