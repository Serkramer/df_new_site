from django import forms
from dal import autocomplete
from custom.models import CompanyClients, PrintingCompanies, PrintingMachinePresets, ClicheTechnologies, \
    CompressionType, AngleSetTypes, AngleSets, OrderPlaneSlices, OrderFartuks, DeliveryTypes, Engravers
from map.models import Areas, Settlements, PostOffices

REVERT_CHOICES = [
    ('direct', 'Прямий'),
    ('reverse', 'Зворотній'),
]

NP_DELIVERY_TIPE_CHOICES = [
    ('post_office', 'Відділення'),
    ('addresses', 'Адресна'),
]


class OrderViewForm(forms.Form):

    engraver = forms.ModelChoiceField(label='Гравер', queryset=Engravers.objects.all(),
                                      widget=autocomplete.ModelSelect2(attrs={'class': 'form-select'}))

    urgency = forms.BooleanField(
        label='Терміновий',
        widget=forms.BooleanField()
    )

    work_file = forms.ChoiceField(
        label='Вивідний файл',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': "Default select example"}),
        choices=[('-1', '-----')],
    )

    name = forms.CharField(
        label='Назва замовлення',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    company_client = forms.ModelChoiceField(
        label='Замовник',
        queryset=CompanyClients.objects.all(),  # Загружаем все клиенты по умолчанию
        widget=forms.Select(
            attrs={
                'class': 'select2 form-select form-select-lg',  # Совпадение с вашим HTML
                'data-allow-clear': 'true',  # Разрешаем очистку выбора
                'id': 'selectCompanyClients',  # Устанавливаем идентификатор
            },
        ),
        required=True
    )

    printing_company = forms.ModelChoiceField(
        label="Друкарська компанія",
        queryset=PrintingCompanies.objects.all(),
        widget=forms.Select( #url='custom:printing-companies', forward=['company_client'],
            attrs={
                'class': 'select2 form-select form-select-lg',  # Совпадение с вашим HTML
                'data-allow-clear': 'true',  # Разрешаем очистку выбора
                'id': 'selectPrintingCompany',  # Устанавливаем идентификатор
            },
        ),
        required=True
    )

    preset = forms.ModelChoiceField(
        label="Набір налаштувань",
        queryset=PrintingMachinePresets.objects.all(),
        widget=forms.Select(#url='custom:printing-machine-presets', forward=['printing_company'],
            attrs={
                'class': 'select2 form-select form-select-lg',  # Совпадение с вашим HTML
                'data-allow-clear': 'true',  # Разрешаем очистку выбора
                'id': 'selectPrintingMachinePreset',  # Устанавливаем идентификатор
            },),
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
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    compression_value = forms.FloatField(label="Значення компресії",
                                         widget=forms.TextInput(attrs={'class': 'form-control'}))

    technology = forms.ModelChoiceField(
        label="Технологія",
        queryset=ClicheTechnologies.objects.all(),
        widget=autocomplete.ModelSelect2(url='custom:cliche-technologies', attrs={'class': 'form-select'})

    )

    angle_set = forms.ModelChoiceField(
        label="Набір кутів",
        queryset=AngleSets.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    color_library = forms.ChoiceField(
        label="бібліотека кольорів",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    raster_dot_default = forms.ChoiceField(
        label="точка",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    ruling_default = forms.ChoiceField(
        label="лініатура",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    materials_default = forms.ChoiceField(
        label="матеріал",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    height_default = forms.IntegerField(
        label="висота",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    width_default = forms.IntegerField(
        label="ширина",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class OrderDeliveryViewForm(forms.Form):
    contact = forms.ChoiceField(label="контакт з доставки", widget=forms.TextInput(attrs={'class': 'form-control'}))
    delivery_type = forms.ModelChoiceField(label="тип доставки",
                                           widget=autocomplete.ModelSelect2(attrs={'class': 'form-control'}),
                                           queryset=DeliveryTypes.objects.all(),
                                           required=True)
    delivery_date = forms.DateField()
    np_type_field = forms.ChoiceField(
        label='вид доставки',
        choices=NP_DELIVERY_TIPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
    area = forms.ModelChoiceField(
        label="Область",
        queryset=Areas.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:areas-autocomplete', attrs={'class': 'form-control'}),
        required=True
    )
    settlement = forms.ModelChoiceField(
        label='Населенний пункт',
        queryset=Settlements.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:settlements-autocomplete', forward=['area'], attrs={'class': 'form-control'}),
        required=True
    )

    post_office_ref = forms.ModelChoiceField(
        label='Відділення НП',
        queryset=PostOffices.objects.all(),
        widget=autocomplete.ModelSelect2(url='map:post-office-autocomplete', forward=['settlement_ref'], attrs={'class': 'form-control'}),
        required=False
    )

    street = forms.CharField(
        label='Вулиця',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    build = forms.CharField(
        label="будинок",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label="коментар",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class FileUploadForm(forms.ModelForm):
    pass


class PlaneSliceForm(forms.ModelForm):
    class Meta:
        model = OrderPlaneSlices
        exclude = ('order', 'name', 'lineature', 'order_plane_slice_group', 'position_x', 'position_y', 'is_defect',
                   'material_plate_type' )


class OrderFartuksForm(forms.ModelForm):
    class Meta:
        model = OrderFartuks
        exclude = ('order',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['height', 'width']
        for field in required_fields:
            self.fields[field].required = True


class OrderDamperForm(forms.ModelForm):
    pass

