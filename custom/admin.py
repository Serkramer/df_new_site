from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from .admin_filters import PrintingCompanyWithShaftsFilter
from .forms import PrintingMachineShaftsForm, CompanyForm, DeliveryPresetsForm, PrintingMachinePresetsForm, \
    AdhesiveTapeThicknessesForm, FartukHeightsForm, PrintingMachinesForm
from .models import *


@admin.register(PaperSizes)
class PaperSizesAdmin(admin.ModelAdmin):
    list_display = ('type', 'height', 'width', 'cost')
    search_fields = ('type', 'height', 'width', 'cost')


@admin.register(PrintingMachineShafts)
class PrintingMachineShaftsAdmin(admin.ModelAdmin):
    list_display = ('printing_machine', 'diameter', 'quantity', 'width', 'thickness', 'date_create',
                    'input_value', 'input_value_type', 'contact', 'printing_width', 'description')

    autocomplete_fields = ['printing_machine', 'contact',]

    search_fields = ('printing_machine__printing_company__id__name', 'printing_machine__name')
    form = PrintingMachineShaftsForm
    list_filter = (PrintingCompanyWithShaftsFilter, )


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'description')
    search_fields = ('first_name', 'last_name')


@admin.register(PrintingCompanies)
class PrintingCompaniesAdmin(admin.ModelAdmin):
    list_display = ('id', 'process_id', 'color_library')
    search_fields = ('id__name',)

    autocomplete_fields = ['id', ]


@admin.register(PrintingMachines)
class PrintingMachinesAdmin(admin.ModelAdmin):
    list_display = ('name', 'printing_company', 'fartuk', 'section', 'module')
    search_fields = ('name', 'printing_company__id__name')
    form = PrintingMachinesForm
    autocomplete_fields = ['printing_company',]


@admin.register(ContactsDetails)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('contact', 'contact_info_type', 'value')
    search_fields = ('value', 'contact')


@admin.register(ContactInfoTypes)
class ContactInfoTypesAdmin(admin.ModelAdmin):
    list_display = ('type',)


@admin.register(PrintingMachinePresets)
class PrintingMachinePresetsAdmin(admin.ModelAdmin):
    list_display = ('printing_machine', 'name', 'material_thickness', 'ruling', 'raster_dot')
    search_fields = ('printing_machine', 'name')
    form = PrintingMachinePresetsForm
    autocomplete_fields = ['printing_machine', 'color_profile']


@admin.register(ColorProfiles)
class ColorProfileAdmin(admin.ModelAdmin):
    list_display = ('color_profile_file_name', )
    search_fields = ('color_profile_file_name', )


@admin.register(AdhesiveTapeThicknesses)
class AdhesiveTapeThicknessAdmin(admin.ModelAdmin):
    list_display = ('thickness',)
    form = AdhesiveTapeThicknessesForm


@admin.register(AdhesiveTapes)
class AdhesiveTapesAdmin(admin.ModelAdmin):
    list_display = ('description', 'manufacturer', 'series', 'adhesive_tape_thickness')
    search_fields = ('description', 'adhesive_tape_thickness__thickness')


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
    list_display = ('name', 'okpo', 'full_name', 'company_group')
    search_fields = ('name', 'okpo', 'full_name')

    autocomplete_fields = ['contact', 'company_group']
    form = CompanyForm


@admin.register(FartukHeights)
class FartukHeightsAdmin(admin.ModelAdmin):
    list_display = ('printing_machine', 'fartuk', 'height')
    search_fields = ('printing_machine', 'height')
    autocomplete_fields = ['printing_machine']
    form = FartukHeightsForm




@admin.register(DeliveryPresets)
class DeliveryPresetAdmin(admin.ModelAdmin):
    list_display = ('company', 'delivery_type', 'contact', 'description', 'name', 'address', 'custom_is_legal_address')
    autocomplete_fields = ['contact', 'company']
    search_fields = ('company', 'delivery_type')
    form = DeliveryPresetsForm

    def custom_is_legal_address(self, obj):
        if obj.is_legal_address is None:
            return 'Невідомо'
        return 'Так' if obj.is_legal_address else 'Ні'

    custom_is_legal_address.short_description = 'Перевірена адреса'


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


@admin.register(FartukMembraneTypes)
class FartukMemberTypesAdmin(admin.ModelAdmin):
    list_display = ('type', 'thickness')


@admin.register(Fartuks)
class FartuksAdmin(admin.ModelAdmin):
    list_display = ("description", "max_height", "max_width", "type", "bottom_fartuk_rail_type", "fartuk_membrane_type",
                    "top_fartuk_rail_type", "is_fixed", "height",)
