
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

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


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Поточний пароль'}),
        label="Поточний пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новий пароль'}),
        label="Новий пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть новий пароль'}),
        label="Повторіть новий пароль"
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user

        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError("Неправильний поточний пароль!")
        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 != new_password2:
            raise forms.ValidationError("Паролі не співпадають!")
        if len(new_password1) < 8:
            raise forms.ValidationError("Пароль має містити мінімум 8 символів!")
        return new_password2
