from django import forms

from .models import RVComment


class RVCommentForm(forms.ModelForm):
    class Meta:
        model = RVComment
        fields = ["name", "rating", "text"]
        labels = {
            "name": "Your name",
            "rating": "Your rating",
            "text": "Your review",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Sarah Jenkins"}),
            "text": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What did you love about this camping van?",
            }),
        }