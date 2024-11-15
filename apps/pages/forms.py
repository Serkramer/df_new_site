
from django import forms

from auth.models import Profile
import re

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'company', 'position', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Прізвище'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Компанія'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Посада'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380', 'type': 'tel', 'maxlength': 13}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        # Разрешаем только цифры и знак '+'
        if not re.match(r'^\+?\d+$', phone_number):
            raise forms.ValidationError("Номер телефону может содержать только цифры и символ '+'.")

        return phone_number
