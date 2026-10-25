from django import forms
 
from .models import Comment
 
 
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "rating", "text"]
        labels = {
            "name": "Your name",
            "rating": "Your rating",
            "text": "Your review",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Isla Devion"}),
            "text": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What did you love about this campsite?",
            }),
        }