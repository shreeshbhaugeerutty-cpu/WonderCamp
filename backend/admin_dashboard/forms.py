from django import forms
from django.contrib.auth import get_user_model

# Try importing from 'vehicles' first, or fallback if path differs
try:
    from backend.vehicles.models import RV
except ImportError:
    try:
        from vehicles.models import RV
    except ImportError:
        from backend.rvs.models import RV

try:
    from backend.campsites.models import Campsite
except ImportError:
    from campsites.models import Campsite

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


class RVForm(forms.ModelForm):
    class Meta:
        model = RV
        fields = ['title', 'subtitle', 'price', 'capacity', 'amenities', 'image', 'fallback_image', 'overall_rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'RV Model Title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. High luxury RV'}),
            'price': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Rs 9,990'}),
            'capacity': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 6 - 7 persons'}),
            'amenities': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'WiFi, Kitchen, AC'}),
            'fallback_image': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Image URL'}),
            'overall_rating': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.1', 'min': '1.0', 'max': '5.0'}),
        }