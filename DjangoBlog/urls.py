"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect, render

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", lambda req: redirect("Home")),
    path(
        "about/", lambda req: render(req, "about.html", {"page": "About"}), name="About"
    ),
    path(
        "terms_of_use/",
        lambda req: render(req, "lorem.html", {"page": "Terms of Use"}),
        name="Terms",
    ),
    path(
        "privacy_policy/",
        lambda req: render(req, "lorem.html", {"page": "Privacy Policy"}),
        name="PrivacyPolicy",
    ),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
