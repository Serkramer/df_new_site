from django import forms
from dal import autocomplete
from pydantic import ValidationError

from custom.models import PrintingMachineShafts, Companies, DeliveryPresets, Addresses, PrintingMachinePresets, \
    AdhesiveTapeThicknesses, FartukHeights, PrintingMachines
from map.models import Areas, PostOffices, Settlements


class PrintingMachinesForm(forms.ModelForm):
    class Meta:
        model = PrintingMachines
        exclude = ('material_thickness',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['printing_company', 'name']
        for field in required_fields:
            self.fields[field].required = True


class PrintingMachinePresetsForm(forms.ModelForm):
    class Meta:
        model = PrintingMachinePresets
        fields = ('printing_machine', 'name', 'ruling', 'angle_set', 'raster_dot', 'material_thickness',
                  'cliche_technology', 'is_revert_printing', 'color_profile', 'plate_curve_strategy',
                  'press_curve_strategy', 'damper', 'description', 'adhesive_tape_thickness_multiplier',
                  'adhesive_tape_thickness', 'fartuk', 'material')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['printing_machine', 'name', 'ruling', 'angle_set', 'raster_dot', 'material_thickness',
                           'cliche_technology', 'is_revert_printing', 'adhesive_tape_thickness']
        for field in required_fields:
            self.fields[field].required = True

    def clean_thickness(self):
        name = self.cleaned_data.get('name')

        # Проверка на уникальность
        if PrintingMachinePresets.objects.filter(name=name).exists():
            self.add_error('name', "Це поле повинно бути унікальним.")

        return name


class AdhesiveTapeThicknessesForm(forms.ModelForm):
    class Meta:
        model = AdhesiveTapeThicknesses
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['thickness'].required = True

    def clean_thickness(self):
        thickness = self.cleaned_data.get('thickness')

        # Проверка на уникальность
        if AdhesiveTapeThicknesses.objects.filter(thickness=thickness).exists():
            self.add_error('thickness', "Це поле повинно бути унікальним. введіть значення, якого ще немає")

        return thickness


class PrintingMachineShaftsForm(forms.ModelForm):

    class Meta:
        model = PrintingMachineShafts
        fields = ('printing_machine', 'input_value', 'input_value_type', 'quantity', 'width', 'printing_width',
                  'description', 'contact', 'date_create')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Указываем обязательные поля
        required_fields = ['printing_machine', 'input_value', 'input_value_type']
        for field in required_fields:
            self.fields[field].required = True


class FartukHeightsForm(forms.ModelForm):
    class Meta:
        model = FartukHeights
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Указываем обязательные поля
        required_fields = ['full_name', 'name',]
        for field in required_fields:
            self.fields[field].required = True

            # Фильтрация queryset для поля delivery_preset
            if self.instance and self.instance.pk:
                self.fields['delivery_preset'].queryset = DeliveryPresets.objects.filter(company=self.instance)
            else:
                self.fields['delivery_preset'].queryset = DeliveryPresets.objects.none()


class AddressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ('settlement_ref', 'post_office_ref', 'street', 'number')


class DeliveryPresetsForm(forms.ModelForm):
    street = forms.CharField(label='Вулиця', required=False)
    build = forms.CharField(label='Номер будинку', required=False)
    post_office_ref = forms.ModelChoiceField(
        label='Відділення НП',
        queryset=PostOffices.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:post-office-autocomplete', forward=['settlement_ref']),
        required=False
    )
    area = forms.ModelChoiceField(
        label='Область',
        queryset=Areas.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:areas-autocomplete'),
        required=True
    )
    settlement_ref = forms.ModelChoiceField(
        label='Населенний пункт',
        queryset=Settlements.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='map:settlements-autocomplete',
            forward=['area']
        ),
        required=True
    )

    class Meta:
        model = DeliveryPresets
        fields = ('company', 'name', 'delivery_type', 'area', 'settlement_ref', 'post_office_ref',
                  'street', 'build', 'description',  'contact', 'is_legal_address')

    class Media:
        #TODO
        js = ('admin/js/forms/delivery_preset_form.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['company', 'delivery_type',]
        for field in required_fields:
            self.fields[field].required = True

        if self.instance.pk and self.instance.address:
            # Заполнение полей адреса, если адрес существует
            address = self.instance.address
            if address:
                self.fields['street'].initial = address.street

                settlement = Settlements.objects.get(ref=address.settlement_ref)
                area = settlement.area_ref

                self.fields['area'].initial = area
                self.fields['build'].initial = address.build
                self.fields['post_office_ref'].initial = address.post_office_ref
                self.fields['settlement_ref'].initial = address.settlement_ref

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # Сохранение адреса
            address_data = {
                'street': self.cleaned_data['street'],
                'build': self.cleaned_data['build'],
                'post_office_ref': self.cleaned_data['post_office_ref'],
                'settlement_ref': self.cleaned_data['settlement_ref'],
            }
            address, created = Addresses.objects.update_or_create(
                id=instance.address_id, defaults=address_data
            )
            instance.address = address
            instance.save()
        return instance
