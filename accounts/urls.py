from unicodedata import name
from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.log_in, name="Login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="Home"),
        name="Logout",
    ),
    path("signup/", views.sign_up, name="Signup"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="Profile"),
    path("profile/edit/<int:user_id>", views.update_profile, name="EditProfile"),
]
