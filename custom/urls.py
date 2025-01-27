from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import CompaniesTableView, CompaniesTableDataView

app_name = 'custom'

urlpatterns = [
    path('company-card/', login_required(views.CompaniesCardView.as_view()), name='company_card'),
    path('company-card/<int:id>/', login_required(views.CompaniesCardView.as_view()), name='edit_company_card'),
    path('companies-table/', login_required(CompaniesTableView.as_view()), name='companies_table'),
    path('companies-table-data/', login_required(CompaniesTableDataView.as_view()), name='companies_table_data'),

    path('company-clients/', login_required(views.CompanyClientsAutocomplete.as_view()),
         name='company-clients'),
    path('printing-companies/', login_required(views.PrintingCompaniesAutocomplete.as_view()),
         name='printing-companies'),
    path('printing-machine-presets/', login_required(views.PrintingMachinePresetsAutocomplete.as_view()),
         name='printing-machine-presets'),
    path('cliche-technologies/', login_required(views.ClicheTechnologiesAutocomplete.as_view()),
         name='cliche-technologies'),
    path('contact-autocomplete/', views.ContactAutocomplete.as_view(), name='contact-autocomplete'),

]
