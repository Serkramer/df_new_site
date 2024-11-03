

from store.models import MaterialSheets, BarcodeTypeList, Barcodes
from django import forms


class MaterialSheetsForm(forms.ModelForm):
    class Meta:
        model = MaterialSheets
        fields = ('height', 'width', 'material',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = ['height', 'width', 'material']
        for field in required_fields:
            self.fields[field].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            if not instance.pk:
                barcode_data = {
                    'type': BarcodeTypeList.SHEET,
                    #TODO ask about generate
                    'code': ''
                }

                barcode, created = Barcodes.objects.update_or_create(
                    id=instance.barcode_id, defaults=barcode_data
                )
                instance.barcode = barcode
                instance.save()

                #TODO add article

        return instance
