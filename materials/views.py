from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Prefetch, Sum
from store.models import Materials, MaterialSheets, MaterialSheetStores
from web_project import TemplateLayout


# Create your views here.


class MaterialInfoView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        materials = Materials.objects.prefetch_related(
            Prefetch('materialsheets_set', queryset=MaterialSheets.objects.all())
        ).annotate(sheet_count=Sum('materialsheets__materialsheetstores__count')).filter(materialsheets__isnull=False)

        for material in materials:
            print(material)


        context['materials'] = materials

        context['material_sheets'] = MaterialSheets.objects.all()
        context['material_sheet_stores'] = MaterialSheetStores.objects.all()
        return context
