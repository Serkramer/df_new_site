from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'custom'

urlpatterns = [
    path('company-clients/', login_required(views.CompanyClientsAutocomplete.as_view()),
         name='company-clients'),

    path('printing-companies/', login_required(views.PrintingCompaniesAutocomplete.as_view()), name='printing-companies'),
    path('printing-machine-presets/', login_required(views.PrintingMachinePresetsAutocomplete.as_view()), name='printing-machine-presets'),
    path('cliche-technologies/', login_required(views.ClicheTechnologiesAutocomplete.as_view()), name='cliche-technologies')

]
