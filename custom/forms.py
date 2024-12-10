from django import forms
from dal import autocomplete
from pydantic import ValidationError

from custom.models import PrintingMachineShafts, Companies, DeliveryPresets, Addresses, PrintingMachinePresets, \
    AdhesiveTapeThicknesses, FartukHeights, PrintingMachines, Fartuks, FartukRailTypes, FartukMembraneTypes, \
    AniloxRolls, ContactsDetails, Contacts, ContactTypeChoices, CompaniesContacts
from map.models import Areas, PostOffices, Settlements


class AniloxRollForm(forms.ModelForm):
    class Meta:
        model = AniloxRolls
        fields = ('printing_machine', 'line_count', 'transfer_volume', 'type', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['printing_machine', 'line_count']
        for field in required_fields:
            self.fields[field].required = True


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


class FartukRailTypesForm(forms.ModelForm):
    class Meta:
        model = FartukRailTypes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True

    def clean_thickness(self):
        type = self.cleaned_data.get('type')

        # Проверка на уникальность
        if FartukRailTypes.objects.filter(type=type).exists():
            self.add_error('type', "Це поле повинно бути унікальним. введіть значення, якого ще немає")

        return type


class FartukMembraneTypesForm(forms.ModelForm):
    class Meta:
        model = FartukMembraneTypes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True


class FartuksForm(forms.ModelForm):
    class Meta:
        model = Fartuks
        exclude = ('height', 'thickness')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Указываем обязательные поля
        required_fields = ['type', 'bottom_fartuk_rail_type', 'fartuk_membrane_type', 'top_fartuk_rail_type']
        for field in required_fields:
            self.fields[field].required = True


class CompanyForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,  # Поле обязательное
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите полное имя',  # Пример заполнения
            'class': 'form-control',  # Класс для Bootstrap
            'style': 'width: 100%;',  # Увеличить ширину поля
        }),
        label="Повне ім'я",  # Ярлык
        help_text='Обов`язково повинно співпадати символ в символ з 1С'  # Подсказка
    )

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
                self.fields['contact'].queryset = Contacts.objects.filter(
                    id__in=CompaniesContacts.objects.filter(company=self.instance).values_list('contact_id', flat=True)
                )
            else:
                self.fields['delivery_preset'].queryset = DeliveryPresets.objects.none()
                self.fields['contact'].queryset = Contacts.objects.none()


class AddressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = ('settlement_ref', 'post_office_ref', 'street', 'build')


class ContactsDetailsForm(forms.ModelForm):

    class Meta:
        model = ContactsDetails
        exclude = ('contact_info_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Указываем обязательные поля
        required_fields = ['contact',]
        for field in required_fields:
            self.fields[field].required = True


class ContactsForm(forms.ModelForm):

    class Meta:
        model = Contacts
        exclude = ('contacts_detail',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['first_name', ]
        for field in required_fields:
            self.fields[field].required = True

        if self.instance and self.instance.pk:
            self.fields['mail_contacts_detail'].queryset = ContactsDetails.objects.filter(
                contact=self.instance,
                contacttypes__type=ContactTypeChoices.EMAIL
            )
            self.fields['phone_contacts_detail'].queryset = ContactsDetails.objects.filter(
                contact=self.instance,
                contacttypes__type=ContactTypeChoices.TELEPHONE
            )
        else:
            self.fields['mail_contacts_detail'].queryset = ContactsDetails.objects.none()
            self.fields['phone_contacts_detail'].queryset = ContactsDetails.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем дубли в связанных таблицах
        mail_contact = cleaned_data.get('mail_contacts_detail')
        phone_contact = cleaned_data.get('phone_contacts_detail')

        if mail_contact and ContactsDetails.objects.filter(
            contact=self.instance,
            value=mail_contact.value
        ).exclude(pk=mail_contact.pk).exists():
            raise forms.ValidationError(f"Контакт с почтовым значением {mail_contact.value} уже существует.")

        if phone_contact and ContactsDetails.objects.filter(
            contact=self.instance,
            value=phone_contact.value
        ).exclude(pk=phone_contact.pk).exists():
            raise forms.ValidationError(f"Контакт с телефонным значением {phone_contact.value} уже существует.")

        # Проверка дубликатов в таблице companies_contacts
        contact_id = self.instance.pk  # или self.cleaned_data.get('contact') если не существует
        company_id = self.cleaned_data.get('company_id')  # предполагаем, что вы передаете company_id
        if company_id:
            if CompaniesContacts.objects.filter(contact_id=contact_id, company_id=company_id).exists():
                raise forms.ValidationError("Этот контакт уже связан с этой компанией.")

        return cleaned_data



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
                  'street', 'build', 'description',  'contact', 'is_legal_address', 'shipping_date_planed_start',
                  'shipping_date_planed_end')

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
