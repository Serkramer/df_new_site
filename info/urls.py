from django.contrib.auth.decorators import login_required
from django.urls import path

from info.views import PrintingRollersView

urlpatterns = [

    path(
        "printing-rollers",
        login_required(PrintingRollersView.as_view()),
        name="printing-rollers"
    ),

]
