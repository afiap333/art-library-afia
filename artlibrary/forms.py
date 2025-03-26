from django import forms
from .models import ArtSupply,Collection, Keyword
from .models import CustomUser


class AddArtSupplyForm(forms.ModelForm):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.all(), 
        empty_label="Select a Collection", 
        required=False
    )
    keywords=forms.CharField(
        required=False,
        help_text="Enter keywords seperated by commas",
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
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
    def save(self,commit=True):
        artSupply=super().save(commit=False)
        if commit:
            artSupply.save()
            self.saveKeywords(artSupply)
    def  saveKeywords(self, artSupply):
        keywords=self.cleaned_data.get('keywords','')
        if keywords:
            keywordsList=[word.strip() for word in keywords.split(',') if word.strip()]
            for word in keywordsList:
                Keyword.objects.create(art_supply=ArtSupply,word=word)
class AddCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title','description','is_public']
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def __init__(self,*args,user=None,**kwargs):
        super().__init__(*args,**kwargs)
        if user and user.user_role!='librarian':
             self.fields.pop('is_public',None)
class EditCollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    delete_collection = forms.BooleanField(required=False, label="Delete Collection")
 
class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    user_role = forms.ChoiceField(choices=CustomUser.roles, required=True)
    class Meta:
        model = CustomUser
        fields = ['profile_pic','user_role']
