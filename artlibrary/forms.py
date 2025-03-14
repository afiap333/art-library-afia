from django import forms
from .models import ArtSupply,Collection

class AddArtSupplyForm(forms.ModelForm):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.all(), 
        empty_label="Select a Collection", 
        required=False
    )
    class Meta:
        model = ArtSupply
        fields = ['name', 'image', 'quantity', 'pickup_location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
class AddCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title','description','is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

