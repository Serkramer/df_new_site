from django import forms

from custom.models import PrintingMachines


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
