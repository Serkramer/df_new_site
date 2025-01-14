from django.contrib import admin

from custom.models import Companies
from .forms import PriceForm, CompanyWithNuancesForm
from OneC.models import Price, CompanyWithNuances


# Register your models here.
@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    form = PriceForm
    list_display = ('id', 'price', 'get_company', 'price_type', 'thickness_list', 'get_materials_list',)
    search_fields = ('price', 'company_id', 'thickness_list',)

    def get_search_results(self, request, queryset, search_term):
        # Получаем стандартные результаты поиска
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Извлекаем список ID компаний с помощью list()
            company_ids = list(
                Companies.objects.using('custom')
                .filter(name__icontains=search_term)
                .values_list('id', flat=True)
            )
            # Фильтруем записи модели Price
            queryset |= self.model.objects.filter(company_id__in=company_ids)

        return queryset, use_distinct

    def get_company(self, obj):
        company = obj.get_company()
        return company.name if company else "-"
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

