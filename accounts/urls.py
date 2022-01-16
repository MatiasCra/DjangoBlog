from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", views.log_in, name="Login"),
    path(
        "logout/",
        LogoutView.as_view(template_name="blog/index.html"),
        name="Logout",
    ),
    path('signup/', views.sign_up, name='Signup'),
]
