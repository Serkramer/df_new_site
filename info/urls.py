from django.contrib.auth.decorators import login_required
from django.urls import path

from info.views import PrintingRollersView, FartukViews

app_name = 'info'

urlpatterns = [

    path(
        "printing-rollers",
        login_required(PrintingRollersView.as_view()),
        name="printing-rollers"
    ),

    path(
        "printing-machine-fartuks",
        login_required(FartukViews.as_view(template_name='info/printing-machine-fartks.html')),
        name="printing-machine-fartks"
    )

]
