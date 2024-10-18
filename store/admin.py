from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Materials, MaterialHardness, MaterialSheets, Articles, MaterialSlices, MaterialSheetStores


# Register your models here.

@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'thickness', 'base_thickness_max', 'base_thickness_min', 'material_hardness',
                    'material_manufacturer', 'material_plate_type', 'material_process_type', 'material_solvent',
                    'is_polymeric', 'low_base_thickness_max', 'low_base_thickness_min', 'material_underlayment')
    list_editable = ['thickness', 'base_thickness_max', 'base_thickness_min', 'material_hardness',
                    'material_manufacturer', 'material_plate_type', 'material_process_type', 'material_solvent',
                    'is_polymeric', 'low_base_thickness_max', 'low_base_thickness_min', 'material_underlayment']


@admin.register(MaterialSheets)
class MaterialSheetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'height', 'width', 'material', 'article',)
    verbose_name = 'Лист матеріала'
    verbose_name_plural = 'Листи матеріала'


@admin.register(MaterialSheetStores)
class MaterialSheetStoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'count', 'cell_branch', 'material_sheet')
#
# @admin.register(Articles)
# class ArticlesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'barcode',)
#     search_fields = ['barcode__code', 'barcode__type']



