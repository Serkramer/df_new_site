from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget
from dal import autocomplete
from custom.models import CompanyClients
from .models import Price, Materials, Companies, CompanyWithNuances, PriceType


class PriceForm(forms.ModelForm):
    # Поле для выбора компании (без отображения ID)
    company = forms.ModelChoiceField(
        queryset=CompanyClients.objects.using('custom').all(),
        label="Компанія",
        widget=autocomplete.ModelSelect2(url='custom:company-clients'),
        required=True
    )

    # Поле для выбора материалов
    materials = forms.ModelMultipleChoiceField(  # Изменено на ModelMultipleChoiceField
        queryset=Materials.objects.using('store').all(),
        label="Матеріали",
        required=False,
        widget=autocomplete.ModelSelect2Multiple(  # Применяем виджет для множественного выбора
            url='store:materials',
            forward=['thickness']  # Передаем значение поля thickness
        )
    )


    thickness = forms.MultipleChoiceField(
        choices=[(thickness, thickness) for thickness in
                 Materials.objects.using('store').values_list('thickness', flat=True).distinct()],
        label="Товщіни",
        required=False,
        widget=Select2MultipleWidget  # Применяем виджет Select2
    )

    class Meta:
        model = Price
        fields = ['company', 'price', 'price_type', 'thickness', 'materials', ]

    class Media:
        js = ('admin/js/price_form.js',)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Сохраняем ID компании, не показывая поле company_id в форме
        instance.company_id = self.cleaned_data['company'].id.id
        if instance.price_type != PriceType.PRICE_MATERIAL:
            instance.thickness_list = []
            instance.material_ids = []
        else:
            # Сохраняем ID материалов (только если materials не пустое)
            materials = self.cleaned_data.get('materials')
            instance.material_ids = [material.id for material in materials] if materials else []

            # Сохраняем список толщин (только если thickness не пустое)
            thickness = self.cleaned_data.get('thickness')
            instance.thickness_list = [f"{float(t):.3f}" for t in thickness] if thickness else []

        if commit:
            instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # Установите начальные данные для поля materials
            self.fields['materials'].initial = Materials.objects.using('store').filter(
                id__in=self.instance.material_ids
            )

            if isinstance(self.instance.thickness_list, list):
                print("Инициализация толщин:", self.instance.thickness_list)  # Отладочный вывод

                # Сохраняем все доступные толщины в choices
                all_thicknesses = Materials.objects.using('store').values_list('thickness', flat=True).distinct()
                thickness_choices = [(str(thickness), str(thickness)) for thickness in all_thicknesses]
                self.fields['thickness'].choices = thickness_choices

                # Устанавливаем начальные данные для поля thickness
                # Убедитесь, что передаете список строковых значений толщин
                self.fields['thickness'].initial = [str(thickness) for thickness in self.instance.thickness_list]

            # Установите начальное значение для поля company
            self.initial['company'] = Companies.objects.using('custom').get(id=self.instance.company_id)


class CompanyWithNuancesForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Companies.objects.using('custom').all(),
        label="Компанія"
    )

    class Meta:
        model = CompanyWithNuances
        fields = ['company', 'check_with_cents', 'name_order_in_check', 'group_orders', 'text_before',
                  'unique_order_name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['company'] = Companies.objects.using('custom').get(id=self.instance.company_id)

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')

        # Проверка на существование записи с таким же company_id
        if company and CompanyWithNuances.objects.filter(company_id=company.id).exclude(pk=self.instance.pk).exists():
            self.add_error('company', ValidationError('Запис для цієї компанії вже існує.'))

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.company_id = self.cleaned_data['company'].id

        if commit:
            instance.save()

        return instance
