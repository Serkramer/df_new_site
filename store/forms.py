from custom.models import Companies
from store.models import MaterialSheets, BarcodeTypeList, Barcodes, MaterialHardnessTypes, MaterialHardness, Articles, \
    Cells, CompanyOwnerOfMaterialEntity
from django import forms


class MaterialHardnessTypesForm(forms.ModelForm):
    class Meta:
        model = MaterialHardnessTypes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True


class MaterialHardnessForm(forms.ModelForm):
    class Meta:
        model = MaterialHardness
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True


class MaterialSheetsForm(forms.ModelForm):

    cell = forms.ModelChoiceField(
        label="Склад",
        required=True,
        queryset=Cells.objects.all(),
    )

    company_owner_of_material = forms.ModelChoiceField(
        label='Чий матеріал',
        queryset=CompanyOwnerOfMaterialEntity.objects.all(),
        required=True
    )

    class Meta:
        model = MaterialSheets
        fields = ('height', 'width', 'material', 'cell')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Получаем все компании из базы custom
        companies = Companies.objects.using('custom').all()

        # Создаем словарь, чтобы сопоставить company_owner_of_material.id и Companies.name
        company_choices = {
            owner.id: company.name
            for owner in CompanyOwnerOfMaterialEntity.objects.all()
            for company in companies
            if owner.id == company.id  # предполагается, что IDs совпадают
        }

        # Настраиваем label для отображения имени компании
        self.fields['company_owner_of_material'].label_from_instance = lambda obj: company_choices.get(obj.id,
                                                                                                       "Неизвестная компания")

        required_fields = ['height', 'width', 'material']
        for field in required_fields:
            self.fields[field].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            if not instance.pk:
                code = f"{instance.material.material_manufacturer} | {instance.material.width}x{instance.material.height} | {instance.material.name}"
                barcode_data = {
                    'type': BarcodeTypeList.SHEET,
                    'code': code
                }

                barcode, created = Barcodes.objects.update_or_create(
                    id=instance.barcode_id, defaults=barcode_data
                )
                instance.barcode = barcode

                #TODO add article

                article_data = {
                    "barcode": instance.barcode,
                    "cell": instance.cell,
                    "company_owner_of_material": instance.company_owner_of_material
                }

                article, created = Articles.objects.update_or_create(
                    id=instance.article_id, defaults=article_data
                )
                instance.article = article

                instance.save()

        return instance
