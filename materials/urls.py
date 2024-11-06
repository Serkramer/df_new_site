from django.contrib.auth.decorators import login_required
from django.urls import path

from materials.views import MaterialInfoView, MaterialsChartsView, filter_materials_by_thickness

app_name = 'materials'

urlpatterns = [

    path(
        "material-info-table",
        login_required(MaterialInfoView.as_view(template_name="materials/material-info-table.html")),
        name="material-info-table"
    ),

    path(
        "material-charts",
        login_required(MaterialsChartsView.as_view()),
        name="materials-charts"
    ),

    path('filter-materials/', filter_materials_by_thickness, name='filter_materials_by_thickness'),

]
