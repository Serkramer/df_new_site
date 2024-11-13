from django import forms
from dal import autocomplete
from custom.models import CompanyClients, PrintingCompanies, PrintingMachinePresets, ClicheTechnologies, \
    CompressionType, AngleSetTypes, AngleSets
from map.models import Areas, Settlements, PostOffices

REVERT_CHOICES = [
    ('direct', 'Прямий'),
    ('reverse', 'Зворотній'),
]


class OrderViewForm(forms.Form):
    work_file = forms.ChoiceField(
        label='Вивідний файл',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'aria-label': "Default select example"})
    )

    name = forms.CharField(
        label='Назва замовлення',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    company_client = forms.ModelChoiceField(
        label='Замовник',
        queryset=CompanyClients.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:company-clients',
                                         attrs={'class': 'form-control', 'aria-label': "Default select example"}, ),
        required=True
    )

    printing_company = forms.ModelChoiceField(
        label="Друкарська компанія",
        queryset=PrintingCompanies.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:printing-companies', forward=['company_client'],
                                         attrs={'class': 'form-control'}),
        required=True
    )

    preset = forms.ModelChoiceField(
        label="Набір налаштувань",
        queryset=PrintingMachinePresets.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:printing-machine-presets', forward=['printing_company'],
                                         attrs={'class': 'form-control'}),
        required=False

    )

    revert_print = forms.ChoiceField(
        label='Друк',
        choices=REVERT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )

    compression = forms.ChoiceField(
        label="Компресія",
        choices=CompressionType.choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    compression_value = forms.FloatField(label="Значення компресії",
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    technology = forms.ModelChoiceField(
        label="Технологія",
        queryset=ClicheTechnologies.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:cliche-technologies', attrs={'class': 'form-control'})
    )

    angle_set = forms.ModelChoiceField(
        label="Набір кутів",
        queryset=AngleSets.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    color_library = forms.ChoiceField(
        label="бібліотека кольорів",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    raster_dot_default = forms.ChoiceField(
        label="точка",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    ruling_default = forms.ChoiceField(
        label="лініатура",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    materials_default = forms.ChoiceField(
        label="матеріал",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    height_default = forms.IntegerField(
        label="висота",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    width_default = forms.IntegerField(
        label="ширина",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class OrderPlaneSliceViewForm(forms.Form):
    color_output = forms.BooleanField()
    color_div = forms.CharField()
    angel = forms.CharField()
    dot = forms.CharField()
    material = forms.CharField()
    page_number = forms.IntegerField()
    width = forms.IntegerField()
    height = forms.IntegerField()
    quantity = forms.IntegerField()


class OrderDeliveryViewForm(forms.Form):
    contact = forms.CharField()
    delivery_type = forms.CharField()
    delivery_date = forms.DateField()
    np_type_field = forms.RadioSelect()
    area = forms.ModelChoiceField(
        label="Область",
        queryset=Areas.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:areas-autocomplete'),
        required=True
    )
    settlement = forms.ModelChoiceField(
        label='Населенний пункт',
        queryset=Settlements.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:settlements-autocomplete', forward=['area']),
        required=True
    )

    post_office_ref = forms.ModelChoiceField(
        label='Відділення НП',
        queryset=PostOffices.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:post-office-autocomplete', forward=['settlement_ref']),
        required=False
    )


class FileUploadForm(forms.ModelForm):
    pass
