from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, 'database/index.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirecto to a success page.
            return HttpResponseRedirect(reverse("index"))
        else:
            # return an 'invalid login' error message
            return render(request, "database/login.html", {
                "message": "Invalid username and/or password. "
            })
    else:
        return render(request, "database/login.html")

def logout_view(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "database/register.html", {
                "message":"Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "database/register.html", {
                "message":"Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "database/register.html")
