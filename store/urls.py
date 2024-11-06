from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = 'store'
urlpatterns = [
    path('materials/', login_required(views.MaterialsAutocomplete.as_view()),
         name='materials'),
]
