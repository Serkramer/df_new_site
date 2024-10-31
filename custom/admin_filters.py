from django.contrib.admin import SimpleListFilter
from django.db.models import Count


class PrintingCompanyWithShaftsFilter(SimpleListFilter):
    title = 'Друкарська компанія'
    parameter_name = 'printing_machine__printing_company__id__name'

    def lookups(self, request, model_admin):
        # Выбираем только компании с количеством Shafts больше нуля
        companies = model_admin.get_queryset(request) \
            .values_list('printing_machine__printing_company__id', 'printing_machine__printing_company__id__name') \
            .annotate(num_shafts=Count('id')) \
            .filter(num_shafts__gt=0)
        return [(company[0], company[1]) for company in companies]

    def queryset(self, request, queryset):
        # Фильтруем по выбранной компании, если параметр задан
        if self.value():
            return queryset.filter(printing_machine__printing_company__id=self.value())
        return queryset
