from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "img_url", "category"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'img_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }