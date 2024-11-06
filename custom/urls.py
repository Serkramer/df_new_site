from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'custom'

urlpatterns = [
    path('company-clients/', login_required(views.CompanyClientsAutocomplete.as_view()),
         name='company-clients'),
]
