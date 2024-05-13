from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="/login/")
def home_view(request):
    return render(request, "home.html")


def public_home(request):
    return render(request, "public/home.html")
