from django import forms
from django_select2.forms import Select2MultipleWidget

from store.models import Materials


class MaterialChartsForm(forms.Form):
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
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material_thickness',
                                            })
    )

    materials = forms.ModelMultipleChoiceField(
        queryset=Materials.objects.using('store').all(),
        label="Матеріали",
        required=False,
        widget=Select2MultipleWidget(attrs={'class': 'select2 form-select', 'id': 'select_material',})
    )

    def clean(self):
        cleaned_data = super().clean()



        return cleaned_data
