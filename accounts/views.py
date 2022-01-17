from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# from .models import Profile
from .forms import LoginForm, SignupForm


def log_in(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form, "page": "Log in"})
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user_by_username = authenticate(username=username, password=password)
            if user_by_username is not None:
                login(request, user_by_username)
                return redirect("Home")

            try:
                username = User.objects.get(email=username)
            except ObjectDoesNotExist:
                username = None

            user_by_mail = authenticate(username=username, password=password)
            if user_by_mail is not None:
                login(request, user_by_mail)
                return redirect("Home")

        return render(
            request,
            "accounts/login.html",
            {"form": form, "page": "Log in"},
        )


def sign_up(request):
    if request.method == "GET":
        form = SignupForm()
        return render(
            request, "accounts/signup.html", {"form": form, "page": "Sign up"}
        )
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Home")

        return render(
            request,
            "accounts/signup.html",
            {"form": form, "page": "Sign up"},
        )
