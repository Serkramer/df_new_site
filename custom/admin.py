from django.contrib import admin
from django.db.models import Subquery, OuterRef, F, Value, Func, CharField
from django.db.models.functions import Coalesce
import pytz
from .admin_filters import PrintingCompanyWithShaftsFilter
from .forms import PrintingMachineShaftsForm, CompanyForm, DeliveryPresetsForm, PrintingMachinePresetsForm, \
    AdhesiveTapeThicknessesForm, FartukHeightsForm, PrintingMachinesForm, FartuksForm, FartukRailTypesForm, \
    FartukMembraneTypesForm, AniloxRollForm, ContactsDetailsForm, ContactsForm, AddressesForm
from .inlines import PrintingMachineShaftsInline, PrintingMachinesInline, PrintingMachinePresetsInline, \
    AniloxRollsInline, CompanyClientsInline, PrintingCompaniesInline, DeliveryPresetsInline, ContactsDetailsInline, \
    CompaniesContactsForContactInline, CompaniesContactsInline, DeliveryPresetsInAddressInline
from .models import *
from datetime import datetime, time, timedelta
from django.utils.html import format_html
from django.urls import reverse

class GroupConcat(Func):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(expressions)s SEPARATOR ", ")'

@admin.register(PaperSizes)
class PaperSizesAdmin(admin.ModelAdmin):
    list_display = ('type', 'height', 'width', 'cost')
    search_fields = ('type', 'height', 'width', 'cost')


@admin.register(PrintingMachineShafts)
class PrintingMachineShaftsAdmin(admin.ModelAdmin):
    list_display = ('get_printing_company', 'printing_machine', 'diameter', 'quantity', 'width', 'thickness',
                    'date_create', 'input_value', 'input_value_type', 'contact', 'printing_width', 'description')

    autocomplete_fields = ['printing_machine', 'contact',]

    search_fields = ('printing_machine__printing_company__id__name', 'printing_machine__name')
    form = PrintingMachineShaftsForm
    list_filter = (PrintingCompanyWithShaftsFilter, )

    @admin.display(description="Друкарська компанія", ordering="printing_machine__printing_company__id__name")
    def get_printing_company(self, obj):
        return obj.printing_machine.printing_company if obj.printing_machine else None


@admin.register(Engravers)
class EngraversAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'name', 'put_into_operation')


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('edit_button', 'first_name', 'last_name', 'middle_name', 'description', 'get_company_from_contact',
                    'get_contact_details')
    search_fields = ('first_name', 'last_name', 'description', 'companies_search', 'contact_details_search')

    form = ContactsForm

    inlines = [ContactsDetailsInline, CompaniesContactsForContactInline]

    @admin.display(description="Редагувати")
    def edit_button(self, obj):
        url = reverse('admin:custom_contacts_change', args=[obj.id])
        return format_html(
            '<a href="{}"  title="Редагувати">'
            '✏️</a>',
            url
        )

    @admin.display(description="З якими компаніями пов'язаний")
    def get_company_from_contact(self, obj):
        companies = CompaniesContacts.objects.filter(contact=obj).select_related('company')
        return ", ".join(set(company.company.name for company in companies if company.company))

    @admin.display(description="Контактна інформація")
    def get_contact_details(self, obj):
        contact_details = ContactsDetails.objects.filter(contact=obj)
        return ", ".join(set(contact_details.value for contact_details in contact_details if contact_details and contact_details.value))

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Агрегация значений компаний через GROUP_CONCAT
        companies = CompaniesContacts.objects.filter(contact=OuterRef('pk')).annotate(
            companies_agg=GroupConcat('company__name')
        ).values('companies_agg')

        # Агрегация значений контактной информации через GROUP_CONCAT
        contact_details = ContactsDetails.objects.filter(contact=OuterRef('pk')).annotate(
            details_agg=GroupConcat('value')
        ).values('details_agg')

        # Добавляем аннотации для поиска
        annotated_queryset = qs.annotate(
            companies_search=Coalesce(
                Subquery(companies[:1], output_field=CharField()),
                Value('')
            ),
            contact_details_search=Coalesce(
                Subquery(contact_details[:1], output_field=CharField()),
                Value('')
            )
        )
        return annotated_queryset


@admin.register(PrintingCompanies)
class PrintingCompaniesAdmin(admin.ModelAdmin):
    list_display = ('id', 'process_id', 'color_library', 'get_use_low_base', 'get_need_printout', 'get_label')
    search_fields = ('id__name',)

    autocomplete_fields = ['id', ]
    inlines = (PrintingMachinesInline,)

    @admin.display(description='Використовує занижений цоколь', ordering='use_low_base')
    def get_use_low_base(self, obj):
        if obj.use_low_base is True:
            return "Так"
        elif obj.use_low_base is False:
            return "Ні"
        return "Невідомо"

    @admin.display(description='Чи потрібны документи', ordering='need_printout')
    def get_need_printout(self, obj):
        if obj.need_printout is True:
            return "Так"
        elif obj.need_printout is False:
            return "Ні"
        return "Невідомо"

    @admin.display(description='Чи потрібен підпис', ordering='need_label')
    def get_label(self, obj):
        if obj.need_label is True:
            return "Так"
        elif obj.need_label is False:
            return "Ні"
        return "Невідомо"


