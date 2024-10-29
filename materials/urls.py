from django.contrib.auth.decorators import login_required
from django.urls import path

from materials.views import MaterialInfoView, MaterialsChartsView

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

]
