from django import forms
from .models import ArtSupply
from .models import CustomUser


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

class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)  # ✅ Ensures only valid images
    user_role = forms.ChoiceField(choices=CustomUser.roles, required=True)
    class Meta:
        model = CustomUser
        fields = ['profile_pic','user_role']