@admin.register(PrintingMachines)
class PrintingMachinesAdmin(admin.ModelAdmin):
    list_display = ('name', 'printing_company', 'fartuk', 'section', 'module')
    search_fields = ('name', 'printing_company__id__name')
    form = PrintingMachinesForm
    autocomplete_fields = ['printing_company',]
    inlines = [PrintingMachineShaftsInline, PrintingMachinePresetsInline, AniloxRollsInline]


@admin.register(AniloxRolls)
class AniloxRollAdmin(admin.ModelAdmin):
    list_display = ('printing_machine', 'line_count', 'transfer_volume', 'type', 'description', 'get_printing_company')
    search_fields = ('printing_machine', 'line_count')
    autocomplete_fields = ['printing_machine', ]
    form = AniloxRollForm

    @admin.display(description="Друкарська компанія", ordering="printing_machine__printing_company__id__name")
    def get_printing_company(self, obj):
        return obj.printing_machine.printing_company if obj.printing_machine else None


@admin.register(ContactsDetails)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('contact', 'contact_info_type', 'value')
    search_fields = ('value', 'contact')

    form = ContactsDetailsForm


@admin.register(PrintingMachinePresets)
class PrintingMachinePresetsAdmin(admin.ModelAdmin):
    list_display = ('get_printing_company', 'printing_machine', 'name', 'material_thickness', 'ruling', 'raster_dot')
    search_fields = ('printing_machine', 'name')
    form = PrintingMachinePresetsForm
    autocomplete_fields = ['printing_machine', 'color_profile']

    @admin.display(description="Друкарська компанія", ordering="printing_machine__printing_company__id__name")
    def get_printing_company(self, obj):
        return obj.printing_machine.printing_company if obj.printing_machine else None


@admin.register(ColorProfiles)
class ColorProfileAdmin(admin.ModelAdmin):
    list_display = ('color_profile_file_name', )
    search_fields = ('color_profile_file_name', )


@admin.register(AdhesiveTapeThicknesses)
class AdhesiveTapeThicknessAdmin(admin.ModelAdmin):
    list_display = ('thickness',)
    form = AdhesiveTapeThicknessesForm


# @admin.register(Addresses)
# class AddressesAdmin(admin.ModelAdmin):
#     list_display = ('get_settlement_ref', 'get_post_office_ref', 'street', 'build')
#     search_fields = ('street', 'build', 'get_settlement_ref', 'get_post_office_ref')
#     form = AddressesForm
#
#     inlines = [DeliveryPresetsInAddressInline]
#
#     @admin.display(description='Населенний пункт')
#     def get_settlement_ref(self, obj):
#         if obj.settlement_ref:
#             settlement = Settlements.objects.filter(ref=obj.settlement_ref).first()
#             if settlement:
#                 return settlement.description
#         return '---'
#
#     @admin.display(description="Відділення НП")
#     def get_post_office_ref(self, obj):
#         if obj.post_office_ref:
#             post_office = PostOffices.objects.filter(ref=obj.post_office_ref).first()
#             if post_office:
#                 return post_office.description
#         return '---'


@admin.register(AdhesiveTapes)
class AdhesiveTapesAdmin(admin.ModelAdmin):
    list_display = ('description', 'manufacturer', 'series', 'adhesive_tape_thickness')
    search_fields = ('description', 'adhesive_tape_thickness__thickness')


@admin.register(ClicheTechnologies)
class ClicheTechnologiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'cliche_technology_type', 'len_file_resolution', 'thickness_min','thickness_max')


@admin.register(CompanyClients)
class CompanyClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'custom_is_banned', 'debt', 'company_our_brand', 'document_delivery_type', 'is_prepayment')
    search_fields = ('id__name',)

    def custom_is_banned(self, obj):
        if obj.is_banned is None:
            return 'Невідомо'
        return 'Так' if obj.is_banned else 'Ні'

    custom_is_banned.short_description = 'Заблокований'


@admin.register(ColorProofOrders)
class ColorProofOrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'launch_date', 'color_proof_file_name', 'count')


@admin.register(CompanyOurBrands)
class CompanyOurBrandsAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbreviation')
    search_fields = ('id__name', 'abbreviation')


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'okpo', 'full_name', 'company_group', 'get_is_verified', 'get_is_outdated')
    search_fields = ('name', 'okpo', 'full_name')

    autocomplete_fields = ['company_group']
    form = CompanyForm

    inlines = [CompanyClientsInline, PrintingCompaniesInline, CompaniesContactsInline, DeliveryPresetsInline]

    @admin.display(description='Перевірений', ordering='is_verified')
    def get_is_verified(self, obj):
        if obj.is_verified is True:
            return "Так"
        elif obj.is_verified is False:
            return "Ні"
        return "Невідомо"

    @admin.display(description='Застарілий', ordering='is_outdated')
    def get_is_outdated(self, obj):
        if obj.is_outdated is True:
            return "Так"
        elif obj.is_outdated is False:
            return "Ні"
        return "Невідомо"


