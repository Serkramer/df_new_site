from django.contrib.auth.decorators import login_required
from django.urls import path

from materials.views import MaterialInfoView

urlpatterns = [

    path(
        "check-list",
        login_required(MaterialInfoView.as_view(template_name="materials/material-info-table.html")),
        name="material-info-table",
    ),

]
