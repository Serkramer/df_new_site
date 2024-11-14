
from django import forms

from auth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'company', 'position', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'firstName', 'autofocus': 'autofocus'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'lastName'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'john.doe@example.com'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'id': 'organization'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'id': 'position'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'phoneNumber', 'placeholder': '+380'}),
        }
