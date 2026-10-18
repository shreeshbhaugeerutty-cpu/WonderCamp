from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

def _input(**extra):
    return forms.TextInput(attrs={"readonly": True, "class": "account-input", **extra})

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]
        widgets = {
            "first_name": _input(autocomplete="given-name"),
            "last_name": _input(autocomplete="family-name"),
            "email": forms.EmailInput(attrs={"readonly": True, "class": "account-input", "autocomplete": "email"}),
            "phone": _input(autocomplete="tel"),
        }