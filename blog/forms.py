from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "subtitle", "image", "content", "category", "user", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "subtitle": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(
                attrs={"class": "form-select", "id": "tagsSelect"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "user": forms.HiddenInput(),
            "tags": forms.HiddenInput(),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }