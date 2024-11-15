
from django import forms

from auth.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'company', 'position', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'firstName', 'placeholder': 'Ім`я'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'lastName', 'placeholder': 'Прізвище'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'id': 'organization', 'placeholder': 'Компанія'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'id': 'position', 'placeholder': 'Посада'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'phoneNumber', 'placeholder': '+380'}),
        }
        labels = {
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
            'company': 'Компанія',
            'position': 'Посада',
            'phone_number': 'Номер телефону',
        }
