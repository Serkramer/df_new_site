from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from math import pi
from config import settings
from custom.models import PrintingMachineShafts, PrintingMachinePresets, PrintingMachineShaftsInputValueTypeList
from store.models import MaterialUnderlayments
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
                material_underlayment = MaterialUnderlayments.objects.filter(id=1).first() if float(
                    shaft.thickness_data['material_thickness']) == 1.14 else MaterialUnderlayments.objects.filter(
                    id=1).first()

                if shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.NUMBER_OF_TEETH:
                    shaft.number_of_teeth = shaft.input_value
                    shaft.rapport = shaft.number_of_teeth * shaft.printing_machine.module \
                        if (shaft.printing_machine and shaft.printing_machine.module) \
                        else shaft.number_of_teeth * settings.DEFAULT_PRINTING_MACHINE_MODUL
                    shaft.printing_diameter = round(float(shaft.rapport) / pi, 2)
                    shaft.diameter = None
                    shaft.metal_diameter = None
                    shaft.circumference = None
                    shaft.distortion = None

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.RAPPORT:
                    shaft.number_of_teeth = 0
                    shaft.rapport = shaft.input_value
                    shaft.diameter = None
                    shaft.metal_diameter = None
                    shaft.circumference = None
                    shaft.distortion = None
                    shaft.printing_diameter = None

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.DIAMETER:
                    shaft.number_of_teeth = 0
                    shaft.rapport = None
                    shaft.diameter = shaft.input_value
                    shaft.metal_diameter = None
                    shaft.circumference = None
                    shaft.distortion = None
                    shaft.printing_diameter = None
                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.METAL_DIAMETER:
                    shaft.number_of_teeth = 0

                    shaft.diameter = None
                    shaft.metal_diameter = shaft.input_value
                    shaft.circumference = round(float(shaft.metal_diameter) * pi, 2)
                    shaft.printing_diameter = (float(shaft.metal_diameter) +
                                               2 *
                                               ((
                                                    float(shaft.thickness_data['material_thickness']) if
                                                    shaft.thickness_data['material_thickness'] else 0) +
                                                (
                                                    float(shaft.thickness_data['fartuk_thickness']) if
                                                    shaft.thickness_data['fartuk_thickness'] else 0) +
                                                (
                                                    float(shaft.thickness_data['damper_thickness']) if
                                                    shaft.thickness_data['damper_thickness'] else 0) +
                                                (
                                                    float(shaft.thickness_data['adhesive_tape_thickness']) if
                                                    shaft.thickness_data['adhesive_tape_thickness'] else 0)

                                                )) if shaft.thickness_data['material_thickness'] and \
                                                      shaft.thickness_data['adhesive_tape_thickness'] else None
                    shaft.rapport = round(shaft.printing_diameter * pi, 2)
                    # shaft.distortion = round((float(shaft.metal_diameter) + 2 *
                    #                          (float(shaft.thickness_data['material_thickness']) +
                    #                           float(material_underlayment.thickness) +
                    #                           (float(shaft.thickness_data['fartuk_thickness']) if shaft.thickness_data[
                    #                               'fartuk_thickness'] else 0) +
                    #                           (float(shaft.thickness_data['damper_thickness']) if shaft.thickness_data[
                    #                               'damper_thickness'] else 0) +
                    #                           (float(shaft.thickness_data['adhesive_tape_thickness']) if
                    #                            shaft.thickness_data['adhesive_tape_thickness'] else 0)
                    #                           )) / shaft.printing_diameter * 100,  2)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.CIRCUMFERENCE:
                    shaft.number_of_teeth = 0
                    shaft.rapport = None
                    shaft.diameter = None
                    shaft.metal_diameter = None
                    shaft.circumference = shaft.input_value
                    shaft.distortion = None
                    shaft.printing_diameter = None
                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.CIRCUMFERENCE:
                    shaft.number_of_teeth = 0
                    shaft.rapport = None
                    shaft.diameter = None
                    shaft.metal_diameter = None
                    shaft.circumference = None
                    shaft.distortion = shaft.input_value
                    shaft.printing_diameter = None

                table_shafts.append(shaft)

        context['shafts'] = table_shafts
        return context
