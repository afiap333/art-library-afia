from django import forms
from django.core.exceptions import ValidationError
from .models import ArtSupply,Collection
from .models import CustomUser

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
<<<<<<< HEAD
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

=======
        fields = ['title', 'description', 'is_public','items']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'items':forms.CheckboxSelectMultiple(attrs={'class':'form-control'}),
        }
    def __init__(self,*args,user=None,**kwargs):
        super().__init__(*args,**kwargs)
        if user and user.user_role!='librarian':
             self.fields.pop('is_public',None)
    
 
>>>>>>> development
class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    user_role = forms.ChoiceField(choices=CustomUser.roles, required=True)
    class Meta:
        model = CustomUser
        fields = ['profile_pic','user_role']
