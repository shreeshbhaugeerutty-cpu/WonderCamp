from django import forms

class PaymentForm(forms.Form):
    method = forms.CharField(widget=forms.HiddenInput(), initial='mcb_juice')
    mobile = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    country = forms.ChoiceField(choices=[
        ('Mauritius', 'Mauritius'),
        ('Réunion', 'Réunion'),
        ('France', 'France'),
        ('United Kingdom', 'United Kingdom'),
        ('Other', 'Other')
    ])