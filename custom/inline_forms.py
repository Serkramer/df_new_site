from django import forms
from django.forms import ModelForm

from custom.models import PrintingMachines, ContactsDetails, ContactTypes, ContactTypeChoices


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

    types = forms.MultipleChoiceField(
        choices=ContactTypeChoices.choices,  # Передаем доступные значения типа из ContactTypeChoices
        required=False,
        widget=forms.CheckboxSelectMultiple,  # Виджет для отображения чекбоксов
        label='Типи контактів'
    )

    def __init__(self, *args, **kwargs):
        # Инициализируем форму
        super().__init__(*args, **kwargs)

        # Получаем связанный объект, если он уже существует
        if self.instance.pk:
            # Получаем связанные типы контактов для текущего объекта ContactsDetails
            selected_types = self.instance.contacttypes_set.values_list('type', flat=True)
            # Преобразуем QuerySet в список
            selected_types_list = list(selected_types)

            # Добавим отладочный вывод для проверки значений
            print(f"selected_types_list: {selected_types_list}")

            # Устанавливаем выбранные типы в поле 'types'
            self.fields['types'].initial = selected_types_list

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Сохраняем выбранные типы
        if commit:
            instance.save()  # Сначала сохраняем контакт
            # Теперь создаем связи с типами контактов
            # Получаем все текущие связи с типами
            existing_types = set(self.instance.contacttypes_set.values_list('type', flat=True))

            # Получаем выбранные типы из формы
            selected_types = set(self.cleaned_data['types'])

            # Удаляем связи для тех типов, которые не были выбраны
            types_to_delete = existing_types - selected_types
            for contact_type in types_to_delete:
                self.instance.contacttypes_set.filter(type=contact_type).delete()

            # Добавляем новые связи
            types_to_add = selected_types - existing_types
            for contact_type in types_to_add:
                ContactTypes.objects.create(
                    contacts_detail=instance,
                    type=contact_type
                )

        return instance