@admin.register(FartukHeights)
class FartukHeightsAdmin(admin.ModelAdmin):
    list_display = ('printing_machine', 'fartuk', 'height')
    search_fields = ('printing_machine', 'height')
    autocomplete_fields = ['printing_machine']
    form = FartukHeightsForm


@admin.register(DeliveryPresets)
class DeliveryPresetAdmin(admin.ModelAdmin):
    list_display = ('company', 'delivery_type', 'contact', 'description', 'name', 'address',
                    'custom_is_legal_address', 'shipping_date_planed_start_display', 'shipping_date_planed_end_display')
    autocomplete_fields = ['contact', 'company']
    search_fields = ('company__name', 'delivery_type__type')
    form = DeliveryPresetsForm

    def custom_is_legal_address(self, obj):
        if obj.is_legal_address is None:
            return 'Невідомо'
        return 'Так' if obj.is_legal_address else 'Ні'

    custom_is_legal_address.short_description = 'Перевірена адреса'

    def shipping_date_planed_start_display(self, obj):
        if obj.shipping_date_planed_start:
            kiev_tz = pytz.timezone('Europe/Kiev')  # Используем pytz для работы с временными зонами

            # Преобразуем время (datetime.time) в datetime с сегодняшней датой
            time_as_datetime = datetime.combine(datetime.today(), obj.shipping_date_planed_start)

            # Преобразуем в UTC, затем в Киевскую временную зону
            local_time = time_as_datetime.replace(tzinfo=pytz.utc).astimezone(kiev_tz).time()

            return local_time.strftime('%H:%M')
        return '-'

    shipping_date_planed_start_display.short_description = 'Час доставки з'

    def shipping_date_planed_end_display(self, obj):
        if obj.shipping_date_planed_end:
            kiev_tz = pytz.timezone('Europe/Kiev')  # Используем pytz для работы с временными зонами

            # Преобразуем время (datetime.time) в datetime с сегодняшней датой
            time_as_datetime = datetime.combine(datetime.today(), obj.shipping_date_planed_end)

            # Преобразуем в UTC, затем в Киевскую временную зону
            local_time = time_as_datetime.replace(tzinfo=pytz.utc).astimezone(kiev_tz).time()

            return local_time.strftime('%H:%M')
        return '-'

    shipping_date_planed_end_display.short_description = 'Час доставки по'

@admin.register(AngleSetTypes)
class AngleSetTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CompanyGroups)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(AngleSets)
class AngleSetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'angle_set_type', 'cyan', 'magenta', 'yellow', 'black', 'green', 'orange', 'violet',
                    'other',)


@admin.register(ColorLibraries)
class ColorLibrariesAdmin(admin.ModelAdmin):
    list_display = ('description', 'type', )


@admin.register(Colors)
class ColorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'red', 'green', 'blue', 'html', 'color_library',)


@admin.register(RasterDotMicroscreens)
class RasterDotMicroscreensAdmin(admin.ModelAdmin):
    list_display = ('microscreen',)


@admin.register(RasterDotTypes)
class RasterDotTypesAdmin(admin.ModelAdmin):
    list_display = ('type',)


@admin.register(Rulings)
class RulingAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(YellowRulings)
class YellowRulingsAdmin(admin.ModelAdmin):
    list_display = ('value', )


@admin.register(RasterDotMicroscreenMainDots)
class RasterDotMicroscreenMainDotsAdmin(admin.ModelAdmin):
    list_display = ('dot',)


@admin.register(RasterDots)
class RasterDotsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'min_dot_size', 'raster_dot_microscreen', 'raster_dot_microscreen_main_dot',
                    'raster_dot_type')


@admin.register(LenFileResolutions)
class LenFileResolutionAdmin(admin.ModelAdmin):
    list_display = ('resolution',)


@admin.register(RulingRelationships)
class RulingRelationshipsAdmin(admin.ModelAdmin):
    list_display = ('angle_set_type', 'len_file_resolution', 'ruling', 'raster_dot')
    search_fields = ('raster_dot__name', 'raster_dot__code')


@admin.register(FartukRailTypes)
class FartukRailTypesAdmin(admin.ModelAdmin):
    list_display = ('type',)
    form = FartukRailTypesForm


@admin.register(FartukMembraneTypes)
class FartukMemberTypesAdmin(admin.ModelAdmin):
    list_display = ('type', 'thickness')
    form = FartukMembraneTypesForm


@admin.register(Fartuks)
class FartuksAdmin(admin.ModelAdmin):
    list_display = ("type", "description", "max_height", "max_width", "bottom_fartuk_rail_type",
                    "fartuk_membrane_type",
                    "top_fartuk_rail_type", "is_fixed", )

    form = FartuksForm

