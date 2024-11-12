from django.contrib import admin

from .inline_forms import PrintingMachinesInlineForm
from .models import PrintingMachines, PrintingMachineShafts, PrintingMachinePresets, AniloxRolls
from django.utils.html import format_html
from django.urls import reverse


class PrintingMachineShaftsInline(admin.TabularInline):  # Или используйте admin.StackedInline для более детального представления
    model = PrintingMachineShafts
    extra = 1  # Число пустых форм для добавления новых объектов
    fields = ['quantity', 'width', 'date_create', 'input_value', 'input_value_type', 'contact', 'printing_width', 'description']
    classes = ['collapse']


class PrintingMachinePresetsInline(admin.TabularInline):
    model = PrintingMachinePresets
    extra = 1
    fields = ('printing_machine', 'name', 'ruling', 'angle_set', 'raster_dot', 'material_thickness',
              'cliche_technology', 'is_revert_printing', 'color_profile', 'plate_curve_strategy',
              'press_curve_strategy', 'damper', 'description', 'adhesive_tape_thickness_multiplier',
              'adhesive_tape_thickness', 'fartuk', 'material')
    classes = ['collapse']


class AniloxRollsInline(admin.TabularInline):
    model = AniloxRolls
    extra = 1
    fields = ('line_count', 'transfer_volume', 'type', 'description')
    classes = ['collapse']


class PrintingMachinesInline(admin.TabularInline):
    model = PrintingMachines
    form = PrintingMachinesInlineForm  # Подключаем кастомную форму
    extra = 1
    fields = ['name', 'fartuk', 'section', 'module', 'view_link']
    readonly_fields = ['view_link']
    classes = ['collapse']

    def view_link(self, obj):
        if obj.id:
            url = reverse('admin:custom_printingmachines_change', args=[obj.id])
            return format_html('<a href="{}" target="_blank">переглянути</a>', url)
        return "Не збережено"

    view_link.short_description = 'Подивитися'


