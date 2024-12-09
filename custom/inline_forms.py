from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from custom.models import PrintingMachines, ContactsDetails, ContactTypes, ContactTypeChoices, CompaniesContacts

from django_select2.forms import Select2MultipleWidget  # Импорт виджета Select2


class PrintingMachinesInlineForm(forms.ModelForm):
    class Meta:
        model = PrintingMachines
        exclude = ('material_thickness',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Указываем обязательные поля
        required_fields = ['name']  # Замените на нужные поля
        for field in required_fields:
            self.fields[field].required = True


class ContactsDetailsInlineForm(forms.ModelForm):
    class Meta:
        model = ContactsDetails
        fields = '__all__'

    # Поле types с виджетом Select2
    types = forms.MultipleChoiceField(
        choices=ContactTypeChoices.choices,  # Доступные значения типа
        required=False,
        widget=Select2MultipleWidget,  # Виджет для отображения Select2
        label='Типи контактів'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если объект уже существует, получаем связанные типы контактов
        if self.instance.pk:
            selected_types = self.instance.contacttypes_set.values_list('type', flat=True)
            selected_types_list = list(selected_types)
            self.fields['types'].initial = selected_types_list

    def save(self, commit=True):
        # Получаем данные из формы
        contact = self.cleaned_data['contact']
        value = self.cleaned_data['value']
        selected_types = set(self.cleaned_data.get('types', []))  # Типы из формы

        # Ищем существующий объект с такими же contact и value
        existing_instance = ContactsDetails.objects.filter(contact=contact, value=value).first()

        if existing_instance:
            # Проверяем, совпадают ли типы
            existing_types = set(existing_instance.contacttypes_set.values_list('type', flat=True))
            if existing_types == selected_types:
                # Если объект и типы совпадают, ничего не делаем
                return None
            else:
                # Если объект существует, но типы отличаются, обновляем их
                for contact_type in (existing_types - selected_types):
                    existing_instance.contacttypes_set.filter(type=contact_type).delete()
                for contact_type in (selected_types - existing_types):
                    # Добавляем только отсутствующие связи
                    ContactTypes.objects.create(
                        contacts_detail=existing_instance,
                        type=contact_type
                    )
                return existing_instance

        # Если объекта с такими contact и value нет, создаём новый
        instance = super().save(commit=False)

        if commit:
            # Сохраняем объект в базу данных
            instance.save()

            # Добавляем выбранные типы
            for contact_type in selected_types:
                ContactTypes.objects.create(
                    contacts_detail=instance,
                    type=contact_type
                )

        return instance


class CompaniesContactsInlineForm(forms.ModelForm):
    class Meta:
        model = CompaniesContacts
        fields = '__all__'






