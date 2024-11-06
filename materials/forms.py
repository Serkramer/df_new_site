from django import forms
from django_select2.forms import Select2MultipleWidget
from datetime import date, timedelta
from store.models import Materials
from dateutil.relativedelta import relativedelta


class MaterialChartsForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        required=True,
        input_formats=['%Y-%m-%d'],
        label='Початкова дата',

    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        required=True,
        input_formats=['%Y-%m-%d'],
        label='Кінцева дата'

    )

    thickness = forms.MultipleChoiceField(
        choices=[(thickness, thickness) for thickness in
                 Materials.objects.using('store')
                 .exclude(thickness__isnull=True)
                 .values_list('thickness', flat=True).distinct()],
        label="Товщіни",
        required=False,
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material_thickness'})
    )

    materials = forms.ModelMultipleChoiceField(
        queryset=Materials.objects.using('store').all(),
        label="Матеріали",
        required=False,
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material',})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('Кінцева дата повинна бути пізніше початкової дати')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Устанавливаем начальную дату — первый день месяца год назад

        one_year_ago = (date.today() - relativedelta(years=1)).replace(day=1)
        self.fields['start_date'].initial = one_year_ago

        self.fields['end_date'].initial = date.today()

    def get_materials_data(self):
        return [
            {'id': material.id, 'name': material.name, 'thickness': material.thickness}
            for material in self.fields['materials'].queryset
        ]

