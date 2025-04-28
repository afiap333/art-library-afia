from django import forms
from django.core.exceptions import ValidationError
from .models import ArtSupply,Collection,ArtSupplyRequest,Reviews
from .models import CustomUser
from django.core.validators import MinValueValidator

class AddArtSupplyForm(forms.ModelForm):
    class Meta:
        model = ArtSupply
        fields = ['name', 'image', 'quantity', 'pickup_location','description','use_policy','item_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'use_policy':forms.TextInput(attrs={'class':'form-control'}),
            'item_type':forms.Select(attrs={'class':'form-control'}),
        }

class DeleteArtSupplyGorm(forms.Form):
    #simple confirmation form for deleting an art supply item.
    confirm = forms.BooleanField(
        required=True,
        label="Are you sure you want to delete this item?"
    )

class AddCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'is_public', 'users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_public_checkbox'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'display:none;'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user and user.user_role == 'patron':
            self.fields['is_public'].widget = forms.HiddenInput()
            self.fields['users'].widget = forms.HiddenInput()
            del self.fields['is_public']
            del self.fields['users']
        else:
            self.fields['users'] = forms.ModelMultipleChoiceField(
                queryset=CustomUser.objects.all(),
                required=False,
                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
            )
    
 
class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ['profile_pic']

class BorrowForm(forms.ModelForm):
    class Meta:
        model = ArtSupplyRequest
        fields = ['lending_period']
        widgets = {
            'lending_period': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts= {
            'lending_period':"Enter how long you would like to borrow the item for.",
        }
    def clean_lending_period(self):
        lending_period=self.cleaned_data.get('lending_period')
        if lending_period!='':
            try:
                lending_period = int(lending_period)
            except(ValueError, TypeError):
                raise forms.ValidationError("Must be a number")
            if lending_period<=0:
                raise forms.ValidationError("Lending period must be greater than 0.")
        return lending_period

class ReviewForm(forms.ModelForm):
    ratings = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = forms.ChoiceField(
        choices=ratings,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model=Reviews
        fields=['rating','comment']
        widgets={
            'comment':forms.TextInput(attrs={'class':'form-control'}),
        }