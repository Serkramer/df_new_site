from django.contrib import admin

from .forms import PriceForm, CompanyWithNuancesForm
from OneC.models import Price, CompanyWithNuances


# Register your models here.
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    form = PriceForm
    list_display = ('id', 'price', 'get_company', 'price_type', 'thickness_list', 'get_materials_list',)
    search_fields = ('price', 'company_id', 'thickness_list')

    def get_company(self, obj):
        return obj.get_company().name
    get_company.short_description = 'Компанія'

    def get_materials_list(self, obj):
        materials = obj.get_materials()
        if materials:
            return ', '.join([material.name for material in materials])
        return "-"

    get_materials_list.short_description = 'Матеріали'


@admin.register(CompanyWithNuances)
class CompanyWithNuancesAdmin(admin.ModelAdmin):
    form = CompanyWithNuancesForm
    list_display = ('get_company', 'check_with_cents', 'name_order_in_check', 'group_orders', 'text_before','unique_order_name')

    def get_company(self, obj):
        return obj.get_company().name

    get_company.short_description = 'Компанія'

