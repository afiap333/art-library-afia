from django import forms
from .models import ArtSupply

class AddArtSupplyForm(forms.ModelForm):
    class Meta:
        model = ArtSupply
        fields = ['name', 'image', 'quantity', 'pickup_location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }