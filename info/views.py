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
            list_printing_machine_data = []
            for presets in printing_machine_presets:
                material_thickness = presets.material.thickness
                fartuk_thickness = presets.fartuk.thickness if presets.fartuk else None
                damper_thickness = presets.damper
                if not presets.adhesive_tape_thickness_multiplier:
                    adhesive_tape_thickness = presets.adhesive_tape_thickness.thickness if presets.adhesive_tape_thickness else None
                else:
                    adhesive_tape_thickness = presets.adhesive_tape_thickness.thickness * presets.adhesive_tape_thickness_multiplier if presets.adhesive_tape_thickness else None

                data = {
                    'material_thickness': material_thickness,
                    'fartuk_thickness': fartuk_thickness,
                    'damper_thickness': damper_thickness,
                    'adhesive_tape_thickness': adhesive_tape_thickness,
                    'fartuk': presets.fartuk
                }
                if data not in list_printing_machine_data:
                    list_printing_machine_data.append(data)

            for data in list_printing_machine_data:
                shaft.data = data
                material_underlayment = MaterialUnderlayments.objects.filter(id=1).first() if float(
                    shaft.data['material_thickness']) == 1.14 else MaterialUnderlayments.objects.filter(
                    id=1).first()

                thickness_material_underlayment = float(material_underlayment.thickness)
                fartuk_thickness = float(shaft.data['fartuk_thickness']) if shaft.data['fartuk_thickness'] else 0
                damper_thickness = float(shaft.data['damper_thickness']) if shaft.data['damper_thickness'] else 0
                adhesive_tape_thickness = float(shaft.data['adhesive_tape_thickness']) if shaft.data[
                    'adhesive_tape_thickness'] else 0
                material_thickness = float(shaft.data['material_thickness']) if shaft.data['material_thickness'] else 0

                if shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.NUMBER_OF_TEETH:
                    shaft.number_of_teeth = shaft.input_value
                    shaft.rapport = shaft.number_of_teeth * shaft.printing_machine.module \
                        if (shaft.printing_machine and shaft.printing_machine.module) \
                        else shaft.number_of_teeth * settings.DEFAULT_PRINTING_MACHINE_MODUL
                    shaft.printing_diameter = round(float(shaft.rapport) / pi, 2)

                    shaft.metal_diameter = (float(shaft.printing_diameter) - 2 * (
                        material_thickness + fartuk_thickness + damper_thickness + adhesive_tape_thickness)) \
                        if material_thickness and adhesive_tape_thickness else None

                    shaft.circumference = round(shaft.metal_diameter * pi, 2)
                    shaft.distortion = round((float(shaft.metal_diameter) + 2 *
                                              (thickness_material_underlayment + fartuk_thickness + damper_thickness +
                                               adhesive_tape_thickness)) / shaft.printing_diameter * 100, 3)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.RAPPORT:
                    shaft.number_of_teeth = 0
                    shaft.rapport = shaft.input_value
                    shaft.printing_diameter = round(shaft.shaft.rapport / pi, 2)
                    shaft.metal_diameter = (float(shaft.printing_diameter) -
                                            2 *
                                            (material_thickness +
                                             fartuk_thickness +
                                             damper_thickness +
                                             adhesive_tape_thickness

                                             )) if material_thickness and \
                                                   adhesive_tape_thickness else None
                    shaft.circumference = round(shaft.metal_diameter * pi, 2)
                    shaft.distortion = round((float(shaft.metal_diameter) + 2 *
                                              ((
                                                  thickness_material_underlayment +
                                                  fartuk_thickness +
                                                  damper_thickness +
                                                  adhesive_tape_thickness
                                              ))) / shaft.printing_diameter * 100, 3)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.DIAMETER:
                    shaft.number_of_teeth = 0
                    shaft.printing_diameter = shaft.input_value
                    shaft.rapport = round(shaft.printing_diameter * pi, 2)
                    shaft.metal_diameter = (float(shaft.printing_diameter) - 2 * (material_thickness +
                                                                                  fartuk_thickness + damper_thickness +
                                                                                  adhesive_tape_thickness)) \
                        if material_thickness and adhesive_tape_thickness else None
                    shaft.circumference = round(shaft.metal_diameter * pi, 2)
                    shaft.distortion = round((float(shaft.metal_diameter) + 2 * (thickness_material_underlayment +
                                                                                 fartuk_thickness + damper_thickness +
                                                                                 adhesive_tape_thickness)) / shaft.printing_diameter * 100,
                                             3)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.METAL_DIAMETER:
                    shaft.number_of_teeth = 0
                    shaft.metal_diameter = shaft.input_value
                    shaft.circumference = round(float(shaft.metal_diameter) * pi, 2)
                    shaft.printing_diameter = (float(shaft.metal_diameter) +
                                               2 *
                                               (material_thickness +
                                                fartuk_thickness +
                                                damper_thickness +
                                                adhesive_tape_thickness

                                                )) if material_thickness and \
                                                      adhesive_tape_thickness else None
                    shaft.rapport = round(shaft.printing_diameter * pi, 2)
                    shaft.distortion = round((float(shaft.metal_diameter)
                                              + 2 * (thickness_material_underlayment +
                                                     fartuk_thickness + damper_thickness +
                                                     adhesive_tape_thickness)) / shaft.printing_diameter * 100,
                                             3)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.CIRCUMFERENCE:
                    shaft.number_of_teeth = 0
                    shaft.circumference = shaft.input_value
                    shaft.metal_diameter = round(float(shaft.circumference) / pi, 2)
                    shaft.printing_diameter = (float(shaft.metal_diameter) +
                                               2 *
                                               (material_thickness + fartuk_thickness + damper_thickness +
                                                adhesive_tape_thickness)
                                               ) if material_thickness and adhesive_tape_thickness else None
                    shaft.rapport = round(shaft.printing_diameter * pi, 2)
                    shaft.distortion = round((float(shaft.metal_diameter) + 2 *
                                              (thickness_material_underlayment + fartuk_thickness + damper_thickness +
                                               adhesive_tape_thickness)) / shaft.printing_diameter * 100, 3)

                elif shaft.input_value_type == PrintingMachineShaftsInputValueTypeList.DISTORTION:
                    shaft.number_of_teeth = 0
                    shaft.distortion = shaft.input_value


                    # Верхняя и нижняя части из формулы
                    upper_part = thickness_material_underlayment + fartuk_thickness + damper_thickness + adhesive_tape_thickness
                    lower_part = material_thickness + fartuk_thickness + damper_thickness + adhesive_tape_thickness

                    # Переводим shaft.distortion в distortion_factor
                    distortion_factor = float(shaft.distortion) / 100

                    # Вычисляем metal_diameter
                    if distortion_factor != 1:  # проверка деления на ноль
                        shaft.metal_diameter = (2 * (upper_part - distortion_factor * lower_part)) / (distortion_factor - 1)
                    else:
                        shaft.metal_diameter = None

                    shaft.circumference = round(float(shaft.metal_diameter) * pi, 2)
                    shaft.printing_diameter = (float(shaft.metal_diameter) +
                                               2 *
                                               (material_thickness +
                                                fartuk_thickness +
                                                damper_thickness +
                                                adhesive_tape_thickness

                                                )) if material_thickness and adhesive_tape_thickness else None
                    shaft.rapport = round(shaft.printing_diameter * pi, 2)

                shaft.minus_from_rapport = round(shaft.rapport * (1 - shaft.distortion / 100), 2)
                shaft.rapport_with_distortion = round(shaft.rapport - shaft.minus_from_rapport, 2)

                table_shafts.append(shaft)

        context['shafts'] = table_shafts
        return context


class FartukViews(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['fartuks'] = None
        return context

