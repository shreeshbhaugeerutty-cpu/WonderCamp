from django import forms
from django.contrib.auth import get_user_model
from backend.campsites.models import Campsite # Adjust this import path if your campsite app has a different folder name

User = get_user_model()


class AdminProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CampsiteForm(forms.ModelForm):
    class Meta:
        model = Campsite
        fields = ['name', 'location', 'description', 'price_per_night', 'capacity', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Campsite Name'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Description...'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Max Guests'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }