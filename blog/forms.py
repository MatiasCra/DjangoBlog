from tkinter import Widget
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "image", "content", "tags", "category", "user")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "subtitle": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "user": forms.HiddenInput(),
        }
