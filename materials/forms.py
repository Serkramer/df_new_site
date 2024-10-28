from django import forms
from django_select2.forms import Select2MultipleWidget

from store.models import Materials

MATERIAL_TYPE_FROM_CHARTS_CHOICES = [
    ('material', 'матеріалом'),
    ('material_thickness', 'товщіною матеріалу'),
]


class MaterialChartsForm(forms.Form):
    material_type = forms.ChoiceField(
        choices=MATERIAL_TYPE_FROM_CHARTS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check form-check-inline mt-4'}),
        label='Дізнатися за:',
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%d.%m.%Y'),
        required=True,
        label='Початкова дата',

    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Кінцева дата'

    )

    thickness = forms.MultipleChoiceField(
        choices=[(thickness, thickness) for thickness in
                 Materials.objects.using('store').values_list('thickness', flat=True).distinct()],
        label="Товщіни",
        required=False,
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material_thickness'})
    )

    materials = forms.ModelMultipleChoiceField(
        queryset=Materials.objects.using('store').all(),
        label="Матеріали",
        required=False,
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material'})
    )

    def clean(self):
        cleaned_data = super().clean()

        material_type = cleaned_data.get('material_type')

        if not material_type:
            raise forms.ValidationError('Необхідно обрати тип вибірки матеріалу')

        return cleaned_data
