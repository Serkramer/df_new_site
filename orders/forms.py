from django import forms
from dal import autocomplete
from custom.models import CompanyClients, PrintingCompanies, PrintingMachinePresets, ClicheTechnologies
from map.models import Areas, Settlements, PostOffices


class OrderViewForm(forms.Form):

    work_file = forms.ChoiceField(
        label='Вивідний файл',
        required=True
    )

    name = forms.CharField(
        label='Назва замовлення'
    )

    company_client = forms.ModelChoiceField(
        label='Замовник',
        queryset=CompanyClients.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:company-clients'),
        required=True
    )

    printing_company = forms.ModelChoiceField(
        label="Друкарська компанія",
        queryset=PrintingCompanies.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:printing-companies', forward=['company_client']),
        required=True
    )

    preset = forms.ModelChoiceField(
        label="Набір налаштувань",
        queryset=PrintingMachinePresets.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:printing-machine-presets', forward=['printing_company']),
        required=False

    )

    revert_print = forms.RadioSelect(
    )

    compression = forms.ChoiceField()

    compression_value = forms.FloatField()

    technology = forms.ModelChoiceField(
        label="Технологія",
        queryset=ClicheTechnologies.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:ClicheTechnologiesAutocomplete')
    )

    angle_set = forms.ChoiceField()

    color_library = forms.ChoiceField()

    raster_dot_default = forms.ChoiceField()

    ruling_default = forms.ChoiceField()

    materials_default = forms.ChoiceField()

    height_default = forms.IntegerField()
    width_default = forms.IntegerField()


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
