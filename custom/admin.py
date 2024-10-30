from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html

from .models import *


@admin.register(PaperSizes)
class PaperSizesAdmin(admin.ModelAdmin):
    list_display = ('type', 'height', 'width', 'cost')
    search_fields = ('type', 'height', 'width', 'cost')


@admin.register(PrintingMachineShafts)
class PrintingMachineShaftsAdmin(admin.ModelAdmin):
    list_display = ('id', 'diameter', 'quantity', 'width', 'printing_machine', 'thickness', 'date_create',
                    'input_value', 'input_value_type', 'contact', 'printing_width', 'description')

    autocomplete_fields = ['printing_machine', 'contact',]


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
    list_display = ('name', 'printing_company', 'material_thickness', 'fartuk', 'section', 'module')
    search_fields = ('name', 'printing_company__id__name')

    autocomplete_fields = ['printing_company',]


@admin.register(CompanyClients)
class CompanyClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'custom_is_banned', 'debt', 'company_our_brand', 'document_delivery_type', 'is_prepayment')
    search_fields = ('id__name',)

    def custom_is_banned(self, obj):
        if obj.is_banned is None:
            return 'Невідомо'
        return 'Так' if obj.is_banned else 'Ні'

    custom_is_banned.short_description = 'Заблокований'


@admin.register(CompanyOurBrands)
class CompanyOurBrandsAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbreviation')
    search_fields = ('id__name', 'abbreviation')


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ('name', 'okpo', 'full_name', 'company_group')
    search_fields = ('name', 'okpo', 'full_name')


@admin.register(AngleSetTypes)
class AngleSetTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)
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
