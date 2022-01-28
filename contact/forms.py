from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control mb-2 mt-1"}),
            "subject": forms.TextInput(attrs={"class": "form-control mb-2 mt-1"}),
            "message": forms.Textarea(
                attrs={"class": "form-control mb-2 mt-1", "rows": "8"}
            ),
        }
