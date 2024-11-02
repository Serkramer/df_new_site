from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from config import settings
from custom.models import PrintingMachineShafts, PrintingMachinePresets, PrintingMachineShaftsInputValueTypeList
from web_project import TemplateLayout


# Create your views here.


class PrintingRollersView(TemplateView):
    template_name = "info/printings_rollers.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        shafts = PrintingMachineShafts.objects.all().order_by('-printing_machine__printing_company__id__name')
        table_shafts = []
        for shaft in shafts:
            printing_machine_presets = PrintingMachinePresets.objects.filter(printing_machine=shaft.printing_machine)
            list_printing_machine_preset_thickness = []
            for presets in printing_machine_presets:
                material_thickness = presets.material.thickness
                fartuk_thickness = presets.fartuk.thickness if presets.fartuk else None
                damper_thickness = presets.damper
                if not presets.adhesive_tape_thickness_multiplier:
                    adhesive_tape_thickness = presets.adhesive_tape_thickness.thickness if presets.adhesive_tape_thickness else None
                else:
                    adhesive_tape_thickness = presets.adhesive_tape_thickness.thickness * presets.adhesive_tape_thickness_multiplier if presets.adhesive_tape_thickness else None

                thickness_data = {
                    'material_thickness': material_thickness,
                    'fartuk_thickness': fartuk_thickness,
                    'damper_thickness': damper_thickness,
                    'adhesive_tape_thickness': adhesive_tape_thickness
                }
                if thickness_data not in list_printing_machine_preset_thickness:
                    list_printing_machine_preset_thickness.append(thickness_data)

            for thickness in list_printing_machine_preset_thickness:
                shaft.thickness_data = thickness
                table_shafts.append(shaft)

            if shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.NUMBER_OF_TEETH:
                number_of_teeth = shaft.input_value
                rapport = number_of_teeth * shaft.printing_machine.module \
                    if (shaft.printing_machine and shaft.printing_machine.module) \
                    else number_of_teeth * settings.DEFAULT_PRINTING_MACHINE_MODUL
                diameter = None
                metal_diameter = None
                circumference = None
                distortion = None

            pass

        context['shafts'] = table_shafts
        return context
