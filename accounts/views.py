from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from accounts.models import Profile
from .forms import LoginForm, SignupForm, ProfileForm


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


class ProfileView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.request.user.id == context["profile"].user.id:
            context["page"] = "My profile"
        else:
            context["page"] = str(context["profile"])
        return context


def update_profile(request, user_id):
    profile = Profile.objects.get(user=user_id)
    user = User.objects.get(id=user_id)
    if request.method == "GET":
        data = profile.__dict__
        data.update(email=user.email, username=user.username)
        data["avatar"] = profile.avatar
        form = ProfileForm(initial=data)
        return render(
            request, "accounts/profile_form.html", {"form": form, "user_id": user_id}
        )
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            avatar = request.FILES.get("avatar")
            bio = request.POST.get("bio")
            user.username = username
            user.email = email
            user.save()
            profile.set_avatar(avatar)
            profile.bio = bio
            profile.save()
            return redirect("Profile", profile.id)
