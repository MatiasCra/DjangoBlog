from cProfile import label
import imp
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=200,
        label="User",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        max_length=200, widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
